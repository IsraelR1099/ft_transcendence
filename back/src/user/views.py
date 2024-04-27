from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.middleware.csrf import get_token
from django.core.serializers import serialize

from allauth.socialaccount.models import SocialApp

import json
import logging
import os
import requests

from .models import Users, FriendRequest, FriendList
from .models import MatchHistory
from .forms import RegistrationForm, UsersAuthenticationForm, UsersUpdateForm
from .utils import get_friend_request_or_false
from .utils import generate_response, get_image_as_base64
from .utils import get_user_info
from .utils import register_42_user
from .friend_utils import get_receiver_by_username, get_receiver_by_id
from .friend_utils import validate_sender_receiver, create_friend_request
from .friend_utils import serialize_friend_request
from .friend_utils import get_serialized_friends, get_friend_request_status
from .friend_request_status import FriendRequestStatus


@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        return (JsonResponse(
            {"error": "You must be authenticated."}, status=401))
    return (JsonResponse(
        {"message": "Success"}, status=200))


def get_csrf_token(request):
    """ This function returns the csrf token. """
    token = get_token(request)
    logging.debug("token csrf is %s", token)
    return (JsonResponse({"csrf_token": token}))


def get_is_auth(request, *args, **kwargs: HttpRequest) -> JsonResponse:
    response_data = {}
    current_user = request.user
    if current_user.is_authenticated:
        response_data['status'] = "Online"
        response_data['user_id'] = request.user.pk
    else:
        response_data['status'] = "Offline"
    return (JsonResponse(response_data, encoder=DjangoJSONEncoder))


def get_google_login_url(request, *args, **kwargs: HttpRequest) -> JsonResponse:
    google_app = SocialApp.objects.get(provider="google")
    google_login_url = google_app.get_login_url(request)
    return (JsonResponse({"google_login_url": google_login_url}))


@csrf_exempt
def login_view(request, *args, **kwargs: HttpRequest) -> JsonResponse:
    context = {}
    user = request.user
    if user.is_authenticated:
        context["error"] = "You are already logged in."
        return (JsonResponse(context, encoder=DjangoJSONEncoder))
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            form = UsersAuthenticationForm(json_data)
            if form.is_valid():
                username = json_data["username"]
                password = json_data["password"]
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    context = generate_response("200", user=user)
                    return (JsonResponse(context, encoder=DjangoJSONEncoder))
                else:
                    logging.debug("user is not valid")
            else:
                context["login_form"] = form
                errors = {}
                for field, field_errors in form.errors.items():
                    errors[field] = field_errors
        except json.JSONDecodeError:
            errors = {"JSONDecodeError": "Please provide a valid JSON."}
            context = generate_response("401", error_message=errors)
            return (JsonResponse(context, encoder=DjangoJSONEncoder))
        context = generate_response("401", error_message=errors)
    return (JsonResponse(context, encoder=DjangoJSONEncoder))


@login_required
@csrf_exempt
def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        user = request.user
        logging.debug("email is %s", user.email)
        user = Users.objects.get(pk=user.pk)
        user_email = user.email
        if "42barcelona" in user_email:
            logout(request)
            user.delete()
            context = {
                    "message": "User deleted.",
                    "status": "success",
                    }
            return (JsonResponse(
                context, encoder=DjangoJSONEncoder, status=200))
        else:
            logout(request)
            context = {
                    "message": "Logout successful.",
                    "status": "success",
                    }
            return (JsonResponse(
                context, encoder=DjangoJSONEncoder, status=200))
    else:
        context = {
            "message": "Method not allowed.",
            "status": "error",
                }
    logging.debug("context in logout is %s", context)
    return (JsonResponse(context, encoder=DjangoJSONEncoder, status=401))


