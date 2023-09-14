from django.db import models


class Perguruan(models.Model):
    id_perguruan = models.IntegerField(primary_key=True)
    nama_perguruan = models.CharField(max_length=50)
    
class Utusan(models.Model):
    id_utusan = models.IntegerField(primary_key=True)
    nama_utusan = models.CharField(max_length=50)
    
class Kelamin(models.Model):
    id_kelamin = models.IntegerField(primary_key=True)
    nama_kelamin = models.CharField(max_length=50)

# Junior, Senior, etc
class Kelompok(models.Model):
    id_kelompok = models.IntegerField(primary_key=True)
    judul_kelompok = models.CharField(max_length=50)

# Bagan Kata / Kumite
class Kategori(models.Model):
    id_kategori = models.IntegerField(primary_key=True)
    judul_kategori = models.CharField(max_length=50)

# Berat badan
class Tanding(models.Model):
    id_tanding = models.IntegerField(primary_key=True)
    judul_tanding = models.CharField(max_length=50)
    
class Atlet(models.Model):
    id_atlet = models.IntegerField(primary_key=True)
    nama_atlet = models.CharField(max_length=50)
    id_utusan = models.ForeignKey(Utusan, on_delete=models.SET_NULL, null=True, blank=True)
    id_perguruan = models.ForeignKey(Perguruan, on_delete=models.SET_NULL, null=True, blank=True)
    id_kelamin = models.ForeignKey(Kelamin, on_delete=models.SET_NULL, null=True, blank=True)
    
# Kata Perorangan Putra,
class BaganKata(models.Model):
    id_bagan = models.IntegerField(primary_key=True)
    judul_bagan = models.CharField(max_length=50)

# Kumite Senior, Junior, etc
class BaganKumite(models.Model):
    id_bagan = models.IntegerField(primary_key=True)
    judul_bagan = models.CharField(max_length=50)
    
# # Liga BKC, O2SN, etc
# class Event(models.Model):
#     id_event = models.AutoField(primary_key=True)
#     judul_event = models.CharField(max_length=50)
#     foto_event = models.ImageField(null=True, blank=True, upload_to="images/event/")
#     tanggal_tanding = models.DateTimeField()
#     tanggal_selesai = models.DateTimeField()
#     tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.judul_event
    

