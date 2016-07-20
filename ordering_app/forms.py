from django import forms

class AddOrder(forms.Form):
    customer = forms.CharField(max_length=15)
    email = forms.EmailField()
    buy = forms.CharField(max_length=20)
    byr = forms.IntegerField(min_value=0, max_value=500000)
    byn = forms.FloatField(min_value=0, max_value=50)
    comment = forms.CharField(max_length=30)

class EditOrder(forms.Form):
    customer = forms.CharField(max_length=15)
    email = forms.EmailField()
    buy = forms.CharField(max_length=20)
    byr = forms.IntegerField(min_value=0, max_value=500000)
    byn = forms.FloatField(min_value=0, max_value=50)
    comment = forms.CharField(max_length=30)