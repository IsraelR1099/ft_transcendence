from django.conf import settings
from django.contrib.auth import authenticate, login

import base64
import logging
import os
import requests
import secrets
import string

from .models import FriendRequest
from .forms import UsersAuthenticationForm, RegistrationForm


def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(
                sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False


def generate_response(status, user=None, error_message=None, tokens=None):
    response = {}

    # Login
    if status == "200":
        if user:
            response["code"] = status
            response["id"] = user.id
            response["username"] = user.username
            response["email"] = user.email
            response["status"] = "online"

            if tokens:
                access_token = tokens.get("access", "")
                refresh_token = tokens.get("refresh", "")

                # Access token info
                if access_token:
                    response["token_access"] = access_token

                # Refresh token info
                if refresh_token:
                    response["token_refresh"] = refresh_token

    # Register
    elif status == "201":
        if user:
            response["code"] = status
            response["id"] = user.id
            response["username"] = user.username
            response["email"] = user.email
            response["status"] = "online"
            response["created_at"] = user.created_date_time.isoformat()

            if tokens:
                access_token = tokens.get("access", "")
                refresh_token = tokens.get("refresh", "")

                # Access token info
                if access_token:
                    response["token_access"] = access_token

                # Refresh token info
                if refresh_token:
                    response["token_refresh"] = refresh_token

    elif status == "401":
        if error_message:
            response["code"] = status
            response["error"] = error_message
    return (response)


def get_image_as_base64(account=None, image_path=None):
    """
    Convert the image at the given path to Base64
    """

    logging.debug(f"Account: {account}")
    logging.debug(f"Image path: {image_path}")
    if account:
        logging.debug("I am using account")
        if account.profile_image:
            image_path = os.path.join(
                    settings.MEDIA_ROOT, str(account.profile_image))
        else:
            return (None)
    elif image_path:
        if not os.path.exists(image_path):
            logging.debug(f"File not found: {image_path}")
            return (None)
    else:
        raise ValueError("Either account or image_path must be provided")

    try:
        with open(image_path, "rb") as img_file:
            enconded_string = base64.b64encode(
                    img_file.read()).decode("utf-8")
        return (enconded_string)
    except FileNotFoundError:
        logging.debug(f"File not found: {image_path}")
        return (None)


def process_profile_image(profile_image_data):
    decoded_image_data = base64.b64decode(profile_image_data)
    return (decoded_image_data)


def save_image_to_folder(image_data, user_id):
    folder_path = f"media_cdn/profile_images/{user_id}"
    os.makedirs(folder_path, exist_ok=True)
    image_path = f"{folder_path}/profile_image.png"

    with open(image_path, "wb") as f:
        f.write(image_data)

    return (image_path)


def get_user_info(access_token):
    url = 'https://api.intra.42.fr/v2/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_info = response.json()
        login = user_info.get('login')
        first_name = user_info.get('first_name')
        last_name = user_info.get('last_name')
        email = user_info.get('email')
        image = user_info.get('image', {})
        small_image_url = None
        for i in image.keys():
            for j in image[i]:
                if j == 'small':
                    small_image_url = image[i][j]
                    break
        password = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for i in range(20))
        user_info_dict = {
            'username': login,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'profile_image': small_image_url
        }
        logging.debug("user_info_dict: %s", user_info_dict)
        return user_info_dict
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting user info: {e}")
        return None


def auth_42_user(request, user_info, instance):
    try:
        form = UsersAuthenticationForm(
                user_info)
        if form.is_valid():
            username = user_info.get('username')
            password = user_info.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return user
            else:
                return None
        else:
            logging.error(f"Error authenticating 42 user: {form.errors}")
            return None
    except Exception as e:
        logging.error(f"Error authenticating 42 user: {e}")
        return None


def register_42_user(request, user_info):
    try:
        user_info['password1'] = user_info['password']
        user_info['password2'] = user_info['password']
        form = RegistrationForm(user_info)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return user
        else:
            return None
    except Exception as e:
        logging.error(f"Error registering 42 user: {e}")
        return None

    return None
