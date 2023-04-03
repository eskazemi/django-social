from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views import View

from home.models import Post
from .forms import (
    RegisterForm,
    LoginForm,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import (
    login,
    authenticate,
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd["username"],
                                     email=cd["email"],
                                     password=cd["password"])
            messages.success(request, "you registered successfully", 'success')
            return redirect('home:home')
        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"],
                                password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully",
                                 "success")
                return redirect('home:home')
            else:
                messages.error(request, "username or password is wrong",
                               'danger')
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    login_url = '/account/login'

    def get(self, request):
        logout(request)
        messages.success(request, "logout user successfully", 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, 'account/profile.html', {"user": user, "posts": posts})



class UserResetPasswordView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset.html'



class UserPasswordResetDownView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'



class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
