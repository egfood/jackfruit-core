from django import forms
from django.forms import widgets
from apps.farmer.models import feedback


class EstimateFeedbackForm(forms.ModelForm):

    class Meta:
        model = feedback.FarmerFeedback
        fields = ('feedback',)
        widgets = {"feedback": widgets.Textarea(attrs={"id": "feedbackPopup"}),}
