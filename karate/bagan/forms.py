from attr import fields
from django import forms

from .models import Atlet

class AtletForm(forms.ModelForm):
    class Meta:
        model = Atlet
        fields = ('nama_atlet', 
                  'jenis_event', 
                  'jenis_kelamin', 
                  'perguruan', 
                  'perwakilan', 
                  'tempat_lahir', 
                  'tanggal_lahir',
                  'usia_atlet',
                  'berat_badan',)
