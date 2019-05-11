from django import forms

# our new form
class ContactForm(forms.Form):
    locFrom = forms.CharField(required=True)
    locTo = forms.CharField(required=True)
    dateFrom = forms.CharField(required=True)
    dateTo = forms.CharField(required=True)

class ContactFormHotel(forms.Form):
    location = forms.CharField(required=True)
    dateFrom = forms.CharField(required=True)
    dateTo = forms.CharField(required=True)

class ContactFormRental(forms.Form):
    locFrom = forms.CharField(required=True)
    locTo = forms.CharField(required=True)
    dateFrom = forms.CharField(required=True)
    dateTo = forms.CharField(required=True)
