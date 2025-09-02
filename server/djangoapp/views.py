# Required imports 
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import logging

logger = logging.getLogger(__name__)

# -------------------------------
# Login View
# -------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"status": "Failure", "message": "Invalid credentials"}, status=401)

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse({"status": "Failure", "message": "Invalid request"}, status=400)

    return JsonResponse({"status": "Failure", "message": "POST request required"}, status=405)

# -------------------------------
# Logout View
# -------------------------------
@csrf_exempt
def logout_user(request):
    if request.method in ["POST", "GET"]:
        try:
            username = request.user.username if request.user.is_authenticated else ""
            logout(request)
            return JsonResponse({"userName": ""})
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return JsonResponse({"status": "Failure", "message": "Logout failed"}, status=400)

    return JsonResponse({"status": "Failure", "message": "POST or GET request required"}, status=405)

@csrf_exempt
@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)