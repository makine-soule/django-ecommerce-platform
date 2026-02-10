from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView

from .forms import SignupForm, UpdateUserForm
from django.contrib.auth import logout
from django.shortcuts import redirect

#Login Required
from django.contrib.auth.mixins import LoginRequiredMixin

# email management
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
# Utilise pour les balises dans le mail envoyé
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
# Permet d'encoder et de decoder l'url d'envoi pour le token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#User
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

#ShippingManagement
from payment.forms import ShippingForm
from payment.models import ShippingAddress

#OrdersManagement
from payment.models import Order, OrderItem

class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("two_factor:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        #Email verification setup(template)

        current_site = get_current_site(self.request)
        subject = "Account verification email"
        message = render_to_string("registration/email-verification.html", {
            "user":user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": user_tokenizer_generate.make_token(user),
        })

        user.email_user(subject=subject, message=message)

        return redirect("email-verification-sent")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On ajoute le texte du place holder pour les deux derniers champs
        context['form'].fields['password1'].widget.attrs['placeholder'] = 'Enter your password . . .'
        context['form'].fields['password2'].widget.attrs['placeholder'] = 'Confirm your password . . .'
        # On enlève les indications qui sont sur le formulaire
        context['form'].fields['username'].help_text = ''
        context['form'].fields['password1'].help_text = ''
        context['form'].fields['password2'].help_text = ''
        return context

def logoutview(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("two_factor:login")

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"
    login_url = "two_factor:login"


class Email_verification(TemplateView):
    def get(self, *args, **kwargs):
        uidb64 = self.kwargs.get("uidb64")
        token = self.kwargs.get("token")
        unique_id = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)

        #success
        if user and user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("email-verification-success")
        #failed
        else:
            return redirect("email-verification-failed")

class Email_verification_sent(TemplateView):
    template_name = "registration/email-verification-sent.html"

class Email_verification_failed(TemplateView):
    template_name = "registration/email-verification-failed.html"

class Email_verification_success(TemplateView):
    template_name = "registration/email-verification-success.html"

#Account management

class ProfileMangement(LoginRequiredMixin, TemplateView):
    template_name = "account/profile_management.html"
    login_url = "two_factor:login"

class UpdateFormAccount(LoginRequiredMixin, UpdateView):
    form_class = UpdateUserForm
    model = User
    template_name = "account/update_user_account.html"
    login_url = "two_factor:login"
    success_url = reverse_lazy("profile-management")

    def form_valid(self, form):
        user = form.save(commit=False)

        if user.email != self.request.user.email:
            user.is_active = False
            user.save()

            #Email verification setup(template)

            current_site = get_current_site(self.request)
            subject = "Account verification email"
            message = render_to_string("registration/email-verification.html", {
                "user":user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject, message=message)
            return redirect("email-verification-sent")

        else:
            user.save()
            return redirect("profile-management")

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['username'].widget.attrs['placeholder'] = 'Enter your username . . .'
        context['form'].fields['email'].widget.attrs['placeholder'] = 'Enter your email . . .'
        context['form'].fields['username'].help_text = ''
        return context

class DeleteAccount(LoginRequiredMixin, DeleteView):
    model = User
    login_url = "two_factor:login"
    template_name = "account/delete_account_warning.html"
    success_url = reverse_lazy("two_factor:login")

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user)

#Custompasswordview
class CustomPasswordResetView(PasswordResetView):
    template_name = "password-reset/password-reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter le placeholder au champ e-mail
        context['form'].fields['email'].widget.attrs['placeholder'] = 'Enter your email ...'
        return context


#Customconfirmresetpassword
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password-reset/password-reset-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'].fields['new_password1'].widget.attrs['placeholder'] = 'Enter your password . . .'
        context['form'].fields['new_password2'].widget.attrs['placeholder'] = 'Confirm your password . . .'

        context['form'].fields['new_password1'].help_text = ''
        context['form'].fields['new_password2'].help_text = ''
        return context

class SecureView(LoginRequiredMixin, TemplateView):
    template_name = "account/secure_account.html"
    login_url = "two_factor:login"

#Shipping Management
class ManageShipping(LoginRequiredMixin, UpdateView):
    form_class = ShippingForm
    login_url = "two_factor:login"
    model = ShippingAddress
    template_name = "account/manage-shipping.html"

    def get_object(self, queryset=None):
        # Récupérer les informations de localisation de l'utilisateur actuellement connecté
        return ShippingAddress.objects.get_or_create(user=self.request.user)[0]

    def form_valid(self, form):
        shipping_user = form.save(commit=False)
        shipping_user.user = self.request.user
        shipping_user.save()
        return redirect("dashboard")


class TrackOrdersView(ListView):
    model = Order
    template_name = "account/track-orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset

class TrackOrdersDetailsView(ListView):
    model = OrderItem
    template_name = "account/orders-informations.html"
    context_object_name = "orders"

    def dispatch(self, request, *args, **kwargs):
        order_id = self.kwargs.get("order_id")
        order_item = get_object_or_404(OrderItem, order_id_id=order_id)

        # Vérifie si l'utilisateur connecté est le propriétaire de la commande
        if order_item.user != request.user:
            return redirect("dashboard")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.kwargs.get("order_id")
        queryset = queryset.filter(user=self.request.user, order_id_id=order_id)

        return queryset