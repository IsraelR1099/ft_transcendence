from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("account/<int:user_id>/", views.account_view, name="view"),
        path("account/<int:user_id>/edit/", views.edit_account_view, name="edit"),
        path("auth42/", views.auth42, name="auth42"),
        path("delete_users_42/", views.delete_users_42, name="delete_users_42"),
        path("friend_list/<int:user_id>/", views.friend_list_view, name="friend-list"),
        path("friend_remove/", views.remove_friend, name="remove-friend"),
        path("friend_request/", views.send_friend_request, name="friend-request"),
        path("friend_request/<int:user_id>/", views.friend_requests, name="friend-requests"),
        path("match_history/<int:user_id>/", views.get_match_history,
             name="match-history"),
        path("get_is_auth/", views.get_is_auth, name="get-is-auth"),
        path("get_google_login_url/", views.get_google_login_url, name="get-google-login-url"),
        path("accept_friend_request/<int:friend_request_id>/",
             views.accept_friend_request, name="accept-friend-request"),
        path("decline_friend_request/<int:friend_request_id>/",
             views.decline_friend_request, name="decline-friend-request"),
        path("get_csrf_token/", views.get_csrf_token, name="get-csrf-token"),
        path("login/", views.login_view, name="login"),
        path("logout/", views.logout_view, name="logout"),
        path("register/", views.register_user, name="register"),
        path("save_match/", views.save_match, name="save-match"),
        path("search/", views.account_search_view, name="search"),


        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
            name='password_change_done'),

        path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
            name='password_change'),

        path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/password_reset_confirm.html'
            ), name='password_reset_confirm'),
        path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html', html_email_template_name='password_reset/password_reset_email.html', email_template_name='password_reset/password_reset_email.html'), name='password_reset'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
        path("<int:user_id>/accept_friend_request/", views.accept_friend_request, name="accept_friend_request"),
        ]
