# -*- coding: utf-8 -*-
import os 
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt

data_list = []
global data_list

def page1(request):
    return render_to_response( 'hello.html')

@csrf_exempt
def download(request):
    global data_list
    if request.POST:
        for data in data_list:
            if request.POST.has_key(data):
                filepath = 'static\\' + data;
                file=open(filepath,'rb')  
                response =FileResponse(file)  
                response['Content-Type']='application/octet-stream'  
                response['Content-Disposition']='attachment;filename=%s' % (data)  
                return response
    return render(request,'page-download.html',{'data_list':data_list})

@csrf_exempt
def upload(request):
    if request.method == "POST":    
        myFile =request.FILES.get("myfile", None)   
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join("static\\",myFile.name),'wb+')    
        for chunk in myFile.chunks():      
            destination.write(chunk)
        destination.close()
        global data_list
        data_list += [myFile.name]
        return HttpResponse("upload over!")
    else:
        return render_to_response('page-upload.html')
