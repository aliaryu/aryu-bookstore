from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserInformationUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "birth_date", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold ms-1",
            "placeholder": "نام",
            "type": "text",
        })
        self.fields["last_name"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold me-1",
            "placeholder": "نام خانوادگی",
            "type": "text",
        })
        self.fields["birth_date"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold",
            "placeholder": "تاریخ تولد - مثال: 1-1-2024",
            "type": "text",
        })
        self.fields["username"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold ms-1",
            "placeholder": "نام کاربری",
            "type": "text",
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control bg-transparent place-holder-grey fw-bold me-1",
            "placeholder": "ایمیل",
            "type": "email",
        })
