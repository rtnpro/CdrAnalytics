from django import forms


class DateRangeForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()


class DateTimeRangeForm(forms.Form):
    from_time = forms.DateTimeField()
    to_time = forms.DateTimeField()
