from django.contrib.auth.views import LoginView
from django.urls import path

from .forms import LoginForm
from .views import ProfileUpdateView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    # Takes priority over django.contrib.auth.urls, which is included after this.
    path("login/", LoginView.as_view(authentication_form=LoginForm), name="login"),
]
