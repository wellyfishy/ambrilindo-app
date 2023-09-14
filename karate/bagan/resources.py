from import_export import resources
from .models import Atlet

class AtletResource(resources.ModelResource):
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

