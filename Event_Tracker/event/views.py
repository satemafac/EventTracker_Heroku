# from cgitb import lookup
# from pickle import FALSE
# from pyexpat.errors import messages
# from turtle import title
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template import context
# from django.test import client
from django.urls import reverse
# from flask import request
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from decouple import config
from .serializers import *
from rest_framework import viewsets,generics,status      
from .models import *
from .models import Todo  
from .Event_forms import NameForm,SocialForm
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
from openai import OpenAI
from asgiref.sync import async_to_sync
import logging
from django.http import JsonResponse
from Event_Tracker.tasks import generate_flyer_task
from celery.result import AsyncResult
from django.views.decorators.http import require_GET


load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))
ideogram_ai = os.getenv('IDEOGRAM_AI')


# from Event_Tracker.event import serializers

DEBUG= config('DEBUG') 
# we write variable name we stored in .env inside quotes

# Create your views here.

# Set your OpenAI API key



# Set up logging
logger = logging.getLogger(__name__)

# Function to generate the flyer prompt using OpenAI's API
# def generate_flyer_prompt(event_name, location, organization, description, start_time, end_time):
#     # Create the base prompt
#     prompt = f"""
#     Give me a prompt to generate a beautiful and engaging flyer for this event.

#     Event Name: {event_name}
#     Location: {location}
#     Organization: {organization}
#     Description: {description}
#     Start Time: {start_time}
#     End Time: {end_time}

#     The flyer should have a modern and elegant design, matching the theme of the event, and should include the provided details in a clear and attractive manner.
#     """

#     # Call OpenAI API to get the prompt for flyer generation
#     response = client.chat.completions.create(
#         model="gpt-4",  # or use "gpt-3.5-turbo" depending on your preference
#         messages=[
#             {"role": "system", "content": "You are a creative assistant skilled in designing event flyers. Keep the prompts concise and to the point of creating an event flyer with no extra jargons."},
#             {"role": "user", "content": prompt},
#         ]
#     )

#     flyer_prompt = response.choices[0].message.content.strip()
#     print(flyer_prompt)

#     return flyer_prompt

# @csrf_exempt
# def generate_flyer(request):
#     if request.method == 'POST':
#         try:
#             # Extract data from the request
#             data = json.loads(request.body.decode('utf-8'))
#             event_name = data.get('event_name')
#             location = data.get('event_location')
#             organization = data.get('event_org')
#             description = data.get('about_event')
#             start_time = data.get('event_start_date')
#             end_time = data.get('event_end_date')

#             # Call the function to generate the flyer prompt
#             flyer_prompt = generate_flyer_prompt(event_name, location, organization, description, start_time, end_time)

#             # Call the Ideogram API to generate an image based on the flyer prompt
#             ideogram_api_url = "https://api.ideogram.ai/generate"
#             ideogram_payload = {
#                 "image_request": {
#                     "model": "V_2",  # Replace with the appropriate model as per Ideogram's API docs
#                     "magic_prompt_option": "AUTO",
#                     "prompt": f"{flyer_prompt}"  # Ensure flyer_prompt is correctly added as a string
#                 }
#             }

#             headers = {
#                 "accept": "application/json",
#                 "content-type": "application/json",
#                 "Api-Key": f"{ideogram_ai}"  # Assuming the API uses Bearer token authentication
#             }

#             print(ideogram_payload)
#             print(headers)

#             ideogram_response = requests.post(ideogram_api_url, json=ideogram_payload, headers=headers)

