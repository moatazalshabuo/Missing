from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .serializer import *

# Create your views here.
def index(request):
    
    return render(request,'public/views/index.html',{'person':MissingPerson.objects.filter(status='1').order_by('-id')[:5]})

def search_missing_persons(request):
    query = request.GET.get('search')
    results = []
    if query:
        results = MissingPerson.objects.filter(
            first_name__icontains=query
        )
    return render(request, 'public/views/search_results.html', {'persons': results, 'query': query})

def awareness(request):
    return render(request,'public/views/awareness.html')
def public_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('admin.index')
            else:
                return redirect('public.index')
        else:
            messages.error(request,'يوجد خطاء في تسجيل الدخول')
    return render(request,'public/views/login.html')

def public_singup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            if request.POST['first_name'].isalpha() and request.POST['first_name'].isalpha():
                user = form.save()
                login(request, user)
                messages.success(request, "تم إنشاء الحساب بنجاح")
                return redirect("/")  # استبدل 'home' بالوجهة المناسبة بعد تسجيل الدخول
            else:
                messages.error(request,'الاسم لا يجب ان يتضمن اي ارقام او رموز')
        else:
            messages.error(request, "هناك خطأ في النموذج. يرجى التحقق من المدخلات.")
    else:
        form = CustomUserCreationForm()
    return render(request, "public/views/singup.html", {"form": form})

def public_Volunteers(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(request.FILES)
        if form.is_valid():
            if request.POST['first_name'].isalpha() and request.POST['first_name'].isalpha():
                
                user = form.save()
                user.is_staff = True
                user.is_active = False
                user.save()
                photoForm = Photo_Profile(None,request.FILES,instance=user.profile)
                photoForm.save()
                print(photoForm.errors)
              
                
                # return redirect("/")  # استبدل 'home' بالوجهة المناسبة بعد تسجيل الدخول
                messages.success(request, " تم إنشاء الحساب بنجاح الرجاء الانتظانر حتى يتم تفعيل الايميل")
                form = CustomUserCreationForm()
            else:
                messages.error(request,'الاسم لا يجب ان يتضمن اي ارقام او رموز')
        else:
            messages.error(request, "هناك خطأ في النموذج. يرجى التحقق من المدخلات.")
    else:
        form = CustomUserCreationForm()
    return render(request, "public/views/Volunteers_create.html", {"form": form})
def public_volun_index(request):
    data = User.objects.filter(is_staff=True,is_active=True,is_superuser=False)
    return render(request,'public/views/Volunteers.html',{'users':data})
def register_mp(request):
    if request.method == 'POST':
        if MissingPerson.objects.filter(user=request.user,status=3).count() < 3:
            missing_person = MissingPerson.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birth_date=request.POST['birth_date'],
                gender=request.POST['gender'],
                height=request.POST['height'],
                weight=request.POST['weight'],
                hair_color=request.POST['hair_color'],
                eye_color=request.POST['eye_color'],
                distinguishing_marks=request.POST['distinguishing_marks'],
                last_seen_date=request.POST['last_seen_date'],
                lat=request.POST['lat'],
                lng=request.POST['lng'],
                Region=request.POST['Region'],
                health_conditions=request.POST['health_conditions'],
                last_seen_clothing=request.POST['last_seen_clothing']
            )
            if request.user:
                missing_person.user = request.user
                missing_person.save()
            form = PhotoMissingPeopleForm(None,request.FILES,instance=missing_person)
            form.save()
            Reporter.objects.create(
                missing_person=missing_person,
                first_name=request.POST['first_name_l'],
                last_name=request.POST['last_name_l'],
                relationship_to_missing=request.POST['relationship_to_missing_l'],
                phone_number=request.POST['phone_number_l'],
                address=request.POST['address_l'],
                additional_info=request.POST['additional_info_l'],
            )
            messages.success(request,'تم الحفظ بنجاح')
        else:
            messages.error(request,'تم رفض طلبك الرجاء التواصل مع الدعم الفني لمزيد من التفاصيل')
    return render(request,'public/views/register_missing_person.html')

def public_logout(request):
    logout(request)
    return redirect('public.login')
def success(request):
    return render(request,'public/views/success.html')
def details(request,id):
    missing_person = MissingPerson.objects.get(pk=id)
    return render(request,'public/views/detiles.html',{'person':missing_person,'time':missing_person.last_seen_date.isoformat})