@csrf_exempt
def register_user(request, *args, **kwargs: HttpRequest) -> JsonResponse:
    context = {}
    user = request.user
    if user.is_authenticated:
        context["error"] = "You are already registered and logged in."
        return (JsonResponse(context, encoder=DjangoJSONEncoder, status=200))
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            logging.debug("json_data is %s", json_data)
            form = RegistrationForm(json_data)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                account = authenticate(
                        username=username, password=raw_password)
                login(request, account)
                context = generate_response("201", user=account)
                logging.debug("context on succes %s", context)
                return (JsonResponse(
                    context, encoder=DjangoJSONEncoder, status=201))
            else:
                errors = []
                for field_errors in form.errors.values():
                    errors.extend(field_errors)
                context = {"error": errors}
                return (JsonResponse(context, encoder=DjangoJSONEncoder,
                                     status=200))
        except json.JSONDecodeError:
            errors = {"error": "Please provide a valid JSON."}
            context = generate_response("401", error_message=errors)
            return (JsonResponse(
                context, encoder=DjangoJSONEncoder, status=200))
    else:
        context['error'] = "Method not allowed."
    logging.debug("context before is %s", context)
    return (JsonResponse(context, encoder=DjangoJSONEncoder, status=200))


"""     if account.profile_image:
            image_path = os.path.join(
                    settings.MEDIA_ROOT, str(account.profile_image))
            encoded_string = get_image_as_base64(image_path)
            if encoded_string:
                context['profile_image_base64'] = encoded_string
            else:
                context['profile_image_base64'] = None
        else:
            context['profile_image_base64'] = None

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        # Friend List of the authenticated user
        friends = friend_list.friends.all()
        serialized_friends = []
        for friend in friends:
            serialized_friend = {
                    "id": friend.id,
                    "username": friend.username,
                    }
            if serialized_friend:
                serialized_friends.append(serialized_friend)


 # Case 1: Request has been sent from THEM to YOU:
                # FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    # We get the id/pk of that specific friend request
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # Case 2: Request has been sent from YOU to THEM:
                # FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # Case 3: No request sent from YOU or THEM:
                # FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value


"""


@login_required
def account_view(request, *args, **kwargs):
    """
    Logic for viewing user account
        is_self -> Boolean
        is_friend -> Boolean
            -1: NO_REQUEST_SENT
            0: THEM_SENT_TO_YOU
            1: YOU_SENT_TO_THEM
    """
    context = {}
    user_id = kwargs.get("user_id")
    # if user does not exist we return a 404
    try:
        account = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        context['error'] = "User not found."
        return (JsonResponse(context, encoder=DjangoJSONEncoder, status=404))
    # if user exists we check if they are a friend
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image_base64'] = get_image_as_base64(
                account=account)
        context['friends'] = get_serialized_friends(account)
        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        friend_requests = None
        # If user is authenticated we check if they are a friend
        # If the user is authenticated and the user is not the same as the
        # account
        if user.is_authenticated and user != account:
            is_self = False
            # We check if we are friends on the friend list of the other user
            friends = account.friends.all()
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                context['request_sent'] = get_friend_request_status(
                        account=account, user=user)
        elif not user.is_authenticated:
            is_self = False
        # If you are looking at your own profile we get all the friend requests
        # that we have set to is_active to true
        else:
            try:
                friend_requests = FriendRequest.objects.filter(
                        receiver=user, is_active=True)
                friend_requests_json = serialize('json', friend_requests)
                friend_requests_dict = json.loads(friend_requests_json)
            except FriendRequest.DoesNotExist:
                friend_requests = None
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['friend_requests'] = friend_requests_dict
    # logging.debug("context in account view is %s", context)
    return (JsonResponse(context, encoder=DjangoJSONEncoder, status=200))


@csrf_exempt
@login_required
def edit_account_view(request, *arg, **kwargs):
    response_data = {}

    if not request.user.is_authenticated:
        response_data = {"error": "You must be authenticated to edit your profile."}
        return (JsonResponse(
            response_data, encoder=DjangoJSONEncoder, status=403))
    user_id = kwargs.get("user_id")
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        response_data['error'] = "User not found."
        return (JsonResponse(
            response_data, encoder=DjangoJSONEncoder, status=400))

    if user.pk != request.user.pk:
        response_data['error'] = "You cannot edit someone elses profile."
        return (JsonResponse(
            response_data, encoder=DjangoJSONEncoder, status=400))
    if request.method == "POST":
        # Extract and process the profile image
        form_data = request.POST.copy()
        if not form_data.get('email', ''):
            form_data['email'] = user.email
        if not form_data.get('username', ''):
            form_data['username'] = user.username
        form = UsersUpdateForm(
                form_data, request.FILES, instance=request.user)
        if form.is_valid():
            logging.debug("form is valid")
            # Delete the old profile image so the name is preserved
            # user.profile_image.delete()
            form.save()
            # We redirect to the same page to see the changes
            response_data['success'] = "Profile updated successfully."
            return (JsonResponse(
                response_data, encoder=DjangoJSONEncoder, status=200))
        else:
            logging.debug("form is not valid")
            form = UsersUpdateForm(
                    request.POST, instance=request.user, initial={
                                      "id": user.pk,
                                      "email": user.email,
                                      "username": user.username,
                                      "profile_image": user.profile_image,
                                      })
            error_messages = ", ".join(
                 [str(errors[0]) for errors in form.errors.values()])
            logging.debug("form.errors is %s", form.errors)
            response_data['error'] = error_messages
    else:
        logging.debug("request method is not post")
        form = UsersUpdateForm(
                initial={
                    "id": user.pk,
                    "email": user.email,
                    "username": user.username,
                    "profile_image": user.profile_image,
                    })
        error_messages = ", ".join(
                [str(errors[0]) for errors in form.errors.values()])
        response_data['error'] = error_messages
    logging.debug("response_data leaving edit: %s", response_data)
    return (JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200))


