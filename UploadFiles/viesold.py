import subprocess
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import  login
import plotly.offline as opy
from .models import *
from django.contrib import messages
import os
from .forms import MyFileForm
from django.http import FileResponse
from django.core.files.storage import default_storage
from .CS05.Segmentation import Securiti
import plotly.graph_objs as go
from django.shortcuts import render
from django.db.models import *
# Create your views here.


def forgotpassword(request):
    return render(request, "forgot-password.html")

def loginrender(request):
    return render(request,"index.html")

def FileAnalytics(request):
    up_files = MyFileUpload.objects.filter(status = 'Uploaded').aggregate(total=Count('file_name'))['total']
    deleted_files = MyFileUpload.objects.filter(status='Deleted').aggregate(deleted_files=Count('file_name'))['deleted_files']
    encrypted_files = MyFileUpload.objects.filter(mode='Encrypted',status='Uploaded').aggregate(encrypted_files=Count('file_name'))['encrypted_files']
    nonencrypted_files = MyFileUpload.objects.filter(mode='Non-Encrypted',status='Uploaded').aggregate(nonencrypted_files=Count('file_name'))[
        'nonencrypted_files']
    # Render the HTML code in the template


    # Add the size range annotation to the queryset
    data = MyFileUpload.objects.filter(status='Uploaded').values('file_size').annotate(
        average_time_difference=Avg((F('end_time') - F('start_time')) / 60, output_field=DurationField())
    )

    # Iterate over the data and access the file size and time difference
    file_sizes = [entry['file_size'] for entry in data]
    time_difference_minute = [round(float(entry['average_time_difference'].total_seconds()), 2) for entry in data]

    # Create the histogram trace
    histogram_trace = go.Bar(x=file_sizes, y=time_difference_minute, width=0.3)

    # Create the layout
    layout = go.Layout(
        title='Histogram of Average Time by File Size',
        xaxis=dict(title='File Size (MB)'),
        yaxis=dict(title='Time Difference (Minute)'))

    # Create the histogram trace
    histogram_trace = go.Bar(x=file_sizes,y=time_difference_minute,width=0.3)

    # Create the layout
    layout = go.Layout(
        title='Histogram of Average Time by File Size',
        xaxis=dict(title='File Size (MB)'),
        yaxis=dict(title='Time Difference (Minute)'),
    )

    # Create the figure
    fig = go.Figure(data=[histogram_trace], layout=layout)
    fig.update_layout( bargap=0.001)
    # Display the histogram
    div = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, "fileanalytics.html", {'up_files': up_files,'deleted_files':deleted_files,
                                                  'encrypted_files':encrypted_files,'nonencrypted_files':nonencrypted_files,
                                                  'div' :div})
def AddServer(request):
    if request.method == 'POST':
        hostname = request.POST['hostname']
        password = request.POST['password']
        portno = request.POST['portno']
        assignedID = request.POST['assignedID']
        serverdata = ServerData(hostname=hostname,password=password,portno=portno,assignedID=assignedID)
        serverdata.save()
    data = ServerData.objects.all()
    return render(request, 'server.html', {'data': data})
def EditServer(request,id):
    if request.method == 'POST':
        hostname = request.POST['hostname']
        portno = request.POST['portno']
        ServerData.objects.filter(assignedID= id).update(hostname = hostname,portno=portno)
    return redirect('/server')
def UpdateServer(request,id):
    status = ServerData.objects.get(assignedID=id)
    if status.status == 'Enabled':
        ServerData.objects.filter(assignedID= id).update(status = 'Disabled')
    else:
        ServerData.objects.filter(assignedID=id).update(status='Enabled')
    return redirect('/server')
