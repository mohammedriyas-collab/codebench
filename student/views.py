from django.shortcuts import render

# Create your views here.

from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from student.serializers import SignUpSerializer,StudentprofileSerializer,SubmissionSerializer
from student.models import StudentProfile
from rest_framework import authentication,permissions
from api.permission import OwnerOnly
from rest_framework.views import APIView
from api.models import Problem
from rest_framework.response import Response
#from student.agent import evaluate_answer
from student.models import Submission
from student.langchain_agent import evaluate_answer



class StudetrgistercreateView(CreateAPIView):

    serializer_class=SignUpSerializer


class StudentProfileRetriveUpdatedeleteView(RetrieveUpdateDestroyAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
   
    permission_classes=[OwnerOnly]
    
    serializer_class=StudentprofileSerializer

    queryset=StudentProfile.objects.all()

    def get_object(self):  # this method is for update the view(which view want to update) ,the retrive is working without an id becose of it is profile, 
        return StudentProfile.objects.get(user=self.request.user)

class SubmissionCreateView(APIView):

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):

        problem = Problem.objects.get(id=pk)


        student_answer=request.data.get("answer")

        # gemini integration (llm)

        result = evaluate_answer(problem,student_answer)

        print(result)

        Submission.objects.create(

            answer=student_answer,
            problem=problem,
            score=result.score,
            remarks=result.remarks,
            submitted_by=request.user,
            status="evaluated"

        )

        return Response({"mssg":"soluthion submitted succefully","score":result.score})



      