def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        # This search query looks for the q on the url.
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            # We use icontains to not take in consideration upper case and
            # lower case. filter allows us to search for different queries
            # inside our db. distinct takes care if there is multiple results
            # in our search and eliminates them, showing just one result.
            # We search for username or email
            search_results = Users.objects.filter(
                    email__icontains=search_query).filter(
                    username__icontains=search_query).distinct()
            # The structure of accounts is the followed:
            # accounts = [(User1, True(depending if they are friends or not)),
            # User2, False]
            accounts = []
            user = request.user
            if user.is_authenticated:
                # We get all the friends of the user
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append({
                        "id": account.id,
                        "username": account.username,
                        "is_friend": auth_user_friend_list.is_mutual_friend(account)
                    })
                context['accounts'] = accounts
            else:
                for account in search_results:
                    account_info = {
                            "id": account.id,
                            "username": account.username,
                            "is_friend": False,
                            }
                    accounts.append(account_info)
                context['accounts'] = accounts
        else:
            context['error'] = "Please enter a valid search query."
    else:
        context['error'] = "Please provide a valid method."
    logging.debug("context on search is %s", context)
    return (JsonResponse(context, encoder=DjangoJSONEncoder, status=200))


@csrf_exempt
@login_required
def send_friend_request(request, *args, **kwargs):
    payload = {}
    user = request.user
    logging.debug("user on send_friend_request is %s", user)
    if request.method == "POST" and user.is_authenticated:
        # The receiver_user_id must be sent by the front end
        body_data = json.loads(request.body.decode("utf-8"))
        logging.debug("body_data on send_friend_request is %s", body_data)

        if 'username' in body_data and body_data['username']:
            receiver = get_receiver_by_username(body_data['username'])
        else:
            receiver = get_receiver_by_id(body_data['receiver_user_id'])
        if receiver:
            try:
                validate_sender_receiver(user, receiver)
                create_friend_request(user, receiver)
                payload['response'] = "Friend request sent."
            except ValueError as e:
                payload['error'] = str(e)
        else:
            payload['error'] = "The specified user does not exist."
    else:
        payload['error'] = "You must be authenticated."
    logging.debug("payload on send_friend_request: %s", payload)
    return (JsonResponse(payload, encoder=DjangoJSONEncoder, status=200))


@login_required
def friend_requests(request, *args, **kwargs):
    response_data = {}
    current_user = request.user
    logging.debug("current_user on friend_requests is %s", current_user)
    if current_user.is_authenticated:
        user_id = kwargs.get("user_id")
        account = Users.objects.get(pk=user_id)
        if account == current_user:
            friend_requests = FriendRequest.objects.filter(receiver=account,
                                                           is_active=True)
            serialized_friend_requests = [
                    serialize_friend_request(request) for request in
                    friend_requests]
            response_data['friend_requests'] = serialized_friend_requests
        else:
            response_data['error'] = "That is not your account."
            logging.debug("response_data 1 on friend_requests is %s", response_data)
            return (JsonResponse(
                response_data, encoder=DjangoJSONEncoder, status=401))
    else:
        logging.debug("response_data 2 on friend_requests is %s", response_data)
        response_data['error'] = "You must be authenticated to view friend requests."
        return (JsonResponse(
            response_data, encoder=DjangoJSONEncoder, status=401))
    logging.debug("response_data 3 on friend_requests is %s", response_data)
    return (JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200))