#             if ideogram_response.status_code == 200:
#                 image_data = ideogram_response.json()
#                 # Return the image data or image URL as a JSON response
#                 return JsonResponse({'flyer_prompt': flyer_prompt, 'image_data': image_data})
#             else:
#                 return JsonResponse({'error': 'Failed to generate image with Ideogram API', 'details': ideogram_response.text}, status=500)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_flyer(request):
    if request.method == 'POST':
        try:
            # Retrieve Celery settings
            CELERY_BROKER_URL = os.getenv('REDIS_URL')
            CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')

            # Print the CELERY_BROKER_URL for debugging
            print(f"CELERY_BROKER_URL: {CELERY_BROKER_URL}")

            data = json.loads(request.body.decode('utf-8'))
            # Start the Celery task
            task = generate_flyer_task.delay(data)
            # Return the task ID to the client
            return JsonResponse({'task_id': task.id})
        except Exception as e:
            # Print the exception for debugging
            print(f"Error in generate_flyer view: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@require_GET
def get_task_status(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'PENDING':
        # Task hasn't started yet
        response = {'state': result.state}
    elif result.state == 'PROGRESS':
        # Task is in progress
        response = {'state': result.state}
    elif result.state == 'SUCCESS':
        # Task completed successfully
        response = {
            'state': result.state,
            'result': result.result
        }
    elif result.state == 'FAILURE':
        # Task failed
        response = {
            'state': result.state,
            'error': str(result.result)
        }
    else:
        # Other states
        response = {'state': result.state}
    return JsonResponse(response)

def start_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect(home_page)
    else:
        return render(request, "event/index.html")

def home_page(request):
    user = request.user

    auth0_user = user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']
    }
    print(user_data)

    # event_list = Event.objects.all()
    # event_host = Event_Host.objects.all()
    event_join = Event_Host.objects.select_related('host','social','event').filter(auth_user=user.id)
    context = {
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user,
        'event_join': event_join
    }



    return render(request, "event/home.html",context)


def home_save_form(request):

    user = request.user

    context = {}
    if request.method!="POST":
        return HttpResponseRedirect(reverse("home-page"))
    else:
        event_name = request.POST.get("event_name")
        event_location = request.POST.get("event_location")
        event_org = request.POST.get("event_org")
        event_img = request.FILES['event_img'] if 'event_img' in request.FILES else False
        if event_img != False:
            fs = FileSystemStorage()
            media_name = fs.save(event_img.name, event_img)
            context['media_url'] = fs.url(media_name)
            print(event_img.size)
        about_event = request.POST.get("about_event")
        event_start_date = request.POST.get("event_start_date")
        event_end_date = request.POST.get("event_end_date")
        twitter = request.POST.get("twitter")
        instagram = request.POST.get("instagram")
        Facebook = request.POST.get("facebook")
        user_bio = request.POST.get("user_bio")
        user_fname = request.POST.get("fname")
        user_lname = request.POST.get("lname")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        event_user=Event_Users(user_fname=user_fname, user_lname=user_lname,username=username, is_event_host=True)
        event_user.save()
        print("this is evnt users",event_user.pk)
        social_media=Event_Socials(twitter=twitter,Facebook=Facebook,instagram=instagram,user_bio=user_bio,phone=phone,email=email,user_id_id=event_user.pk)
        social_media.save()
        event_create=Event(event_name=event_name, event_location=event_location, event_org=event_org,event_start_date=event_start_date, event_end_date=event_end_date, event_image = fs.url(media_name) if event_img != False else "", about_event = about_event, host_id=event_user.pk)
        event_create.save()
        event_host=Event_Host(host_id=event_user.user_id, social_id=social_media.social_id,event_id=event_create.pk, auth_user = user.id)
        event_host.save()
        messages.success(request, "Data Save Successfully")
        return HttpResponseRedirect(reverse("home-page"))
        # except:
        #     messages.error(request,"Error in Saving Data")
        #     return HttpResponseRedirect(reverse("home-page"))


def profile(request):
    user = request.user

    auth0_user = user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']
    }

    context = {
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user
    }

    return render(request,"event/profile.html",context)

def create(request):
    user = request.user

    auth0_user = user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']
    }

    return render(request,"event/create.html")



def man_event(request):
    user = request.user
    event_list = Event_Host.objects.select_related('host','social','event').filter(auth_user=user.id)

    return render(request, "event/man_event.html", {'event_list': event_list})

def event_entree(request, event_code = None):
    event_code = event_code
    user = request.user
    context={
        'event' : 'http://127.0.0.1:8000/event/'+event_code,
        'event_code' : Event.objects.filter(event_code=event_code)
    }


    # for code in event_code:
    #     print(code.event_code_short)

    return render(request, "event/event_entree.html", context,)



