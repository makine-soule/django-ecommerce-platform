from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("signup/", views.SignupView.as_view(), name="signup-user"),
    path("logout/", views.logoutview, name="logout-user"),

    #Registration activation email
    path("email-verification/<str:uidb64>/<str:token>/", views.Email_verification.as_view(), name="email-verification"),
    path("email-verification-sent/", views.Email_verification_sent.as_view(), name="email-verification-sent"),
    path("email-verification-success/", views.Email_verification_success.as_view(), name="email-verification-success"),
    path("email-verification-failed/", views.Email_verification_failed.as_view(), name="email-verification-failed"),

    #Management profil
    path("profile-management/", views.ProfileMangement.as_view(), name="profile-management"),
    path("delete-account/", views.DeleteAccount.as_view(), name="delete-management"),
    path("update-account/", views.UpdateFormAccount.as_view(), name="update-account"),
    path("secure-account/", views.SecureView.as_view(), name="secure-account"),

    #Reset password
    # Submit our email form
    path("reset-password/", auth_views.PasswordResetView.as_view(template_name="password-reset/password-reset.html"), name="reset-password"),

    # A success message stating that an email was sent to reset our password
    path("reset-password-sent/", auth_views.PasswordResetDoneView.as_view(template_name="password-reset/password-reset-sent.html"), name="password_reset_done"),

    # Send a link to our email... So we can reset our password
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password-reset/password-reset-form.html"), name="password_reset_confirm"),

    # Show a success message stating that our password was changed
    path("reset-password-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password-reset/password-reset-complete.html"), name="password_reset_complete"),

    # Manage shipping url
    path("manage-shipping/", views.ManageShipping.as_view(), name="manage-shipping"),

    #track orders
    path("track-orders/", views.TrackOrdersView.as_view(), name="track-orders"),
    #track orders in details
    path("track-orders-detail/<str:order_id>/", views.TrackOrdersDetailsView.as_view(), name="track-orders-detail")
]