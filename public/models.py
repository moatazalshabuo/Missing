# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User

# Model for the Missing Person
class MissingPerson(models.Model):
    GENDER_CHOICES = {
        'M': 'ذكر',
        'F': 'أنثى'
    }
    Status_CHOICES = {
    '0':'في انتظار',
    '1':'مفقود',
    '2':'تم العثور',
    '3':'رفض'
    }
    first_name = models.CharField(max_length=255, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=255, verbose_name="اسم العائلة")
    birth_date = models.DateField(verbose_name="تاريخ الميلاد")
    gender = models.CharField(max_length=1, choices=[
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ], verbose_name="الجنس")
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الطول")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الوزن")
    hair_color = models.CharField(max_length=255, verbose_name="لون الشعر")
    eye_color = models.CharField(max_length=255, verbose_name="لون العينين")
    distinguishing_marks = models.TextField(blank=True, null=True, verbose_name="علامات مميزة")
    last_seen_date = models.DateTimeField(verbose_name="تاريخ آخر مرة شوهد فيها")
    Region = models.CharField(max_length=30,blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    health_conditions = models.TextField(blank=True, null=True, verbose_name="الحالة الصحية")  
    last_seen_clothing = models.TextField(blank=True, null=True, verbose_name="الملابس عند الاختفاء")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="صورة حديثة")
    status = models.CharField(max_length=255,choices=(('0', 'في انتظار'),
        ('1', 'مفقود'),
        ('2', 'تم العثور'),
        ('3', 'رفض')),default=0)
    user = models.ForeignKey(User,blank=True,null=True, related_name='my_report',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def get_birt_day(self):
        year = datetime.date.today().year - self.birth_date.year
        return year
    def get_gender(self):
        return self.GENDER_CHOICES[self.gender]
    def get_status(self):
        return self.Status_CHOICES[self.status]
# Model for the Person Reporting the Missing Person

class Reporter(models.Model):
    missing_person = models.OneToOneField(MissingPerson, on_delete=models.CASCADE, verbose_name="المفقود")
    user = models.ForeignKey(User,related_name='user_report',on_delete=models.CASCADE,blank=True, null=True)
    first_name = models.CharField(max_length=50, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=50, verbose_name="اسم العائلة")
    relationship_to_missing = models.CharField(max_length=100, verbose_name="العلاقة بالمفقود")
    phone_number = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    address = models.CharField(max_length=200, verbose_name="عنوان السكن")
    report_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ البلاغ")
    additional_info = models.TextField(blank=True, null=True, verbose_name="معلومات إضافية")

    def __str__(self):
        return f'{self.first_name} {self.last_name} reporting {self.missing_person}'

class ReportInformation(models.Model):
    missing_person = models.ForeignKey(MissingPerson,related_name='info',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_info',on_delete=models.CASCADE,blank=True, null=True)
    phone = models.CharField(max_length=12,blank=True, null=True)
    status = models.CharField(max_length=20,verbose_name='الحالة',choices=(('تم العثور','تم العثور'),('شوهد','شوهد')))
    status_of_report = models.IntegerField(default=0)
    additional_info = models.TextField(blank=True, null=True, verbose_name="معلومات إضافية")
    there_is_loc = models.BooleanField(default=False)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.user.username
    
class FoundPersonDetails(models.Model):
    person = models.OneToOneField(MissingPerson, on_delete=models.CASCADE, related_name="found_person_details")
    found_date = models.DateField(verbose_name="تاريخ العثور")
    found_location_lat = models.FloatField(verbose_name="خط العرض لمكان العثور",blank=True, null=True)
    found_location_lng = models.FloatField(verbose_name="خط الطول لمكان العثور",blank=True, null=True)
    current_health_status = models.CharField(max_length=150,verbose_name="الحالة الصحية الحالية")
    state = models.CharField(max_length=50,verbose_name='المنطقة',blank=True, null=True)
    other_detiles = models.TextField(verbose_name='تفاصيل اخرى')

    def __str__(self):
        return f'Found details for {self.person.first_name} {self.person.last_name}'
    
class sendingEmail(models.Model):
    person = models.ForeignKey(MissingPerson,on_delete=models.CASCADE,related_name='send_miss')
    user = models.ForeignKey(User,related_name='user_send',on_delete=models.CASCADE)
    