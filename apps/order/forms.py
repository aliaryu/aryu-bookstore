from apps.user.models import Address
from apps.discount.models import Discount
from apps.product.models import Book
from .models import Order, OrderBook
from django import forms
from django.db import transaction



class AddressModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.get_province_display()} - {obj.postal_code}"


class PaymentForm(forms.Form):
    discount_code = forms.CharField(max_length=10, required=False)
    address = AddressModelChoiceField(queryset=None)

    def __init__(self, user, cookie={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.cookie = cookie
        if self.user.is_authenticated:
            self.fields["address"].queryset = Address.objects.filter(user=self.user)
        else:
            self.fields["address"].choices = []
        
        self.fields["address"].choices = list(self.fields["address"].choices)[1:]
        self.fields["address"].widget.attrs.update({
            "class": "form-select mt-2",
            "required": True,
        })

        self.fields["discount_code"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold mt-2",
            "placeholder": "کد تخفیف دارید؟",
            "type": "text"
        })

    def clean_discount_code(self):
        discount_code = self.cleaned_data["discount_code"]
        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
                self.discount = discount
            except Discount.DoesNotExist:
                raise forms.ValidationError("کد تخفیف نا معتبر است.")
        return discount_code
    
