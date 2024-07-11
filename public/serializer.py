from rest_framework import serializers
from .models import *

class Missing_Person_serializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = ['id',
                  "first_name",
                    "last_name",
                    "birth_date",
                    "gender",
                    "height",
                    "weight",
                    "hair_color",
                    "eye_color",
                    'distinguishing_marks',
                    'last_seen_date',
                    "lat",
                    "lng",
                    "health_conditions",
                    "last_seen_clothing",
                    "photo",
                    "status",
                    "created_at",
                    "get_birt_day",
                    'get_status','get_gender','Region']