from django.contrib import admin
from django.urls import path
from UploadFiles import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('myfile',views.home,name="home"),
    path('uploadfile',views.uploadfile,name="uploadfile"),
    path('deleteFile/<int:id>',views.deleteFile),
    path('downloadFile/<int:id>',views.downloadFile, name="downloadFile"),
    path('downloadFileDEC/<int:id>', views.downloadFileDEC),
    path('DownloadFileCustom/<int:id>',views.DownloadFileCustom, name="downloadFileCustom"),
    path('dashboard',views.dashboard),
    path('',views.loginrender),
    path('sign_uppage',views.signuprender),
    path('admindashboard/',views.adminpagerender),
    path('fileanalytics/',views.FileAnalytics),
    path('user/',views.adminuserpagerender),
    path('myfile', views.myfilerender),
    path('server/',views.AddServer,name="add_server"),
    path('server/<int:id>',views.EditServer,name="edit_server"),
    path('UpdateServer/<int:id>',views.UpdateServer),
    path('userinfomodal/<str:user>',views.userdetails),
    path('logout/',views.logout),
    path('dashboard/',views.dashboard),
    path('console', views.console,name="console"),
    path('sign_uppage/',views.sign_up,name="sign_up"),
    path('home',views.login_user,name="login_user"),
    path('myfile',views.cancel),
    path('getprogress/<int:id>', views.getprogress, name='getprogress'),

    path('forgot-password.html', views.forgotpassword),

path('password-reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),
         name='password_reset'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='forgot_password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('', auth_views.PasswordResetCompleteView.as_view(
        template_name='/'), name='password_reset_complete'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
