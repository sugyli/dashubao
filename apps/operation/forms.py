from django import forms

from operation import models as operation_import


class UserAskForm(forms.ModelForm):

    class Meta:
        model = operation_import.UserAsk
        fields = ['message']



class AddUserFavForm(forms.Form):
    bookid = forms.CharField(required=True)
    chapterid = forms.CharField(required=True)