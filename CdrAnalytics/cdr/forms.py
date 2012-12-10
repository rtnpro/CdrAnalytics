from django import forms


class MaxConCallsAnalyticsForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