@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        data = Event_Users.objects.all()

        serializer = UsersSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def users_detail(request, pk):
    try:
        users = Event_Users.objects.get(pk=pk)
    except Event_Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UsersSerializer(users, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def socials_list(request):
    if request.method == 'GET':
        data = Event_Socials.objects.all()

        serializer = SocialsSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SocialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def socials_detail(request, pk):
    try:
        socials = Event_Socials.objects.get(pk=pk)
    except Event_Socials.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = SocialsSerializer(socials, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        socials.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def attendee_list(request):
    if request.method == 'GET':
        data = Event_Attendee.objects.all()

        serializer = AttendeeSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttendeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def attendee_detail(request, pk):
    try:
        attendee = Event_Attendee.objects.get(pk=pk)
    except Event_Attendee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AttendeeSerializer(attendee, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Event_Attendee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetEvent(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'event_code_short'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Event.objects.filter(event_code_short=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Event Not Found': 'Invalid Event Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class RoomView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = RoomSerializer

class JoinEvent(APIView):   
    lookup_url_kwarg = 'event_code_short'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        print(code)
        if code != None:
            room_result = Event.objects.filter(event_code_short=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['event_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)

def delete_event(request, event_idd):
    event_db = Event_Host.objects.select_related('host','social','event').filter(event_id=event_idd)
    Event_Users.objects.filter(user_id=event_db.first().host_id).delete()
    return redirect("man_event")

def update_event_form(request, event_idd): 
    print(event_idd)

    user = request.user

    context = {}
    if request.method!="POST":
        return HttpResponseRedirect(reverse("man_event"))
    else:
        event_name = request.POST.get("event_name")
        event_location = request.POST.get("event_location")
        event_org = request.POST.get("event_org")
        event_img = request.FILES['event_img'] if 'event_img' in request.FILES else False
        if event_img != False:
            fs = FileSystemStorage()
            media_name = fs.save(event_img.name, event_img)
            context['media_url'] = fs.url(media_name)
            print(event_img.size)
        about_event = request.POST.get("about_event")
        event_start_date = request.POST.get("event_start_date")
        event_end_date = request.POST.get("event_end_date")
        twitter = request.POST.get("twitter")
        instagram = request.POST.get("instagram")
        Facebook = request.POST.get("facebook")
        user_bio = request.POST.get("user_bio")
        user_fname = request.POST.get("fname")
        user_lname = request.POST.get("lname")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        print(twitter + Facebook)
        # try:
        # event = Event_Host.objects.select_related('host','social','event').filter(event_id=event_idd).update(host_id=event_user.user_id, social_id=social_media.social_id,event_id=event_create.pk, auth_user = user.id)
        event_db = Event_Host.objects.select_related('host','social','event').filter(id=event_idd)
        # host = Event_Host.objects.get(id=event_idd,host_id=host_id)
        print(event_db[0].social_id)



        # eventt = Event.objects.filter('host', 'event_social').update_or_create()

        # Tweet.objects.filter(pk=1).update(tweet_id=mentions.meta.get("newest_id"))
        event_user=Event_Users.objects.filter(user_id=event_db[0].host_id).update(user_fname=user_fname, user_lname=user_lname,username=username)
        #Get pk from event_social
        # event_user.save()
        # print("this is evnt users",event_user.pk)
        social_media=Event_Socials.objects.filter(social_id=event_db[0].social_id).update(twitter=twitter,Facebook=Facebook,instagram=instagram,user_bio=user_bio,phone=phone,email=email)
        #Get social id from event_host and then update by that pk
        # social_media.save()
        event_create=Event.objects.filter(event_id=event_db[0].event_id).update(event_name=event_name, event_location=event_location, event_org=event_org,event_start_date=event_start_date, event_end_date=event_end_date, event_image = fs.url(media_name) if event_img != False else "", about_event = about_event)
        # event_create.save()
        # event_host=Event_Host.objects.update(host_id=event_db[0].id, social_id=social_media.social_id,event_id=event_create.pk, auth_user = user.id)
        #UPDATE by event_id
        # event_host.save()
        messages.success(request, "Data Save Successfully")
        return HttpResponseRedirect(reverse("man_event"))
        # except:
        #     messages.error(request,"Error in Saving Data")
        #     return HttpResponseRedirect(reverse("home-page"))


def update_event(request, event_idd):

    # event = Event_Host.objects.get(pk=event_id)
    event = Event_Host.objects.select_related('host','social','event').filter(event_id=event_idd)
    return render(request, "event/update_event.html", {'event': event})


def logout(request):
    django_logout(request)

    domain=config('APP_DOMAIN')
    client_id=config('APP_CLIENT_ID')
    # return_to='http://127.0.0.1:8000/host/'
    return_to='https://event.sharetunez.me/'


    return HttpResponseRedirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")

class TodoView(viewsets.ModelViewSet):  
    serializer_class = TodoSerializer   
    queryset = Todo.objects.all()

