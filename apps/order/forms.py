from django import forms
from apps.user.models import Address




class PaymentForm(forms.Form):
    discount_code = forms.CharField(max_length=10, required=False)
    address = AddressModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields["address"].queryset = Address.objects.filter(user=user)
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