@login_required
def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    # Found the request, Not accept it.
                    friend_request.accept()
                    payload['response'] = "Friend request accepted."
                else:
                    payload['error'] = "Friend request not found."
            else:
                payload['error'] = "That is not your request to accept."
        else:
            payload['error'] = "Unable to accept that friend request."
    else:
        payload['error'] = "You must be authenticated to accept a friend request."
    logging.debug("payload on accept_friend_request: %s", payload)
    return (JsonResponse(payload, encoder=DjangoJSONEncoder, status=200))


@csrf_exempt
def remove_friend(request, *args, **kwars):
    payload = {}
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        # The receiver_user_id must be sent by the front end
        # the receiver_user_id is the user we are removing from our friend list
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        user_id = body_data.get("receiver_user_id")
        # user_id = request.POST.get("receiver_user_id")
        logging.debug("user_id en remove friend is %s", user_id)
        if user_id:
            try:
                removee = Users.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['error'] = str(e)
        else:
            payload['error'] = "Unable to remove that friend."
    else:
        payload['error'] = "You must be authenticated to remove a friend."
    logging.debug("payload on remove_friend: %s", payload)
    return (JsonResponse(payload, encoder=DjangoJSONEncoder, status=200))


def decline_friend_request(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm it is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    # Found the request. Now decline it.
                    friend_request.decline()
                    payload['response'] = "Friend request declined."
                else:
                    payload['error'] = "Friend request not found."
            else:
                payload['error'] = "That is not your request to decline."
        else:
            payload['error'] = "Unable to decline that friend request."
    else:
        payload['error'] = "You must be authenticated to decline a friend request."
    logging.debug("payload on decline_friend_request: %s", payload)
    return (JsonResponse(payload, encoder=DjangoJSONEncoder, status=200))


@csrf_exempt
def cancel_friend_request(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        user_id = body_data.get("receiver_user_id")
        if user_id:
            receiver = Users.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                        sender=user, receiver=receiver, is_active=True)
            except FriendRequest.DoesNotExist:
                payload['error'] = "Friend request not found."
            # There should only be a single active friend request at any given
            # time.
            if len(friend_requests) > 1:
                # This is an error. There should only ever be one active friend
                # request at a time.
                for request in friend_requests:
                    request.cancel()
                payload['error'] = "Somehow you have more than one request."
            else:
                # Found the request. Cancel it.
                friend_requests.first().cancel()
                payload['response'] = "Friend request cancelled."
        else:
            payload['error'] = "Unable to cancel that friend request."
    else:
        payload['error'] = "You must be authenticated to cancel a friend request."
    logging.debug("payload on cancel_friend_request: %s", payload)
    return (JsonResponse(payload, encoder=DjangoJSONEncoder, status=200))


@login_required
def friend_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = Users.objects.get(pk=user_id)
                context['this_user'] = this_user.username
            except Users.DoesNotExist:
                context['error'] = "That user does not exist."
            try:
                friend_list = FriendList.objects.get(user=this_user)
            except FriendList.DoesNotExist:
                context['error'] = "Could not find a friend list for this user."

            # Must be friends to view a friends list
            if user != this_user:
                if not user in friend_list.friends.all():
                    context['error'] = "You must be friends to view their friends list."
                    return JsonResponse(context, encoder=DjangoJSONEncoder,
                                        status=200)

            friends = []  # [(friend1, True), (friend2, False), ...]
            image_base64 = None
            auth_user_friend_list = FriendList.objects.get(user=user)
            for friend in friend_list.friends.all():
                if friend.profile_image:
                    image_path = os.path.join(
                            settings.MEDIA_ROOT, str(friend.profile_image))
                    encoded_string = get_image_as_base64(image_path=image_path)
                    if encoded_string:
                        image_base64 = encoded_string
                    else:
                        image_base64 = None
                friends.append(({'friend_id': friend.id,
                                 'friend': friend.username,
                                 'profile_image': image_base64,
                                 'is_friend':
                                 auth_user_friend_list.is_mutual_friend(friend)}))
            context['friends'] = friends
        else:
            context['error'] = "No user id provided."
    else:
        context['error'] = "You must be authenticated to view a friends list."
    logging.debug("context on friend_list_view: %s", context)
    return JsonResponse(context, encoder=DjangoJSONEncoder, status=200)


@csrf_exempt
def auth42(request, *args, **kwargs):
    response_data = {}
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)
    code = body_data.get("code")
    if not code:
        response_data['error'] = "No code provided."
        return JsonResponse(
                response_data, encoder=DjangoJSONEncoder, status=200)
    url = 'https://api.intra.42.fr/oauth/token'
    data = {
            'grant_type': 'authorization_code',
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET'),
            'code': code,
            'redirect_uri': 'https://pong.xyz/42-auth',
            }
    logging.debug("data on 42auth is %s", data)
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        response_data = response.json()
        token_access = response_data.get('access_token')
        user_info = get_user_info(token_access)
        # We should get login, first_name, last_name, email, and image small
        if user_info:
            logging.debug("user does not exist")
            user = register_42_user(request, user_info)
            if not user:
                response_data['error'] = "Could not register user."
                return JsonResponse(
                        response_data, encoder=DjangoJSONEncoder, status=200)
            response_data = generate_response("200", user=user)
        else:
            response_data['error'] = "Could not get user info."
        logging.debug("response_data on 42auth is %s", response_data)
    except requests.exceptions.RequestException as e:
        response_data['error'] = str(e)
    logging.debug("response_data on 42auth is %s", response_data)
    return JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200)


