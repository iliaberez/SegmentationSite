from email.mime import base
from multiprocessing import context
import os
import re
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.template.response import TemplateResponse
from DiplomaSite.models import SegmentationPost
from DiplomaSite.utils import get_chart, get_chart_pred, get_graph
from .forms import LoginUserForm, RegisterUserForm, SegmentationForm
from keras.models import load_model
from keras import utils
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import base64
from django.core.files.base import ContentFile

global model
model = load_model('static/segmantation_lung_lobe_200epochs.hdf5', compile=False)

def home(request):
    return render(request,"DiplomaSite/home.html")
  
def index(request):
    return render(request, "DiplomaSite/home.html")
 
def segmentation(request):
    form = SegmentationForm()
    temp = []
    center = [256,256]
    if request.method == 'POST':
        if 'segmentation' in request.POST:
            form = SegmentationForm(request.POST)
            if form.is_valid:
                file = request.FILES['file']
                base_path = 'media/upload/'
                if request.user.is_authenticated :
                    base_path = 'media/upload/' + request.user.username + '/'
                fs = FileSystemStorage(location= base_path)
                filename = fs.save(file.name, file)
                number_slide = int(request.POST['number_slide'])
                epi_img = nib.load(base_path + filename)
                epi_img_data = epi_img.get_fdata()
                os.remove(os.path.join(base_path + filename))
                epi_img_data = epi_img_data[:,:,number_slide]
                image = np.zeros(np.concatenate((512,512), axis=None))
                image = image + epi_img_data[:,:]
                image = image[center[0]-200:center[0]+200,center[1]-160:center[1]+160]
                chart = get_chart(image)
                tempList = np.array(temp.append(image))
                tempList = utils.normalize(temp, axis= 1)
                image_dataset_encoded = np.expand_dims(tempList, axis = 3)
                predict = model.predict(image_dataset_encoded)
                chart_predict = get_chart_pred(predict)
                if request.user.is_authenticated :
                    original_file_name = 'original_' + (file.name).split('.')[0] + '.png'
                    segm_file_name = 'segm_' +(file.name).split('.')[0] + '.png'
                    fs.save(original_file_name, ContentFile(base64.b64decode(chart),'image.png'))
                    fs.save(segm_file_name, ContentFile(base64.b64decode(chart_predict),'image.png'))
                    post = SegmentationPost.objects.create(
                        author = request.user.username, 
                        number_slide = number_slide, 
                        original_file = original_file_name, 
                        segm_file = segm_file_name, 
                        description = '')
                context = {'chart': chart, 'predict' : chart_predict, 'form': form}
                return render(request, "DiplomaSite/segmentation.html", context)
        elif 'cancel' in request.POST:
            form = SegmentationForm()
            return render(request, "DiplomaSite/segmentation.html", form)
    else:
        return render(request, "DiplomaSite/segmentation.html", {'form': form})
 
def history(request):
    base_path = 'media/upload/' + request.user.username
    temp = SegmentationPost.objects.filter(author = request.user.username)
    data = []
    data.append(base_path + temp[0].original_file.url)
    print(data[0])
    return render(request, "DiplomaSite/history.html", context = {'elements' : data})

class RegisterUser(CreateView):
    form_class = RegisterUserForm   
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

