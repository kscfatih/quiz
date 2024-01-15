from django import forms
from .models import Image
from .models import Medya
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class MedyaForm(forms.ModelForm):
    class Meta:
        model = Medya
        fields = ['tur', 'dosya']



class MedyaForm2(forms.ModelForm):
    dosya = forms.FileField()

    class Meta:
        model = Medya
        fields = ['dosya', 'tur']





