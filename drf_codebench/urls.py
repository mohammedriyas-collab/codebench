"""
URL configuration for drf_codebench project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from api.views import ProblemListCreateView
from api.views import UpadteDeleteView
from api.views import AdminCreateView
from api.views import ProblemRetriveView
from student.views import SubmissionCreateView
from student.views import StudetrgistercreateView,StudentProfileRetriveUpdatedeleteView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/token/",ObtainAuthToken.as_view()),
    path("api/admin/register/",AdminCreateView.as_view()),
    path("api/problems/",ProblemListCreateView.as_view()),
    path("api/problems/<int:pk>/",UpadteDeleteView.as_view()),
    path("api/problems/<int:pk>/details/",ProblemRetriveView.as_view()),
   #student
    path("api/register/",StudetrgistercreateView.as_view()),
    path("api/profile/",StudentProfileRetriveUpdatedeleteView.as_view()),
    path("api/problem/<int:pk>/solution/",SubmissionCreateView.as_view()),

]
