# -*- coding: utf-8 -*-
import os,re
import sys
import os.path 
import chardet
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

data_list = []
global data_list
'''data_list = os.listdir("static\\")
data1 = []
print data_list
for data in data_list:
    data_new = data.decode('gbk').decode('utf-8')
    data1 += [data_new]
data_list = data1
print data_list'''



reload(sys)
sys.setdefaultencoding('utf-8')

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*'.join(user_input) # Converts 'djm' to 'd.*j.*m'
    regex = re.compile(pattern)     # Compiles a regex.
    for item in collection:
        match = regex.search(item)  # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


def index(request):
    request.session['account'] = 'nopeople'
    return render_to_response( 'index.html')

def about(request):
    return render_to_response( 'about.html')

def contact(request):
    return render_to_response( 'contact.html')

@csrf_exempt
def download(request):
    warn = "下拉为现有资源总览↓"
    global data_list
    if request.GET:
        content = request.GET.get('do-search')
        data_s = fuzzyfinder(content, data_list)
        if data_s == []:
            warn = "未找到含该关键词的资源，请留言告知其他用户该需求"
        else:
            warn = "成功找到含有该关键词的资源，请下拉查看"
        return render(request,'page-download.html',{'data_list' : data_s, 'alert': warn})
    if request.POST:
        for data in data_list:
            if request.POST.has_key(data):
                filepath = 'static\\source\\' + data;
                file = open(filepath,'rb')  
                response = FileResponse(file)  
                response['Content-Type']='application/octet-stream'  
                response['Content-Disposition']='attachment;filename="{0}"'.format(data.encode('utf-8')) 
                return response
    global data_list
    data_list = os.listdir("static\\source\\")
    data1 = []
    for data in data_list:
        data_new = data.decode(encoding='gbk').decode(encoding='utf-8')
        data1 += [data_new]
    data_list = data1
    data_list = data1
    return render(request,'page-download.html',{'data_list':data_list, 'alert': warn})

@csrf_exempt
def upload(request):
    warn = ""
    if request.method == "POST":    
        myFile =request.FILES.get("myfile", None)   
        if not myFile:
            warn = "没有选择文件！"
            return render_to_response('upload.html', {'alert': warn})
        extention = os.path.splitext(myFile.name)[1]
        if request.POST['name'] == '':
            warn = "文件名不能为空，请重命名！"
            return render_to_response('upload.html', {'alert': warn})
        name = request.POST['name'] + extention
        if name in data_list:
            warn = "文件名重复，请重命名！"
            return render_to_response('upload.html', {'alert': warn})
        destination = open(os.path.join("static\\source\\",name),'wb+')
        #destination = open(os.path.join("static\\",myFile.name),'wb+')   
        for chunk in myFile.chunks():      
            destination.write(chunk)
        destination.close()
        global data_list
        #data_list += [myFile.name]
        data_list += [name]
        warn = "上传成功！"
    return render_to_response('upload.html', {'alert': warn})

@csrf_exempt
def login(request):
    warn = "请输入用户名和密码"
    if request.method == "POST":
        if request.POST['account_name'] == 'keeper'and request.POST['pass_word'] == '123456789':
                request.session['account'] = 'keeper'
                return HttpResponseRedirect("/page-keep")
        request.session['account'] = 'nopeople'
        warn = "用户名或密码错误！"
    return render_to_response('login.html', {'warning': warn})


#@login_required
def keep(request):
    request.session.setdefault('account','nopeople')
    if request.session['account'] != 'keeper':
        return HttpResponseRedirect("/login")
    global data_list
    if request.POST:
        for data in data_list:
            if request.POST.has_key(data):
                filepath = 'static\\source\\' + data;
                if(os.path.exists(filepath)):
                    os.remove(filepath)
                    data_list.remove(data)
                    return render(request,'page-keep.html',{'data_list':data_list})
                else:
                    return HttpResponse("删除失败，请尽快联系我们！")
    global data_list
    data_list = os.listdir("static\\source\\")
    data1 = []
    for data in data_list:
        data_new = data.decode(encoding='gbk').decode(encoding='utf-8')
        data1 += [data_new]
    data_list = data1
    return render(request,'page-keep.html',{'data_list':data_list})
