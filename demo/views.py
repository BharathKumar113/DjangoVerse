from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import instaloader
import qrcode
import io
import os
import requests
from django.conf import settings
from .models import Sample
import django.contrib.messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from PIL import Image
import stepic
# Create your views here.
def user(request,name):
    return HttpResponse(f"Hello {name}")
def home(request):
    username=request.user.username
    return render(request,"demo1.html",{'username':username})
def qr(request):
    if request.method=='POST' :
        text=request.POST.get('text') 
        q=qrcode.make(text)  
        buffer=io.BytesIO()
        q.save(buffer,format='PNG')
        buffer.seek(0)
        response=HttpResponse(buffer,content_type="image/png")
        response['Content-Disposition']=f'attachment;filename="new.png"'
        return response
def Qrcode(request):
    return render(request,"qrcode.html")
@login_required    
def insta(request):
    return render(request,'insta.html')
@login_required    
def insta_download(request):
    if request.method == 'POST':
        link = request.POST['url']
        try:
            loader = instaloader.Instaloader()
            shortcode = link.split("/")[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url
            response = requests.get(video_url)
            buffer = io.BytesIO(response.content)
            buffer.seek(0)
            response1 = HttpResponse(buffer, content_type='video/mp4')
            response1['Content-Disposition'] =f'attachment;filename="{shortcode}.mp4"'
            return response1
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Invalid request method", status=400)

def sample(request):
               details=Sample.objects.all()
               data=Sample.objects.get(id=1)                            
               return render(request,'sample.html',{"data":data})                                 
def pdf_protect(request):
    return render(request,'pdf.html')   
from PyPDF2 import PdfReader, PdfWriter

def pdf_process(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf = request.FILES['file']
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, 'new.pdf')

        
        with open(save_path, "wb") as file:
            for chunk in pdf.chunks():
                file.write(chunk)
        password = request.POST.get('password', '1234')  
        encrypted_path = os.path.join(upload_dir, 'protected.pdf')

        try:
            reader = PdfReader(save_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(encrypted_path, 'wb') as f:
                writer.write(f)

           
            with open(encrypted_path, "rb") as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="protected.pdf"'
                return response

        except Exception as e:
            return HttpResponse(f"Error while encrypting PDF: {e}")

    return HttpResponse("Failed to process PDF")  
def text(request):
    return render(request,'text.html')
import gtts       
def text_process(request):  
    if request.method == 'POST':
        text = request.POST.get('text', '')
        
        if text.strip() != '':
            tts = gtts.gTTS(text)
            buffer = io.BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
            return response
        else:
            return HttpResponse("Please enter some text to convert.")
    else:
        return HttpResponse("Invalid request method", status=400)
@login_required        
def stego(request):
    return render(request,"index.html")
@login_required    
def encode(request):
    if request.method=="POST" :
        message=request.POST['message']   
        image=request.FILES['image']
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, 'new.png')
        with open(save_path,"wb") as file:
            for chunk in image.chunks():
                file.write(chunk)
        original_image=Image.open(save_path)
        encoded_image_path=os.path.join(upload_dir,'encoded.png')
        encoded_image=stepic.encode(original_image,message.encode())
        encoded_image.save(encoded_image_path)
        return render(request,'result.html',{'success':True})
        
    else:
              
              return HttpResponse("Invalid Method")          
@login_required              
def return_encoded(request):
                                      
                      upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
                                      
                      os.makedirs(upload_dir, exist_ok=True)
                      save_path = os.path.join(upload_dir, 'encoded.png')
                      response=HttpResponse(open(save_path,"rb"),content_type="image/png")
                      return response
def decoded(request):           
       if request.method=="POST":
               img=request.FILES["image"]
               upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
               os.makedirs(upload_dir, exist_ok=True)
               save_path = os.path.join(upload_dir, 'user_encoded.png')
               with open(save_path,"wb") as file:
                 for chunk in img.chunks():
                     file.write(chunk)
                 decode_image=Image.open(save_path)
                 message=stepic.decode(decode_image)
                 return render(request,"result.html",{'message':message})   
def get_signup(request):
         return render(request,"signup.html")                 
def signup(request):       
    if request.method=="POST":
        username=request.POST['username']   
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request,"Password Do Not Match")
            return redirect('get_signup')
        if User.objects.filter(username=username).exists():
            messages.error(request,"User name Already exists")
            return redirect('get_signup')    
        if  User.objects.filter(email=email).exists():
            messages.error(request,"Email Id Already Exists")
            return redirect('get_signup')
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.success(request,f"Your Account created Successfully:  {username}")
        return redirect('get_login')
    return redirect('get_signup')     
def get_login(request):
    return render(request,"login.html")
def login_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
                       login(request,user)
                       messages.success(request,f"Welcome Back {username}")
                       return redirect('home')
        else:
             messages.error(request,"Invalid Username or Password")
             return redirect('get_login')
    return redirect('get_login')  
def get_logout(request):
    logout(request)
    return redirect("home")    