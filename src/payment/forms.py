from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "email",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        ]
        labels = {
            "full_name": "Full Name :",
            "email": "Email :",
            "address1": "Address 1 :",
            "address2": "Address 2 :",
            "city": "City :",
            "state": "State :",
            "zipcode": "Zipcode :",
        }

        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter your full name . . . *", "class": "validate"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email . . . *", "class": "validate"}),
            "address1": forms.TextInput(attrs={"placeholder": "Enter your address 1 . . . *", "class": "validate"}),
            "address2": forms.TextInput(attrs={"placeholder": "Enter your address 2 . . . *", "class": "validate"}),
            "city": forms.TextInput(attrs={"placeholder": "Enter your city . . . *", "class": "validate"}),
            "state": forms.TextInput(attrs={"placeholder": "Enter your state (Optional) . . ."}),
            "zipcode": forms.TextInput(attrs={"placeholder": "Enter your zipcode (Optional) . . ."})
        }
