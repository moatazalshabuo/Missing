from django.conf import settings
from django.core.mail import send_mail

from geopy.distance import great_circle
from django.utils import timezone
from django.template.loader import render_to_string

def my_scheduled_job():
  from public.models import MissingPerson,sendingEmail,User
  missingperson = MissingPerson.objects.filter(status = 1)
  current_time = timezone.now()
  
  for val in missingperson: 
    search_radius = ((current_time - val.last_seen_date).seconds // 3600 + 1) * 2  # زيادة 2 كم كل ساعة
    point1 = (val.lat, val.lng)
    for user in User.objects.filter(is_staff=False):
      print(user)
      print(search_radius)
      print(sendingEmail.objects.filter(user=user,person=val).exists())
      if not sendingEmail.objects.filter(user=user,person=val).exists():
        point2 = (user.profile.latitude,user.profile.longitude)
        distance = great_circle(point1, point2).kilometers
        print(distance)
        print(search_radius)
        if distance <= search_radius:
                # إرسال البريد الإلكتروني
                html = render_to_string('public/views/detiles.html',{'person':val,'time':val.last_seen_date.isoformat})
                send_mail(
                   'تنبيه بمفقود',
                   '',
                    'info@missing.desert-technology.com.ly',
                    [user.email],
                    html_message=html
                )
                # إنشاء سجل إرسال البريد الإلكتروني
                sendingEmail.objects.create(person=val, user=user)