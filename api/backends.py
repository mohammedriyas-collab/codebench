# to create  custom authentication by phone number and password  , need a new file which is backends.py




from django.contrib.auth.backends import BaseBackend

from api.models import User

#13.24 time 31 class

class PhoneBackend(BaseBackend):

    def authenticate(self, request, username = None, password = None ,**kwargs):

        try:

            user_object=User.objects.get(phone=username)

            if user_object.check_password(password):  # to chech the password userobject_password and sending password to check both are same or not ,
                                                      # the userobject password was enctrpted by the creating time ,check_password function will help for that

                return  user_object
            else:
                return None

        except:
            return  None


    def get_user(self, user_id):  #  to return the user 
        try:
            return User.objects.get(id=user_id)

        except:
            return None
            
