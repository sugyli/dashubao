from django import forms


class AddUserFavForm(forms.Form):
    bookid = forms.CharField(required=True)
    chapterid = forms.CharField(required=True)



