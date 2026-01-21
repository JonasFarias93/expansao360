from django import forms


class LocationForm(forms.Form):
    location_id = forms.CharField(max_length=50)
    name = forms.CharField(max_length=200)