@login_required(login_url='/login')
def report(request,id):
    form = ReportForm(request.POST or None)
    person = MissingPerson.objects.get(pk=id)
    if request.method == "POST":
        if form.is_valid():
            report_inf = ReportInformation.objects.create(
                missing_person=person,
                user=request.user,
                status=request.POST['status'],
                additional_info=request.POST['additional_info'],
            )
            if request.POST['lat'] == '' or request.POST['lat'] == None:
                pass
            else:
                report_inf.there_is_loc = True
                report_inf.lat = request.POST['lat']
                report_inf.lng = request.POST['lng']
                report_inf.save()
                messages.success(request,'تم الحفظ بنجاح')
            form = ReportForm()
    return render(request,'public/views/report.html',{'form':form,'person':person})

# ========================================== admin side ================================
def check_if_staff(re):
    if re.user.is_staff:
        pass
    else:
        return redirect('/')
@login_required(login_url='/login')
def admin_index(request):
    check_if_staff(request)
    persons = MissingPerson.objects.all()
    count_missing = persons.filter(status = 1).count()
    count_found = persons.filter(status = 2).count()
    count_wait = persons.filter(status = 0).count()
    count_reject = persons.filter(status = 3).count()
    chart =[]
    chart_unaccept =[]
    unaccept_messing = MissingPerson.objects.filter(status=3) 
    for i in range(1,13):
        chart.append(persons.filter(created_at__year=datetime.date.today().year,created_at__month=i).count())
    for i in range(1,13):
        chart_unaccept.append(persons.filter(status=3,created_at__year=datetime.date.today().year,created_at__month=i).count())
        
    print(chart)
    return render(request,'dashboard/views/index.html',{'count_missing':count_missing
                                                        ,'count_found':count_found,
                                                        'count_wait':count_wait,
                                                        'total':persons.count(),
                                                        'reject':count_reject,
                                                        'persons':persons,'chart':chart,'chart_unaccept':chart_unaccept,'unaccept_messing':unaccept_messing})
@login_required(login_url='/login')
def admin_map(request):
    check_if_staff(request)

    return render(request,'dashboard/views/map.html')

@login_required(login_url='/login')
def missing_persons_list(request):
    check_if_staff(request)
    missing_persons = MissingPerson.objects.filter(status='0')
    return render(request, 'dashboard/views/missing_persons_wait.html', {'missing_persons': missing_persons})
@login_required(login_url='/login')
def missing_persons_approve(request):
    check_if_staff(request)
    missing_persons = MissingPerson.objects.filter(status='1')
    return render(request, 'dashboard/views/missing_persons_accept.html', {'missing_persons': missing_persons})
@login_required(login_url='/login')
def missing_persons_reject(request):
    check_if_staff(request)
    missing_persons = MissingPerson.objects.filter(status='3')
    return render(request, 'dashboard/views/missing_persons_reject.html', {'missing_persons': missing_persons})
@login_required(login_url='/login')
def missing_persons_found(request):
    check_if_staff(request)
    missing_persons = MissingPerson.objects.filter(status='2')
    return render(request, 'dashboard/views/missing_persons_found.html', {'missing_persons': missing_persons})
@login_required(login_url='/login')
def missing_persons_all(request):
    check_if_staff(request)
    missing_persons = MissingPerson.objects.all()
    return render(request, 'dashboard/views/missing_persons_all.html', {'missing_persons': missing_persons})
from django.conf import settings
from django.core.mail import send_mail

