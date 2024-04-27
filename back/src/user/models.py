from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q

import os


class MyUsersManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
                email=self.normalize_email(email),
                username=username,
                )
        user.set_password(password)
        user.save(using=self._db)
        return (user)


def get_profile_image_filepath(self, filename):
    return ('profile_images/' + str(self.pk) + '/profile_image.png')


def get_default_profile_image():
    return ("profile_images/default_profile_image.png")


class MatchHistory(models.Model):
    OUTCOME_CHOICES = (
            ('win', 'win'),
            ('loss', 'loss'),
            ('draw', 'draw'),
            )
    winner = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="winner")
    loser = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loser")
    game_type = models.CharField(max_length=64)
    room_code = models.CharField(max_length=64)
    result = models.CharField(max_length=4, choices=OUTCOME_CHOICES)
    date_time = models.DateTimeField(auto_now_add=True)


class Users(AbstractBaseUser):
    first_name          = models.CharField(max_length=64)
    last_name           = models.CharField(max_length=64)
    birth_date          = models.DateTimeField(default = timezone.now)
    username            = models.CharField(max_length=64, unique=True)
    email               = models.EmailField(max_length=100, verbose_name="email", unique=True)
    created_date_time   = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active           = models.BooleanField(default=True)
    profile_image = models.FileField(max_length=500, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    friends             = models.ManyToManyField("Users", blank=True)
    hide_email          = models.BooleanField(default=True)
    match_history       = models.ManyToManyField("MatchHistory", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    # profile_image       = models.ImageField(max_length=500, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

    objects = MyUsersManager()

    def __str__(self):
        return (f"{self.username}")

    # This function substrates the name of the image from the user profile
    # image and sets it as profile_image name
    def get_profile_image_filename(self):
        return (str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):])


class FriendList(models.Model):
    user        = models.OneToOneField(
                    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends     = models.ManyToManyField(
                    settings.AUTH_USER_MODEL, blank=True, related_name="user_friends")

    def __str__(self):
        return (f"{self.user.username}")

    def add_friend(self, account):
        """
        Add a new friend.
        If the account is not in our friendlist then we add that friend
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Remove a friend.
        If the account is in our friendlist then we remove them
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_friends_list = self  # person terminating the friendship
        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)
        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return (True)
        return (False)


class FriendRequest(models.Model):
    """
    1. Sender
    -- The person sending the friend request
    2. Receiver
    -- The person receiving the friend request
    """
    sender      = models.ForeignKey(
                    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver    = models.ForeignKey(
                    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active   = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.sender.username}")

    def accept(self):
        """
        Accept a friend request.
        Update both SENDER and RECEIVER friend lists.
        """

        # Update receiver's friend request status
        receiver_request = FriendRequest.objects.filter(
                Q(sender=self.sender, receiver=self.receiver) |
                Q(sender=self.receiver, receiver=self.sender)
                ).first()
        if receiver_request:
            receiver_request.is_active = False
            receiver_request.save()

        # Update friend lists
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request.
        It is "declined" by setting is_active to False.
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request.
        This is when the sender decides to cancel their friend request.
        This is only different with respect to "declining" through notification
        is generated.
        """
        self.is_active = False
        self.save()
