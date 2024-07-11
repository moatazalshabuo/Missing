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
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح")
            return redirect("/")  # استبدل 'home' بالوجهة المناسبة بعد تسجيل الدخول
        else:
            messages.error(request, "هناك خطأ في النموذج. يرجى التحقق من المدخلات.")
    else:
        form = CustomUserCreationForm()
    return render(request, "public/views/singup.html", {"form": form})

def register_mp(request):
    if request.method == 'POST':
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
            health_conditions=request.POST['health_conditions'],
            last_seen_clothing=request.POST['last_seen_clothing']
        )
        
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
        return redirect('success')
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
                return redirect('success')
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
    for i in range(1,13):
        chart.append(persons.filter(created_at__year=datetime.date.today().year,created_at__month=i).count())
        
    print(chart)
    return render(request,'dashboard/views/index.html',{'count_missing':count_missing
                                                        ,'count_found':count_found,
                                                        'count_wait':count_wait,
                                                        'total':persons.count(),
                                                        'reject':count_reject,
                                                        'persons':persons,'chart':chart})
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

@login_required(login_url='/login')
def approve_person(request, person_id):
    check_if_staff(request)
    person = get_object_or_404(MissingPerson, id=person_id)
    person.status = 1  # تم العثور
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
    print(report_missing)
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
    return render(request, 'dashboard/views/charts.html', {'data': data})

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