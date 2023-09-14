from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

class Statistic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("dashboard", kwargs={"slug": self.slug})

    @property
    def data(self):
        return self.dataitem_set.all()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    owner = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.owner}: {self.value}"

class Jury(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.id_user.username
    
class AdminTatami(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  

    def __str__(self):
        return self.id_user.username
    
class ScoreDetail(models.Model):
    id_scoredetail = models.AutoField(primary_key=True)
    id_jury = models.ManyToManyField(Jury, blank=True)
    jury_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    nama = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    tertinggi = models.BooleanField(null=True, blank=True)
    terendah = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f'Score Detail {self.jury_score} {self.number}'
    
class TotalScore(models.Model):
    id_totalscore = models.AutoField(primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
class Score(models.Model):
    id_score = models.AutoField(primary_key=True)
    juri_score = models.ManyToManyField(ScoreDetail, blank=True)
    id_totalscore = models.ManyToManyField(TotalScore, blank=True)
    
    def __str__(self):
        return f'Score {self.pk}'
    
class Atlet(models.Model):
    JENIS_KELAMIN = (
        ('putra', 'Putra'),
        ('putri', 'Putri'),
    )
    JENIS_EVENT = (
        ('internal', 'Internal'),
        ('external', 'External'),
    )
    id_atlet = models.AutoField(primary_key=True)
    nama_atlet = models.CharField(max_length=50, null=True, blank=True)
    jenis_event = models.CharField(max_length=10, choices=JENIS_EVENT, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN, null=True, blank=True)
    perguruan = models.CharField(max_length=50, null=True, blank=True)
    perwakilan = models.CharField(max_length=50, null=True, blank=True)
    nomor_tanding = models.CharField(max_length=50, null=True, blank=True)
    tipe = models.CharField(max_length=50, null=True, blank=True)
    id_score = models.ManyToManyField(ScoreDetail, blank=True)
    
    def __str__(self):
        return self.nama_atlet
    
class Tatami(models.Model):
    id_tatami = models.AutoField(primary_key=True)
    tatami = models.CharField(max_length=50)
    number = models.IntegerField(null=True, blank=True)
    id_jury = models.ManyToManyField(Jury, blank=True)
    penilaian = models.BooleanField(default=False)
    admin = models.OneToOneField(AdminTatami, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.tatami
    
    def delete(self, *args, **kwargs):
        juries = self.id_jury.all()

        self.admin.id_user.delete()

        for jury in juries:
            jury.id_user.delete()

        super(Tatami, self).delete(*args, **kwargs)
    
class BaganKategori(models.Model):
    TIPE = (
        ('perorangan', 'Perorangan'),
        ('beregu', 'Beregu')
    )
    id_kategori = models.AutoField(primary_key=True)
    datetimekategori = models.DateTimeField(default=datetime.now)
    id_atlet = models.ManyToManyField(Atlet, blank=True)
    judul_kategori = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tipe = models.CharField(choices=TIPE, max_length=10,blank=True, null=True)
    tatami_nomor_tanding = models.ForeignKey(Tatami, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.judul_kategori
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.judul_kategori}-{self.datetimekategori.strftime('%Y%m%d%H%M%S')}")
        super().save(*args, **kwargs)
    
class DetailBagann(models.Model):
    ROUND = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    id_detailbagan = models.AutoField(primary_key=True)
    id_atlet = models.ManyToManyField(Atlet, blank=True)
    id_score = models.ManyToManyField(Score, blank=True)
    round = models.IntegerField(choices=ROUND, null=True, blank=True)
    kata1 = models.CharField(max_length=50, null=True, blank=True)
    kata2 = models.CharField(max_length=50, null=True, blank=True)
    peserta1 = models.BooleanField(default=False)
    peserta2 = models.BooleanField(default=False)
    peserta1_telahdinilai = models.BooleanField(default=False)
    peserta2_telahdinilai = models.BooleanField(default=False)
    timer_status = models.BooleanField(default=False)
    timer_reset = models.BooleanField(default=False)
    grup = models.BooleanField(default=False)
    penilaian = models.BooleanField(default=False)
    dinilai = models.BooleanField(default=False)
    id_tatami = models.OneToOneField(Tatami, on_delete=models.SET_NULL, null=True, blank=True)
    id_scoredetail = models.ManyToManyField(ScoreDetail, blank=True)
    tampilkan = models.BooleanField(default=False)
    group_tanding = models.IntegerField(null=True, blank=True)
    medali = models.BooleanField(default=False)
    merah = models.BooleanField(default=False)
    biru = models.BooleanField(default=False)

    def __str__(self):
        if self.id_atlet:
            return f'{self.id_atlet.first()}'
        elif not self.id_atlet:
            return f'Detail Bagan {self.id_detailbagan}'
        else:
            return f'Detail Bagan'

class DetailMedali(models.Model):
    nama = models.CharField(null=True, blank=True, max_length=50)
    id_detailbagan = models.ForeignKey(DetailBagann, null=True, blank=True, on_delete=models.CASCADE)
    id_atlet = models.ForeignKey(Atlet, null=True, blank=True, on_delete=models.SET_NULL)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nama 
    
class Bagan(models.Model):
    STATUS_PERTANDINGAN =  (
        ('S', 'Selesai'),
        ('P', 'Pending'),
    )
    STATUS_KATEGORI = (
        ('kata', 'kata'),
        ('kumite', 'kumite'),
    )
    GRUP_KATA = (
        ('perorangan', 'Perorangan'),
        ('beregu', 'Beregu'),
    )
    JENIS_KELAMIN = (
        ('putra', 'Putra'),
        ('putri', 'Putri'),
    )
    JENIS_EVENT = (
        ('internal', 'Internal'),
        ('external', 'External'),
    )
    TIPE = (
        ('ranking', 'Ranking'),
    )
    id_bagan = models.AutoField(primary_key=True)
    judul_bagan = models.CharField(max_length=100)
    jenis_event = models.CharField(max_length=10, choices=JENIS_EVENT, null=True, blank=True)
    id_detailbagan = models.ManyToManyField(DetailBagann, blank=True)
    tanggal_tanding = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_PERTANDINGAN, default='P')
    kategori = models.CharField(max_length=6, choices=STATUS_KATEGORI, null=True, blank=True)
    grup_kata = models.CharField(max_length=50, choices=GRUP_KATA, null=True, blank=True)
    kategori_kata = models.ManyToManyField(BaganKategori, blank=True)
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN, null=True, blank=True)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tipe = models.CharField(max_length=10, choices=TIPE, null=True, blank=True)
    tatami = models.ForeignKey(Tatami, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.judul_bagan
    
    def delete(self, *args, **kwargs):
        detailbagans = self.id_detailbagan.all()

        for detailbagan in detailbagans:
            detailbagan.id_scoredetail.all().delete()
            scores = detailbagan.id_score.all()
            
            for score in scores:
                score.id_totalscore.all().delete()

            detailbagan.id_score.all().delete()

        self.id_detailbagan.all().delete()

        super(Bagan, self).delete(*args, **kwargs)
    
class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    id_bagan = models.ManyToManyField(Bagan, blank=True)
    judul_event = models.CharField(max_length=50)
    foto_event = models.ImageField(null=True, blank=True, upload_to="images/event/")
    tanggal_tanding = models.DateTimeField()
    tanggal_selesai = models.DateTimeField()
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    id_atlet = models.ManyToManyField(Atlet, blank=True)
    bagan_kategori = models.ManyToManyField(BaganKategori, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    id_tatami = models.ManyToManyField(Tatami, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul_event)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.judul_event