def userdetails(request,user):
    id = 42
    serverdata = ServerData.objects.filter(status='Enabled')
    userfiles= MyFileUpload.objects.filter(user=user,status='Uploaded')
    node_dict = {}
    for i in serverdata:
        node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
    seg = Securiti(user, f"upload/{str(id)}", " ", " ", " ",node_dict)
    x = ['Storage Consumed']
    y = []
    storage_used, ext_record = seg.get_userStorage()
    y.append(round(storage_used,2))
    for i in range(len(ext_record)):
        x.append((ext_record[i][1]))
        y.append(round(ext_record[i][0],2))
    # Create the trace for the pie chart
    trace = go.Bar(
        x=y,  # ,'Media Files','Documents','Others']
        y=x ,
        orientation='h',
        marker=dict(color=['crimson', 'green', 'blue', 'yellow', 'magenta']),width=0.4
    )
    layout = go.Layout(
        title='User Storage Used Information',
        plot_bgcolor='lightblue',
        width=800,  # Set the width of the graph
        height=300,  # Set the height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Set the margins around the graph
        paper_bgcolor='white',
        xaxis_title="File Size (MB)",
        yaxis_title="File Type"


    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
        )
    )


    # Generate the HTML code for the pie chart
    div = opy.plot(fig, auto_open=False, output_type='div')
    return render(request,"userinfomodal.html", {'plot_div': div,'user':user,'userfiles':userfiles})


def adminpagerender(request):
    id = 42
    x,y=0,0
    extension,size= [],[]
    serverdata = ServerData.objects.filter(status='Enabled')
    node_dict = {}
    for i in serverdata:
        node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
    seg = Securiti(request.user.username,f"upload/{str(id)}", " ", " "," ",node_dict)
    totalserver = len(seg.nodes_dict)
    x,y,server_online,admin_record = seg.get_NoOfsegments()
    for i in range(len(admin_record)):
        extension.append(admin_record[i][1])
        size.append(round(admin_record[i][0],2))
    # Create the trace for the pie chart
    trace = go.Bar(
        x=x,
        y=y,
        marker=dict(color=['crimson','green','blue','yellow','magenta']),width=0.3
    )

    pie_trace = go.Pie(
        labels=extension,
        values=size,
        marker=dict(colors=['crimson','green','blue','yellow','magenta']))
    # Create the layout for the bar chart
    layout = go.Layout(
        title='Servers and Number of Segments Stored',
        xaxis=dict(title='Servers'),
        yaxis=dict(title='No of Segments')
    )
    fig = go.Figure(data=[trace],layout=layout)

    pie_fig = go.Figure(data =[pie_trace])
    fig.update_layout(
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
        )
    )
    # Generate the HTML code for the pie chart
    div = opy.plot(fig, auto_open=False, output_type='div')
    pie_div = opy.plot(pie_fig, auto_open=False, output_type='div')

    # Render the HTML code in the template

    return render(request,"admindashboard.html", {'plot_div': div,'server_online':str(server_online),
                                                  'totalserver':totalserver,'pie_div':pie_div})
def adminuserpagerender(request):
    data = UserStorage.objects.all()
    return render(request, 'user.html', {'data': data})
def myfilerender(request):
    return render(request,"myfile.html")
def signuprender(request):
    return render(request,"sign_uppage.html")
def index(request):
    return render(request, "index.html")
def dashboard(request):
    id = 42
    serverdata = ServerData.objects.filter(status='Enabled')
    node_dict = {}
    for i in serverdata:
        node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
    seg = Securiti(request.user.username,f"upload/{str(id)}", " ", " "," ",node_dict)
    x = ['Storage Consumed']
    y = []
    storage_used, ext_record = seg.get_userStorage()
    y.append(round(storage_used,2))
    for i in range(len(ext_record)):
        x.append(ext_record[i][1])
        y.append(round(ext_record[i][0],2))
    # Create the trace for the pie chart
    trace = go.Bar(
        x=y,        #,'Media Files','Documents','Others']
        y=x,
        orientation = 'h',
        marker=dict(color=['crimson','green','blue','yellow','magenta']),width=0.4
    )
    layout = go.Layout(
        title='User Storage Used Information',
        xaxis_title="File Size (MB)",
        yaxis_title="File Type"
    )

    fig = go.Figure(data=[trace],layout=layout)
    fig.update_xaxes(range=[0, 25])
    fig.update_layout(
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
        )
    )
    # Generate the HTML code for the pie chart
    div = opy.plot(fig, auto_open=False, output_type='div')
    return render(request,"dashboard.html",{'plot_div': div})


