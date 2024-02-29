import os
import json
import nltk
import random
from .models import Video
from django.contrib import auth
from .tasks import process_video
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
# from asgiref.sync import sync_to_async,async_to_sync
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.core.files import File

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        videos = Video.objects.filter(user=user)
        if videos != None:
            return render(request,'home.html',{"video":videos})
        else:
            return render(request,'home.html')
    else:
        return render(request,'home.html')

def about_view(request):
	return render(request,'about.html')

def contact_view(request):
	return render(request,'contact.html')

def drive(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        videos = Video.objects.filter(user=user)
        if videos != None:
            return render(request,'drive.html',{"video":videos})
        else:
            return render(request,'drive.html')
    else:
        return render(request,'drive.html')

def show_video(request,video_id):
    video = Video.objects.get(id =video_id)
    return render(request,'show_video.html',{'video':video})

def add_file(request):
    if request.method == 'POST':

        req_dict = dict(request.POST.items())
        csrfmiddlewaretoken = req_dict['csrfmiddlewaretoken']

        # Generate a random integer between 1 and 100 (inclusive)
        random_number = str(random.randint(1, 10000000))
        request.FILES['video'].name = request.FILES['video'].name.replace(" ","_")
        request.FILES['subtitles'].name = request.FILES['subtitles'].name.replace(" ","_")
        current_directory = os.getcwd()
        print(current_directory)

        user_id = str(request.user.id)
        video_file_path =  current_directory + '\\media\\videos\\' + str(user_id) + "_" + random_number + "_" + request.FILES['video'].name
        subtitles_file_path =  current_directory + '\\media\\videos\\' + str(user_id) + "_" + random_number + "_" + request.FILES['subtitles'].name

        with open(video_file_path, 'wb') as f:
            for chunk in request.FILES['video'].chunks():
                f.write(chunk)

        with open(subtitles_file_path, 'wb') as f:
            for chunk in request.FILES['subtitles'].chunks():
                f.write(chunk)

        data = {
            'video_file_path': video_file_path,
            'video_file_name':request.FILES['video'].name,
            'subtitles_file_path': subtitles_file_path,
            'subtitles_file_name':request.FILES['subtitles'].name,
            'user_id' : request.user.id,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }

        # json_data = json.dumps(data)
        # status = process_video.delay(json_data) # calling celery task

        try:
            video = Video()
            video_file_path = data['video_file_path']
            subtitles_file_path = data['subtitles_file_path']
            video.video.name = 'videos/' + str(user_id) + "_" + random_number + "_" + request.FILES['video'].name
            video.subtitles.name = 'videos/' + str(user_id) + "_" + random_number + "_" + request.FILES['subtitles'].name
            video.user = User.objects.get(id=request.user.id)
            video.video_file_name = request.FILES['video'].name
            video.save()
            success = {"success":"Files Uploaded Successfully!"}
            return render(request,'add_file.html',success)
            # return render(request,'add_file.html',{'task_id': status.task_id})

        except Exception as e:
            print(e)
            error = {"error":"Files Upload Failed!"}
            return render(request,'add_file.html',error)
    else:
        return render(request,'add_file.html')

def signup(request):
    # to check request is genuine or not
    if request.method=="POST":
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request,'signup.html',{'error':'WARNING !!! Username Already Exist.'})
            except User.DoesNotExist:
                if len(request.POST['pass1'])>8:
                    user = User.objects.create_user(username = request.POST['username'], password = request.POST['pass1'] )
                    auth.login(request,user)
                    return redirect('home')
                else:
                    return render(request,'signup.html',{'error':'WARNING !!! Length of password should be greater than 8 letters.'})
        else:
            return render(request,'signup.html',{'error':'WARNING !!! Passwords Do Not Match.'})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username = request.POST['username'],password = request.POST['pass'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'WARNING !!! Username Or Password Is Incorrect'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url="login")
def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text;


		return render(request,'animation.html',{'words':words,'text':text})
	else:
		return render(request,'animation.html')