@csrf_exempt
def delete_users_42(request, *args, **kwargs):
    if request.method == "POST":
        users_to_delete = Users.objects.filter(email__icontains="42barcelona")
        deleted_user_count = users_to_delete.count()
        users_to_delete.delete()
        response_data = {
                "message": f"Deleted {deleted_user_count} users.",
                "status": "success",
                }
        return JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200)
    else:
        response_data['error'] = "Method not allowed."
        return JsonResponse(response_data, encoder=DjangoJSONEncoder, status=405)


@csrf_exempt
@login_required
def save_match(request, *args, **kwargs):
    response_data = {}
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        winner_username = body_data.get("winner")
        loser_username = body_data.get("loser")
        room_code = body_data.get("room_code")
        game_type = body_data.get("game_type")
        if winner_username == "draw" or loser_username == "draw":
            response_data['error'] = "Cannot save a draw."
            return JsonResponse(
                    response_data, encoder=DjangoJSONEncoder, status=200)

        try:
            winner_user = Users.objects.get(username=winner_username)
            loser_user = Users.objects.get(username=loser_username)

            winner_match = MatchHistory.objects.create(
                    winner=winner_user,
                    loser=loser_user,
                    room_code=room_code,
                    game_type=game_type,
                    result='win'
                    )
            loser_match = MatchHistory.objects.create(
                    winner=winner_user,
                    loser=loser_user,
                    room_code=room_code,
                    game_type=game_type,
                    result='loss'
                    )
            winner_user.match_history.add(winner_match)
            loser_user.match_history.add(loser_match)
            response_data['response'] = "Match saved."
            return JsonResponse(
                    response_data, encoder=DjangoJSONEncoder, status=200)
        except Users.DoesNotExist:
            response_data['error'] = "User does not exist."
        except Exception as e:
            response_data['error'] = str(e)
    else:
        response_data['error'] = "You must be authenticated to save a match."
    return JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200)


@login_required
def get_match_history(request, *args, **kwargs):
    response_data = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        try:
            this_user = Users.objects.get(pk=user_id)
            match_history = this_user.match_history.all()
            serialized_match_history = []
            for match in match_history:
                serialized_match = {
                        "winner": match.winner.username,
                        "loser": match.loser.username,
                        "room_code": match.room_code,
                        "game_type": match.game_type,
                        "result": match.result,
                        "date": match.date_time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                serialized_match_history.append(serialized_match)
                response_data['winner'] = match.winner.username
                response_data['loser'] = match.loser.username
                response_data['room_code'] = match.room_code
                response_data['game_type'] = match.game_type
                response_data['result'] = match.result
                response_data['date'] = match.date_time.strftime(
                        "%Y-%m-%d %H:%M:%S")
        except Users.DoesNotExist:
            response_data['error'] = "User does not exist."
        except Exception as e:
            response_data['error'] = str(e)
    else:
        response_data['error'] = "You must be authenticated to view match history."
    return JsonResponse(response_data, encoder=DjangoJSONEncoder, status=200)
