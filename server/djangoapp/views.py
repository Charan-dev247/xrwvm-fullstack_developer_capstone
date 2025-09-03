# views.py

# Required imports 
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import logging
from .models import CarMake, CarModel
from .populate import initiate  # import initiate from populate.py

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

# -------------------------------
# Registration View
# -------------------------------
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = User.objects.filter(username=username).exists()

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# -------------------------------
# Get Cars View
# -------------------------------
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})