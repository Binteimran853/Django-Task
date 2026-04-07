from django import forms

from accounts.models import User


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["address", "phone"]
        widgets = {
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Enter delivery address",
                }
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone number"}
            ),
        }
