from multiprocessing import context
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.template.response import TemplateResponse
from DiplomaSite.models import ElementHistory
from DiplomaSite.utils import get_chart, get_chart_pred, get_graph
from .forms import LoginUserForm, RegisterUserForm, UserForm, UploadFileForm
from keras.models import load_model
from keras import utils
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

global model
model = load_model('static/segmantation_lung_lobe_200epochs.hdf5', compile=False)

def home(request):
    return render(request,"DiplomaSite/home.html")
  
def index(request):
    return render(request, "DiplomaSite/home.html")
 
def segmentation(request):
    temp = []
    if request.method == 'POST':
        center = [256, 256]
        epi_img = nib.load('static/4.nii')
        epi_img_data = epi_img.get_fdata()
        epi_img_data = epi_img_data[:,:,61]
        image = np.zeros(np.concatenate((512,512), axis=None))
        image = image + epi_img_data[:,:]
        image = image[center[0]-200:center[0]+200,center[1]-160:center[1]+160]
        chart = get_chart(image)
        tempList = np.array(temp.append(image))
        tempList = utils.normalize(temp, axis= 1)
        image_dataset_encoded = np.expand_dims(tempList, axis = 3)
        predict = model.predict(image_dataset_encoded)
        chart_predict = get_chart_pred(predict)
        context = {'chart': chart, 'predict' : chart_predict}
        return render(request, "DiplomaSite/segmentation.html", context)
    else:
        return render(request, "DiplomaSite/segmentation.html")
 
def history(request):
    data = []
    data.append(ElementHistory(numberPacient= '1', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
    data.append(ElementHistory(numberPacient= '2', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
    data.append(ElementHistory(numberPacient= '3', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
    data.append(ElementHistory(numberPacient= '4', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
    data.append(ElementHistory(numberPacient= '5', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
    data.append(ElementHistory(numberPacient= '6', Date= '11.04.2022', Disease='Fibrosco Tuberculesis'))
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

