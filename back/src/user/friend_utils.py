# Description: This file contains utility functions for the friend app.
from django.conf import settings

from .models import Users, FriendRequest
from .models import FriendList
from .utils import get_image_as_base64, get_friend_request_or_false
from .friend_request_status import FriendRequestStatus

import os


def get_receiver_by_username(username):
    try:
        receiver = Users.objects.get(username=username)
        return receiver
    except Users.DoesNotExist:
        return None


def get_receiver_by_id(user_id):
    try:
        receiver = Users.objects.get(pk=user_id)
        return receiver
    except Users.DoesNotExist:
        return None


def validate_sender_receiver(sender, receiver):
    if sender == receiver:
        raise ValueError("Cannot send friend request to yourself.")

    friend_requests = FriendRequest.objects.filter(
            sender=sender, receiver=receiver)
    for request in friend_requests:
        if request.is_active:
            raise ValueError("You already sent them a friend request.")


def create_friend_request(sender, receiver):
    friend_request = FriendRequest(sender=sender, receiver=receiver)
    friend_request.save()


def serialize_friend_request(request):
    sender_username = request.sender.username
    receiver_username = request.receiver.username
    sender_profile_image = ""

    if request.sender.profile_image:
        image_path = os.path.join(
                settings.MEDIA_ROOT, str(request.sender.profile_image))
        encoded_string = get_image_as_base64(image_path=image_path)
        if encoded_string:
            sender_profile_image = encoded_string
        else:
            sender_profile_image = ""
    else:
        sender_profile_image = ""

    return ({
        "pk": request.pk,
        "sender": sender_username,
        "receiver": receiver_username,
        "sender_profile_image": sender_profile_image,
        "is_active": request.is_active
    })


def get_serialized_friends(account):
    try:
        friend_list = FriendList.objects.get(user=account)
    except FriendList.DoesNotExist:
        friend_list = FriendList(user=account)
        friend_list.save()
    # Friend list of the authenticated user
    friends = friend_list.friends.all()
    serialized_friends = []
    for friend in friends:
        serialized_friend = {
                "id": friend.id,
                "username": friend.username,
                }
        if serialized_friend:
            serialized_friends.append(serialized_friend)
    return serialized_friends


def get_friend_request_status(account, user):
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    # Case 1: Request has been sent from THEM to YOU:
    # FriendRequestStatus.THEM_SENT_TO_YOU
    # Case 2: Request has been sent from YOU to THEM:
    # FriendRequestStatus.YOU_SENT_TO_THEM
    # Case 3: No request sent:
    # FriendRequestStatus.NO_REQUEST_SENT
    if get_friend_request_or_false(sender=account, receiver=user) != False:
        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
    elif get_friend_request_or_false(sender=user, receiver=account) != False:
        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
    else:
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    return request_sent
