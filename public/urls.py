from django.urls import path,include
from .views import *
from .api import *
urlpatterns = [
    path('',index,name='public.index'),
    path('register_missing_person',register_mp,name='public.register_missing_person'),
    path('details/<int:id>',details,name='public.details'),
    path('report/<int:id>',report,name='public.report'),
    path('login/',public_login,name='public.login'),
    path('singup/',public_singup,name='public.singup'),
    path('logout',public_logout,name='public.logout'),
    path('success',success,name='success'),
    path('awareness',awareness,name='awareness'),
    # ============== api urls ====================
    
    path('api/get_missing',get_missing),
    path('api/person-data/<int:id>',get_person)
    # ============= admin ===========================
    ,path('dash',admin_index,name='admin.index'),
    path('dash/map',admin_map,name='admin.map'),
    path('dash/missing_persons/wait',missing_persons_list,name='dash.missing_persons.wait'),
    path('dash/missing_persons/aprove',missing_persons_approve,name='dash.missing_persons.approve'),
    path('dash/missing_persons/reject',missing_persons_reject,name='dash.missing_persons.reject'),
    path('dash/missing_persons/found',missing_persons_found,name='dash.missing_persons.found'),
    path('dash/missing_persons/all',missing_persons_all,name='dash.missing_persons.all'),
    path('dash/missing_persons/info',missing_prson_info,name='dash.missing_persons.info'),
    path('approve/<int:person_id>/', approve_person, name='approve_person'),
    path('reject/<int:person_id>/', reject_person, name='reject_person'),
    path('found/<int:person_id>/', mark_as_found, name='found_person'),
    path('missing-person/<int:person_id>/', missing_person_detail, name='missing_person_detail'),
    path('dash/dashboard/', missing_persons_dashboard, name='missing_persons_dashboard'),
    path('filter_data_by_region_and_date', filter_data_by_region_and_date, name='filter_data_by_region_and_date'),
    path('search/', search_missing_persons, name='search_missing_persons'),
    path('delete/<int:id>',delete_person,name='delete.person'),
    path('api/check_messing',check_data_missing,name='check.missing')
]
