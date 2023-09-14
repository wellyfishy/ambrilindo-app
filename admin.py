from django.contrib import admin
from .resources import *
from .models import *

admin.site.register(Event)
admin.site.register(Bagan)
admin.site.register(DetailBagann)
admin.site.register(BaganKategori)
admin.site.register(Atlet)
# admin.site.register(Buyer)
admin.site.register(Tatami)
admin.site.register(Jury)
admin.site.register(Score)
admin.site.register(ScoreDetail)
admin.site.register(TotalScore)
admin.site.register(AdminTatami)
admin.site.register(DetailMedali)
admin.site.register(Statistic)



