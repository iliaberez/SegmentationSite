import os
from keras import utils
import nibabel as nib
import numpy as np
import base64
import uuid
from keras.models import load_model
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from DiplomaSite.models import SegmentationPost
from DiplomaSite.utils import get_chart, get_chart_pred
from .forms import LoginUserForm, RegisterUserForm, SegmentationForm
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

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
    base_path = 'media/upload/'
    if request.user.is_authenticated :
        base_path = 'media/upload/' + request.user.username + '/'
    fs = FileSystemStorage(location= base_path)
    if request.method == 'POST':
        if 'segmentation' in request.POST:
            form = SegmentationForm(request.POST)
            file = request.FILES['file']
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
            context = {'file': file, 'number_slide': number_slide,'chart': chart, 'predict' : chart_predict, 'form': form}
            return render(request, "DiplomaSite/segmentation.html", context)
        elif 'save' in request.POST:
            form = SegmentationForm(request.POST)
            user = User.objects.get(username = request.user.username)
            if form.is_valid:
                number_slide = int(request.POST['number_slide'])
                name_pacient = request.POST['name_pacient']
                description = request.POST['description']
                filename = request.POST['file']
                chart = request.POST.get('chart')
                chart_predict = request.POST.get('predict')
                description = request.POST['description']
                generator = str(uuid.uuid4())
                original_file_name = 'original_' + generator +  '.png'
                segm_file_name = 'segm_' + generator + '.png'
                if os.path.isfile(base_path + original_file_name):
                    generator = str(uuid.uuid4())
                    original_file_name = 'original_' + generator +  '.png'
                    segm_file_name = 'segm_' + generator + '.png'
                fs.save(original_file_name, ContentFile(base64.b64decode(chart),'image.png'))
                fs.save(segm_file_name, ContentFile(base64.b64decode(chart_predict),'image.png'))
                post = SegmentationPost.objects.create(
                    author = request.user.username, 
                    number_slide = number_slide, 
                    original_file = original_file_name, 
                    segm_file = segm_file_name, 
                    name_pacient = name_pacient,
                    description = description)
                post.viewers.add(user)
                form = SegmentationForm()
            return render(request, "DiplomaSite/segmentation.html", {'form': form})
        elif 'cancel' in request.POST:
            form = SegmentationForm()
            return render(request, "DiplomaSite/segmentation.html", {'form': form})
    else:
        return render(request, "DiplomaSite/segmentation.html", {'form': form})
 
def history(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            print('delete')
            base_path = 'media/upload/' + request.user.username + '/'
            idPost = request.POST['idPost']
            data = SegmentationPost.objects.get(id = idPost)
            os.remove(base_path + data.original_file.url.split('/')[2],)
            os.remove(base_path + data.segm_file.url.split('/')[2],)
            data.delete()
            return HttpResponseRedirect("/history/")
    temp = SegmentationPost.objects.filter(viewers__id = request.user.id)
    base_path = '/media/upload/'
    url = '/segmentations'
    data = []   
    for element in temp:
        data.append(HistoryPost(
            element.id,
            element.author,
            element.name_pacient,
            base_path + element.author + '/' + element.original_file.url.split('/')[2],
            url + '/' + str(element.id) + '/'
        ))
    return render(request, "DiplomaSite/history.html", context = {'elements' : data})

class HistoryPost():
    def __init__(self, id, author, name_pacient, image_path, url):
        self.id = id
        self.author = author
        self.name_pacient = name_pacient
        self.image_path = image_path
        self.url = url

def details(request, SegPostId):
    data = SegmentationPost.objects.get(id = SegPostId)
    viewers = list(User.objects.filter(segmentationpost__id = SegPostId))
    form = None
    error = None
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = SegmentationForm(initial={'name_pacient': data.name_pacient, 'description': data.description})
            context = {'form' : form}
            return render(request, "DiplomaSite/details.html", context)
        if 'save' in request.POST:
            form = SegmentationForm(request.POST)
            data.name_pacient = request.POST['name_pacient']
            data.description = request.POST['description']
            data.save()
            form = None
        if 'cancel' in request.POST:
            form = None
        if 'add' in request.POST:
            viewer = request.POST['viewer']
            user = User.objects.filter(username = viewer).first()
            if user and user not in viewers:
                data.viewers.add(user)
                viewers.append(user)
            elif user in viewers:
                error = 'This user has already been added'
            else:
                error = 'User not find'
        if 'delete' in request.POST:
            current_name = request.POST['current_name']
            delete_user = User.objects.get(username = current_name)
            data.viewers.remove(delete_user)
            viewers = list(User.objects.filter(segmentationpost__id = SegPostId))
    for viewer in viewers:
        if data.author == viewer.username:
            viewers.remove(viewer)
            break
    base_path = '/media/upload/' + data.author + '/'
    context = {
        'form': form,
        'chart' : base_path + data.original_file.url.split('/')[2],
        'pred': base_path + data.segm_file.url.split('/')[2],
        'name_pacient' : data.name_pacient,
        'description' : data.description,
        'author': data.author,
        'viewers' : viewers,
        'error': error
    }
    return render(request, "DiplomaSite/details.html", context)

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

