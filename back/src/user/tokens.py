# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import get_user_model

# User = get_user_model()


#def create_jwt_pair_for_user(user: User) -> dict:
#     refresh = RefreshToken.for_user(user)

#     tokens = {
#            "access": str(refresh.access_token),
#            "access_expires_at": refresh.access_token['exp'],
#            "refresh": str(refresh),
#            "refresh_expires_at": refresh['exp']
#        }
#    return (tokens)
