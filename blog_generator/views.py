from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from os import getenv
from dotenv import load_dotenv
from openai import OpenAI
from .models import BlogPost

load_dotenv()
openAI = OpenAI(
  api_key=os.getenv('OPEN_AI_KEY')
)

# Create your views here.
@login_required
def index(request):
  return render(request,'index.html')

@csrf_exempt
def generate_blog(request):
  if request.method=='POST':
    try:
      data=json.loads(request.body)
      yt_link=data['link']

    except (KeyError,json.JSONDecodeError):
      return JsonResponse({'error':'Invalid data sent'},status=400)
    

    # get yt title
    # title=yt_title(yt_link)

    # get transcript
    # transcription=get_transcription(yt_link)
    # if not transcription:
    #   return JsonResponse({'error':'Failed to get transcript'},status=500)


    # use OpenAI to generate the blog
    blog_content=generate_blog_from_transcription("""Title: Achieve Your Goals in 2024!

[0:00]
"Welcome to this video! Today, we’ll discuss how to set and achieve your biggest goals for 2024. Whether it’s about career, health, or personal growth, this year is your time to shine!"

[0:15]
"First, let’s talk about clarity. To achieve any goal, you must know exactly what you want. Write it down, visualize it, and make it as specific as possible. Instead of saying, 'I want to get fit,' say, 'I want to lose 15 pounds by June.' Specificity is key!"

[1:00]
"Next, create a plan. Break your big goal into smaller, actionable steps. Remember, consistency beats perfection. If you dedicate 30 minutes a day to your goal, imagine how far you can go in a year!"

[2:00]
"Now, let’s address mindset. Self-doubt is the biggest barrier to success. Replace 'I can’t' with 'I will.' Your thoughts shape your reality, so choose empowering beliefs."

[3:00]
"Accountability is another game-changer. Share your goal with a friend or join a community with similar aspirations. Having someone to cheer you on makes all the difference."

[4:30]
"And finally, celebrate your progress! Every milestone, no matter how small, deserves recognition. Reward yourself—it keeps you motivated and reminds you how far you’ve come."

[5:30]
"Remember, 2024 is YOUR year. Start today, take action, and don’t stop until you’re proud. Thank you for watching, and don’t forget to like, share, and subscribe for more motivational content. You’ve got this!""")
    
    if not blog_content:
      return JsonResponse({'error':'Failed to generate blog article'},status=500)

    # save blog article to database
    new_blog_article=BlogPost.objects.create(
      user=request.user,
      youtube_title="Anything",
      youtube_link=yt_link,
      generated_content=blog_content,
    )

    new_blog_article.save()

    # return blog article as the response
    return JsonResponse({'content':blog_content})
  else:
    return JsonResponse({'error':'Invalid request method'},status=405)
  

def yt_title(link):
  yt=YouTube(link)
  title=yt.title
  return title

def download_audio(link):
  yt=YouTube(link)
  video=yt.streams.filter(only_audio=True).first()
  out_file=video.download(output_path=settings.MEDIA_ROOT)
  base,ext=os.path.splittext(out_file)
  new_file=base +'.mp3'
  os.rename(out_file,new_file)
  return new_file

def get_transcription(link):
  audio_file=download_audio(link)
  aai.settings.api_key=os.getenv('AAI_SETTTINGS_API_KEY')

  transcriber=aai.Transcriber()
  transcript=transcriber.transcribe(audio_file)

  return transcript.text

def generate_blog_from_transcription(transcription):
  prompt=f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but don't make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

  # response=openAI.completions.create(
  #   model='gpt-4o-mini',
  #   prompt=prompt,
  #   max_tokens=1000
  # )
  response = openAI.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": transcription}
    ]
)

  generated_content=response.choices[0].message.content
  return generated_content


def blog_list(request):
  blog_articles=BlogPost.objects.filter(user=request.user)
  return render(request,'all-blogs.html',{'blog_articles':blog_articles})

def blog_details(request,pk):
  blog_details=BlogPost.objects.get(id=pk)
  if request.user==blog_details.user:
    return render(request,'blog-details.html',{'blog_article_detail':blog_details})
  else:
    return redirect('/')

def user_login(request):
  if request.method=='POST':
    username=request.POST['username']
    password=request.POST['password']

    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('/')
    else:
      error_message="Invalid username or password entered!"
      return render(request,'login.html',{'error_message':error_message})
  return render(request,'login.html')

def user_signup(request):
  if request.method=='POST':
    username=request.POST['username']
    email=request.POST['email']
    password=request.POST['password']
    repeatPassword=request.POST['repeatPassword']

    if password==repeatPassword:
      try:
        user= User.objects.create_user(username,email,password)
        user.save()
        login(request,user)
        return redirect('/')
      except:
        error_message="Error creating the account! Please try again."
        return render(request,'signup.html',{'error_message':error_message})
    else:
      error_message='Password do not match'
      return render(request,'signup.html',{'error_message':error_message})
  return render(request,'signup.html')

def user_logout(request):
  logout(request)
  return redirect('/')