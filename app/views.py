from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import *
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from pathlib import Path
from tensorflow.keras.preprocessing import image
import os
import tensorflow as tf
from .models import *

root = Path(__file__).resolve().parent.parent
model = tf.keras.models.load_model('app/covid_detaction.h5')


# Create your views here.
def home(request):
    return render(request, 'app/index.html')


def test_create(request):
    form = ImageUploadForm()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('prediction')
    return render(request, 'app/test_create.html', {'form': form})


def prediction(request):
    user_id = request.user.id
    data = CovidUserModel.objects.filter(user=user_id).last()
    img_data = str(root) + str(data.image.url)
    img = tf.keras.utils.load_img(
        img_data, target_size=(224, 224)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['COVID', 'Lung_Opacity', 'Normal', 'Viral Pneumonia']
    if class_names[np.argmax(score)] == 'COVID':
        result = "Infected by Covid-19"
        positivity = True
    else:
        result = "Not Infected by Covid-19"
        positivity = False

    context = {
        'data': data,
        'result': result,
        'positivity': positivity,
        'accuracy': round(100 * np.max(score), 2)
    }

    return render(request, 'app/prediction.html', context)


def registration_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    return render(request, 'app/register.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login_view')
    return render(request, 'app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


def about_us(request):
    return render(request, 'app/about.html')
