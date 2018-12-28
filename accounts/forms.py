from captcha.fields import CaptchaField
from django import forms


class UploadPhotoForm(forms.Form):
    photo = forms.ImageField()


class CaptchaForm(forms.Form):
    captcha = CaptchaField()
