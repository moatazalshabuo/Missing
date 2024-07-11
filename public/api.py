from django.http import JsonResponse
from .serializer import *
from .models import *

def get_missing(request):
    status = int(request.GET['status'])
    age = str(request.GET['ourage']).split('-')
    from_date = request.GET['from']
    to_date = request.GET['to']
    missing_person = MissingPerson.objects.all().exclude(status='0')
    if status != 0:
        missing_person = missing_person.filter(status=status)
        print(status)
    if from_date != '':
        missing_person = missing_person.filter(last_seen_date__gte=from_date)
        
    if to_date != '':
        missing_person = missing_person.filter(last_seen_date__lte=to_date)
    if age[0] != '':
        missing_person1 = []
        for val in missing_person:
            if val.get_birt_day() in range(int(age[0]),int(age[1])):
                missing_person1.append(val)
        missing_person = missing_person1
         
    return JsonResponse({'person':Missing_Person_serializer(missing_person,many=True).data})

def get_person(requset,id):
    return JsonResponse(Missing_Person_serializer(MissingPerson.objects.get(pk=id)).data)