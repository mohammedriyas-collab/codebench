from django.shortcuts import render

# Create your views here.

from django.contrib.auth.backends import ModelBackend    #=> to impliment the athutication by phone numb and password

from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework import permissions ,authentication
from api.serializers import ProblemSerializer,AdminSerializers
from api. models import Problem
from api. permission import OwnerOnly

class AdminCreateView(CreateAPIView):

    serializer_class=AdminSerializers

class ProblemListCreateView(ListAPIView,CreateAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]

    serializer_class=ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(posted_by=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(posted_by=self.request.user)  #to save the user which who creted the posted_by(posted_by fields read only field that why this is done like this)

class UpadteDeleteView(UpdateAPIView,DestroyAPIView):

    serializer_class=ProblemSerializer

    queryset = Problem.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes = [OwnerOnly]



class ProblemRetriveView(RetrieveAPIView):

    queryset = Problem.objects.all()

    serializer_class = ProblemSerializer

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]