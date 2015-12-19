from django.contrib.auth import authenticate
from django.contrib.auth import logout


def authUser(username,password):
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return "success" #success
        else:
            return "inactive" #user not active
    else:
        # the authentication system was unable to verify the username and password
        return "invalid" #invalid login

def logoutSession(request):
    logout(request)