def activateemail(request,user, to_email):
    messages.success(request,f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration. <b>Note:</b>Check your spam folder ")


def sign_up(request):
    if request.method== 'POST':
        name = request.POST['name']
        email1 = request.POST['email1']
        password = request.POST['password1']
        if User.objects.filter(username=name).exists():
            messages.error(request, "sorry, this username is already taken")
            return redirect('/sign_uppage/')
        
        if User.objects.filter(email=email1).exists():
            return redirect('/sign_uppage/')
        else:
            user = User.objects.create_user(username=name,email=email1,password=password)
            user_info = UserStorage.objects.create(user = name)
            user.save()
            user_info.save()
            return redirect('/')
    else:
        return render(request,'sign_uppage.html')

def logout(request):
    UserStorage.objects.filter(user=request.user.username).update(is_loggedin=0)
    auth.logout(request)
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        
        login_username = request.POST['usernameL']
        login_password = request.POST['passwordL']
        user = auth.authenticate(username=login_username,password =login_password)

        if user is not None:
            # auth.login(request,user)
            login(request,user)
            if login_username and login_password == "admin":
                return redirect('/admindashboard')
            else:
                username = request.user.username.title()
                messages.success(request,f'{username} Successfully logged in')
                UserStorage.objects.filter(user=request.user.username).update(is_loggedin=1)
                return home(request)
        else:
            return redirect('/')
    else:
        return redirect('/')

        
def home(request):
    user_name = request.user.username
    mydata=MyFileUpload.objects.filter(user = user_name,status = "Uploaded")
    myform=MyFileForm()
    if mydata!='':
        context={'form':myform,'mydata':mydata}
        return render(request,"myfile.html",context)
    else:
        context={'form':myform}
        return render(request,"myfile.html",context)
def console(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        save_code(code)  # Save the code to the file
        try:
            skeleton_code = open('user_code.txt','r')
            skeleton_code = skeleton_code.read()
        except:
            skeleton_code = ''
        result = execute_code(code)  # Execute the predefined function
        context = {'result': result,'code': skeleton_code}
    else:
        try:
            skeleton_code = open('user_code.txt','r')
            skeleton_code = skeleton_code.read()
        except:
            skeleton_code = ''
        context = {'code': skeleton_code}
    return render(request, 'console.html', context)

def execute_code(code):
    result = subprocess.run(['python','-c', code], capture_output=True, text=True)
    return result.stdout + result.stderr


def save_code(code):
    with open('user_code.txt', 'wb') as f:
        f.write(code.encode('utf-8'))

def uploadfile(request):
    if request.method == "POST":
        myform = MyFileForm(request.POST, request.FILES)
        if myform.is_valid():
            MyFileName = request.POST.get('file_name')
            MyFile = request.FILES.get('file')
            file_name = MyFile.name
            user_name = request.user.username
            count = 1
            while MyFileUpload.objects.filter(user=user_name, file_name=file_name, status='Uploaded').exists():
                filename_parts = file_name.split('.')
                base_name = filename_parts[0]
                extension = filename_parts[1]
                if base_name[-1].isalpha():
                    file_name = f"{base_name}{count}.{extension}"
                else:
                    if int(base_name[-1]) <= 9  :
                        base_name=base_name.replace(base_name[-1],str(int(base_name[-1]) +1),1)
                    file_name = f"{base_name}.{extension}"
                    count += 1
            # else:
                # Save the encoded content to the database
            mydata = MyFileUpload.objects.create(file_name=file_name,user = user_name)
            mydata.save()
            with open(f"upload/{str(mydata.id)}", 'wb+') as destination:
                for chunk in MyFile.chunks():
                    destination.write(chunk)
            extension = os.path.splitext(file_name)[1]
            serverdata = ServerData.objects.filter(status='Enabled')
            node_dict = {}
            if serverdata:
                for i in serverdata:
                    node_dict[int(i.assignedID)] = [i.hostname,i.password,int(i.portno)]

                # id=request.POST['file_id']
                mode_prompt=int(request.POST['option'])
                seg = Securiti(request.user.username, f"upload/{str(mydata.id)}", extension, mode_prompt, "fixed",node_dict)
                file_size = seg.segmentation(str(mydata.id))

                file_size_mb = round((file_size/1024/1024),2)
                hostlst =""
                for i in seg.hostdata:
                    hostlst += str(i)
                if mode_prompt == 1:
                    mode = 'Encrypted'
                elif mode_prompt == 2:
                    mode = 'Custom'
                else:
                    mode = "Non-Encrypted"

                MyFileUpload.objects.filter(user=user_name, file_name=file_name, status="Uploaded").update(
                    file_size=file_size_mb, hostdata=hostlst, end_time=datetime.datetime.now(),mode = mode)
                us_storage = UserStorage.objects.get(user=user_name)
                us_storage = float(us_storage.storage_consumed) + float(file_size_mb)
                us_storage = round(us_storage,2)

                UserStorage.objects.filter(user=user_name).update(storage_consumed=us_storage)

                if os.path.exists(f"upload/{str(mydata.id)}"):
                    with open(f"upload/{str(mydata.id)}", 'wb+') as destination:
                        txt = str(file_size_mb).encode('utf-8')
                        destination.write(txt)

                messages.success(request, "File uploaded successfully.")

            else:
                messages.error(request,"No Online Server")
        return redirect("home")
    else:
        myform = MyFileForm()
    return render(request, 'upload_file.html', {'form': myform})


def deleteFile(request,id):
    try:
        mydata=MyFileUpload.objects.get(id=id)
        del_time = datetime.datetime.now()
        MyFileUpload.objects.filter(user=request.user.username, file_name=mydata.file_name, status="Uploaded").update(
            del_start_time=del_time)
        user_name = request.user.username
        serverdata = ServerData.objects.filter(status='Enabled')
        node_dict = {}
        for i in serverdata:
            node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
        seg = Securiti(user_name, f"upload/{str(mydata.id)}", "jpg", 1, "fixed",node_dict)
        file_size_mb =  MyFileUpload.objects.get(user=user_name, file_name =mydata.file_name,status = "Uploaded")
        file_size_mb = float(file_size_mb.file_size)

        us_storage = UserStorage.objects.get(user=user_name)
        us_storage = float(us_storage.storage_consumed) - file_size_mb
        if us_storage < 0:
            us_storage = 0.0
        UserStorage.objects.filter(user=user_name).update(storage_consumed=us_storage)
        seg.deletesegments(str(mydata.id))
        MyFileUpload.objects.filter(user= user_name,file_name=mydata.file_name,status='Uploaded').update(status = "Deleted",del_end_time=datetime.datetime.now())
        messages.success(request,'File deleted successfully.')
        return redirect('home')

    except FileNotFoundError:
        messages.error(request,'File has been deleted or doesnt exist')
    return redirect('home')

def downloadFile(request,id):
    try:
        mydata=MyFileUpload.objects.get(id=id)
        down_time = datetime.datetime.now()
        MyFileUpload.objects.filter(user=request.user.username, file_name=mydata.file_name, status="Uploaded").update(
            download_start_time=down_time)
        dl_count = MyFileUpload.objects.get(user = request.user.username , file_name = mydata.file_name, status= "Uploaded")
        count = dl_count.downloadcount
        serverdata = ServerData.objects.filter(status='Enabled')
        node_dict = {}
        for i in serverdata:
            node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
        seg = Securiti(request.user.username, f"upload/{str(mydata.id)}", "jpg", 1, "fixed",node_dict)
        data = mydata.hostdata
        host_list = []
        for i in data:
            host_list.append(int(i))
        seg.desegment(host_list,str(mydata.id))
        messages.success(request, f'{mydata.file_name.title()} Downloaded Successfully with decryption')
        count = int(count) + 1
        MyFileUpload.objects.filter(user=request.user.username,file_name = mydata.file_name, status= "Uploaded").update(downloadcount=count,download_end_time=datetime.datetime.now())
        file_path = str(mydata.id)
        response = FileResponse(default_storage.open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % mydata.file_name
        return response
    except MyFileUpload.DoesNotExist:
        messages.error(request,'File has been deleted or doesnt exist')

    return redirect('home')

def DownloadFileCustom(request,id):
    try:
        mydata=MyFileUpload.objects.get(id=id)
        down_time = datetime.datetime.now()
        MyFileUpload.objects.filter(user=request.user.username, file_name=mydata.file_name, status="Uploaded").update(
            download_start_time=down_time)
        dl_count = MyFileUpload.objects.get(user = request.user.username , file_name = mydata.file_name, status= "Uploaded")
        count = dl_count.downloadcount
        serverdata = ServerData.objects.filter(status='Enabled')
        node_dict = {}
        for i in serverdata:
            node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
        seg = Securiti(request.user.username, f"upload/{str(mydata.id)}", "jpg", 1, "fixed",node_dict)
        data = mydata.hostdata
        host_list = []
        for i in data:
            host_list.append(int(i))
        seg.user_desegment(host_list,str(mydata.id))
        messages.success(request, f'{mydata.file_name.title()} Downloaded Successfully with decryption')
        count = int(count) + 1
        MyFileUpload.objects.filter(user=request.user.username,file_name = mydata.file_name, status= "Uploaded").update(downloadcount=count,download_end_time=datetime.datetime.now())
        file_path = str(mydata.id)
        response = FileResponse(default_storage.open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % mydata.file_name
        return response
    except MyFileUpload.DoesNotExist:
        messages.error(request,'File has been deleted or doesnt exist')

    return redirect('home')


def downloadFileDEC(request,id):
    try:
        mydata=MyFileUpload.objects.get(id=id)
        down_time = datetime.datetime.now()
        MyFileUpload.objects.filter(user=request.user.username, file_name=mydata.file_name, status="Uploaded").update(
            download_start_time=down_time)
        dl_count = MyFileUpload.objects.get(user=request.user.username, file_name=mydata.file_name, status= "Uploaded")
        count = dl_count.downloadcount
        serverdata = ServerData.objects.filter(status='Enabled')
        node_dict = {}
        for i in serverdata:
            node_dict[int(i.assignedID)] = [i.hostname, i.password,int(i.portno)]
        seg = Securiti(request.user.username, f"upload/{str(mydata.id)}", "jpg", 0, "fixed",node_dict)
        data = mydata.hostdata
        host_list = []
        for i in data:
            host_list.append(int(i))
        seg.desegment(host_list,str(mydata.id))
        messages.success(request, f'{mydata.file_name.title()} Downloaded Successfully without decryption')
        count = int(count) + 1
        MyFileUpload.objects.filter(user=request.user.username, file_name=mydata.file_name, status= "Uploaded").update(downloadcount=count,download_end_time=datetime.datetime.now())
        file_path = str(mydata.id)
        response = FileResponse(default_storage.open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % mydata.file_name
        return response
    except MyFileUpload.DoesNotExist:
        messages.error(request,'File has been deleted or doesnt exist')

    return redirect('home')



