from cgitb import text
import string
from turtle import pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
from accounts.models import Member
import pandas as pd
import numpy as np

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file_name', help='file with user info')

    def handle(self, *args, **kwargs):
        fileName = kwargs['file_name']
        userInfo = pd.read_csv(fileName)
        
        for index,row in userInfo.iterrows():
            firstName = row['FirstName']
            lastName = row['LastName']
            email=row['Email']
            mobile=row['Mobile']
            country=row['Country']

            if lastName == np.nan or firstName == np.nan:
                continue

            if mobile == 0:
                mobile=1985
            
            if pd.isna(email):
                email="unknown@email.com"
                
            if pd.isna(country):
                country = "Sri Lanka"

            username=firstName+lastName[0]
            password=lastName[:2]+str(mobile)[:4]+firstName[:2]

            try:
                print("Saving -> "+firstName+", "+ lastName+","+str(mobile)+","+username+","+password)
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
                member = Member.objects.get(user_id=user.id)
                member.country = country
                member.mobile= str(mobile)
                member.save(update_fields=['country','mobile'])

                print(firstName+", "+ lastName+", "+str(mobile)+","+username+","+password)
            except IntegrityError as e:
                print("ERROR "+firstName+" "+lastName+" could not be added user "+username+" already exists")
            
         



            

