# from django.conf import settings
# from django.core.mail import send_mail

# from geopy.distance import great_circle
# from django.utils import timezone
# from django.template.loader import render_to_string

def my_scheduled_job():
    pass
#   from public.models import MissingPerson,sendingEmail,User
#   missingperson = MissingPerson.objects.filter(status = 1)
#   current_time = timezone.now()
  
#   for val in missingperson: 
#     search_radius = ((current_time - val.last_seen_date).seconds // 3600 + 1) * 2  # زيادة 2 كم كل ساعة
#     point1 = (val.lat, val.lng)
#     for user in User.objects.filter(is_staff=False):
#       print("kkkkk",search_radius)
#       if not sendingEmail.objects.filter(user=user,person=val).exists():
#         point2 = (user.profile.latitude,user.profile.longitude)
#         distance = great_circle(point1, point2).kilometers
#         print(distance)
#         print(search_radius)
#         if distance <= search_radius:
#                 # إرسال البريد الإلكتروني
#             html = '''<!DOCTYPE html>
#                           <html lang="ar">
#                           <head>
#                               <meta charset="UTF-8">
#                               <title>تفاصيل الشخص المفقود</title>
#                               <style>
#                                   body {
#                                         font-family: Arial, sans-serif;
#                                         direction: rtl;
#                                         text-align: right;
#                                         background-color: #f4f4f4;
#                                         margin: 0;
#                                         padding: 0;
#                                     }
#                                     .container {
#                                         width: 80%;
#                                         margin: 20px auto;
#                                         background: #fff;
#                                         padding: 20px;
#                                         box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#                                     }
#                                     .profile {
#                                         display: flex;
#                                         align-items: center;
#                                         margin-bottom: 20px;
#                                     }
#                                     .profile img {
#                                         border-radius: 50%;
#                                         margin-left: 20px;
#                                         width: 150px;
#                                         height: 150px;
#                                         object-fit: cover;
#                                     }
#                                     .profile-details {
#                                         flex: 1;
#                                     }
#                                     .profile-details h2 {
#                                         margin: 0;
#                                         color: #333;
#                                     }
#                                     .profile-details p {
#                                         margin: 5px 0;
#                                         color: #666;
#                                     }
#                                     .profile-details a {
#                                         display: inline-block;
#                                         margin-top: 10px;
#                                         padding: 10px 20px;
#                                         color: #fff;
#                                         background-color: #007BFF;
#                                         text-decoration: none;
#                                         border-radius: 5px;
#                                     }
#                                     .profile-details a:hover {
#                                         background-color: #0056b3;
#                                     }
#                                 </style>
#                             </head>
#                             <body>'''
#             html += f'''<div class="container">
#                                     <div class="profile">
                                        
#                                             <img src="{val.photo.url}" alt="صورة حديثة">
                                        
#                                         <div class="profile-details">
#                                             <h2>{val.first_name} {val.last_name}</h2>
#                                             <p><strong>منطقة الاختفاء:</strong> {val.Region}</p>
#                                             <a href="https://missing.desert-technology.com.ly/details/{val.id}">عرض التفاصيل</a>
#                                         </div>
#                                     </div>
#                                 </div>
#                             </body>
#                             </html>'''
#             send_mail(
#                    'تنبيه بمفقود',
#                    '',
#                     'info@missing.desert-technology.com.ly',
#                     [user.email],
#                     html_message=html
#                 )
#                 # إنشاء سجل إرسال البريد الإلكتروني