from geopy.distance import great_circle
from django.utils import timezone
@login_required(login_url='/login')
def approve_person(request, person_id):
    check_if_staff(request)
    person = get_object_or_404(MissingPerson, id=person_id)
    person.status = 1  # تم العثور
    val = person
    current_time = timezone.now()
    search_radius = ((current_time - val.last_seen_date).seconds // 3600 + 1) * 2  # زيادة 2 كم كل ساعة
    point1 = (val.lat, val.lng)
    for user in User.objects.filter(is_staff=False):
      print("kkkkk",search_radius)
      if not sendingEmail.objects.filter(user=user,person=val).exists():
        point2 = (user.profile.latitude,user.profile.longitude)
        distance = great_circle(point1, point2).kilometers
        print(distance)
        print(search_radius)
        if distance <= search_radius:
                # إرسال البريد الإلكتروني
            html = '''<!DOCTYPE html>
                          <html lang="ar">
                          <head>
                              <meta charset="UTF-8">
                              <title>تفاصيل الشخص المفقود</title>
                              <style>
                                  body {
                                        font-family: Arial, sans-serif;
                                        direction: rtl;
                                        text-align: right;
                                        background-color: #f4f4f4;
                                        margin: 0;
                                        padding: 0;
                                    }
                                    .container {
                                        width: 80%;
                                        margin: 20px auto;
                                        background: #fff;
                                        padding: 20px;
                                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                    }
                                    .profile {
                                        display: flex;
                                        align-items: center;
                                        margin-bottom: 20px;
                                    }
                                    .profile img {
                                        border-radius: 50%;
                                        margin-left: 20px;
                                        width: 150px;
                                        height: 150px;
                                        object-fit: cover;
                                    }
                                    .profile-details {
                                        flex: 1;
                                    }
                                    .profile-details h2 {
                                        margin: 0;
                                        color: #333;
                                    }
                                    .profile-details p {
                                        margin: 5px 0;
                                        color: #666;
                                    }
                                    .profile-details a {
                                        display: inline-block;
                                        margin-top: 10px;
                                        padding: 10px 20px;
                                        color: #fff;
                                        background-color: #007BFF;
                                        text-decoration: none;
                                        border-radius: 5px;
                                    }
                                    .profile-details a:hover {
                                        background-color: #0056b3;
                                    }
                                </style>
                            </head>
                            <body>'''
            html += f'''<div class="container">
                                    <div class="profile">
                                        
                                            <img src="https://missing.desert-technology.com.ly/{val.photo.url}" alt="صورة حديثة">
                                        
                                        <div class="profile-details">
                                            <h2>{val.first_name} {val.last_name}</h2>
                                            <p><strong>منطقة الاختفاء:</strong> {val.Region}</p>
                                            <a href="https://missing.desert-technology.com.ly/details/{val.id}">عرض التفاصيل</a>
                                        </div>
                                    </div>
                                </div>
                            </body>
                            </html>'''
            send_mail(
                  'تنبيه بمفقود',
                  '',
                    'info@missing.desert-technology.com.ly',
                    [user.email],
                    html_message=html
                )
            sendingEmail.objects.create(person=val,user=user)

    person.save()
    return redirect('/dash/missing_persons/wait')
@login_required(login_url='/login')
def reject_person(request, person_id):
    check_if_staff(request)
    person = get_object_or_404(MissingPerson, id=person_id)
    person.status = 3  # في انتظار
    person.save()
    return redirect('/dash/missing_persons/wait')


@login_required(login_url='/login')
def delete_person(request, id):
    check_if_staff(request)
    person = get_object_or_404(MissingPerson, id=id)
    person.delete()
    return redirect('/dash/missing_persons/wait')

@login_required(login_url='/login')
def missing_person_detail(request, person_id):
    check_if_staff(request)
    person = get_object_or_404(MissingPerson, id=person_id)
    return render(request, 'dashboard/views/missing_person_detail.html', {'person': person})

@login_required(login_url='/login')
def mark_as_found(request, person_id):
    check_if_staff(request)
    if request.method == 'POST':
        form = FoundPersonDetailsForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            fund.person = MissingPerson.objects.get(pk=person_id)
            fund.save()
            person = get_object_or_404(MissingPerson, id=person_id)
            person.status = '2'  # تحديث الحالة إلى "تم العثور"
            person.save()
            messages.success(request,'تم الحفظ بنجاح')
        return redirect('missing_person_detail', person_id=person_id)
    else:
        form = FoundPersonDetailsForm()
    return render(request,'dashboard/views/found.html',{'form':form})

from django.db.models import Count
from django.db.models.functions import TruncMonth



def get_age_group_for_children(age):
    if age <= 6:
        return 'اقل من 6 سنوات'
    elif 6 <= age <= 12:
        return '6-12 سنة'
    elif 13 <= age <= 17:
        return '13-17 سنة'
    else:
        return 'أكبر من 17'
    
def get_initial_data():
    report_missing = MissingPerson.objects.values('Region').annotate(count=Count('id')).order_by('-count')[:5]
    report_found = MissingPerson.objects.filter(status='2').values('Region').annotate(count=Count('id')).order_by('-count')[:5]
    report_trend = MissingPerson.objects.annotate(month=TruncMonth('last_seen_date')).values('month').annotate(count=Count('id')).order_by('month')

    total_missing = MissingPerson.objects.filter(status='1').count()
    total_found = MissingPerson.objects.filter(status='2').count()
    total_rejected = MissingPerson.objects.filter(status='3').count()
     # Age group distribution for children
    age_distribution = MissingPerson.objects.all()
    age_groups = {'اقل من 6 سنوات': 0, '6-12 سنة': 0, '13-17 سنة': 0}
    for person in age_distribution:
        age = person.get_birt_day()
        if age <= 17:
            age_group = get_age_group_for_children(age)
            age_groups[age_group] += 1
    missing_person = MissingPerson.objects.filter(status='1')
    found_person = MissingPerson.objects.filter(status='2')
    data = {
        'missing': {
            'regions': [item['Region'] for item in report_missing],
            'counts': [item['count'] for item in report_missing]
        },
        'found': {
            'regions': [item['Region'] for item in report_found],
            'counts': [item['count'] for item in report_found]
        },
        'trend': {
            'months': [item['month'].strftime('%Y-%m') for item in report_trend],
            'counts': [item['count'] for item in report_trend]
        },
        'total_missing': total_missing,
        'total_found': total_found,
        'total_rejected': total_rejected,
        'total_reports': MissingPerson.objects.all().count(),
        'age_groups': age_groups,
        'missing_people':Missing_Person_serializer(missing_person,many=True).data,
        'found_people':Missing_Person_serializer(found_person,many=True).data
    }
    return data

@login_required(login_url='/login')
def missing_persons_dashboard(request):
    check_if_staff(request)
    data = get_initial_data()
    return render(request, 'dashboard/views/charts.html', {'data': data,'table_missing':zip(data['missing']['regions'],data['missing']['counts'])})

def filter_data_by_region_and_date(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    region = request.GET.get('region')
    filters = {}
    if start_date and end_date:
        filters['last_seen_date__range'] = [start_date, end_date]
        
    if region:
        filters['Region'] = region
        
    report_missing = MissingPerson.objects.filter(**filters).values('Region').annotate(count=Count('id')).order_by('-count')[:5]

    report_found = MissingPerson.objects.filter(**filters,status='2').values('Region').annotate(count=Count('id')).order_by('-count')[:5]

    report_trend = MissingPerson.objects.filter(**filters).annotate(
        month=TruncMonth('last_seen_date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    total_missing = MissingPerson.objects.filter(
        **filters,
        status='1',
    ).count()

    total_found = MissingPerson.objects.filter(
    **filters,status='2',
    ).count()

    total_rejected = MissingPerson.objects.filter(
        **filters,
        status='3',
    ).count()
    
    # Age group distribution for children
    
    age_distribution = MissingPerson.objects.filter(
        **filters
    )
    
    age_groups = {'اقل من 6 سنوات': 0,  '6-12 سنة': 0, '13-17 سنة': 0}

    for person in age_distribution:
        age = person.get_birt_day()
        if age <= 17:
            age_group = get_age_group_for_children(age)
            age_groups[age_group] += 1
            
    missing_person = MissingPerson.objects.filter(**filters,status='1')
    found_person = MissingPerson.objects.filter(**filters,status='2')
    data = {
        'missing': {
            'regions': [item['Region'] for item in report_missing],
            'counts': [item['count'] for item in report_missing]
        },
        'found': {
            'regions': [item['Region'] for item in report_found],
            'counts': [item['count'] for item in report_found]
        },
        'trend': {
            'months': [item['month'].strftime('%Y-%m') for item in report_trend],
            'counts': [item['count'] for item in report_trend]
        },
        'total_missing': total_missing,
        'total_found': total_found,
        'total_rejected': total_rejected,
        'total_reports': MissingPerson.objects.filter(**filters).count(),
        'age_groups': age_groups,
        'missing_people':Missing_Person_serializer(missing_person,many=True).data,
        'found_people':Missing_Person_serializer(found_person,many=True).data
    }
    return JsonResponse(data)

@login_required(login_url='/login')
def missing_prson_info(request):
    check_if_staff(request)
    return render(request,'dashboard/views/missing_persons_info.html',{'report':ReportInformation.objects.order_by('-id').all()})


@login_required(login_url='/login')
def volunteers_list(request):
    check_if_staff(request)
    # جلب المتطوعين الذين هم جزء من فريق العمل وليسوا مشرفين
    volunteers = User.objects.filter(is_staff=True, is_superuser=False)

    if request.method == "POST":
        # معالجة طلب التفعيل أو إلغاء التفعيل
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = User.objects.get(id=user_id)

        if action == "activate":
            user.is_active = True
        elif action == "deactivate":
            user.is_active = False
        elif action == "delete":
            user.delete()

        user.save() if action != "delete" else None
        return redirect('volunteers_list')

    return render(request, 'dashboard/views/Volunteers.html', {'volunteers': volunteers})

def about(request):
    return render(request,'public/views/about.html')