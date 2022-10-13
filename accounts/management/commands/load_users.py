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
        userInfo=userInfo.fillna(0)
        wfile = open("usernames.csv","w")

        for index,row in userInfo.iterrows():
            firstName = row['FirstName']
            lastName = row['LastName']
            email=row['Email']
            mobile=row['Mobile']
            country=row['Country']

            if lastName==0 and firstName ==0:
                continue

            if lastName ==0 or  lastName == "":
                lastName="Unknown"

            if mobile == 0:
                mobile=1985
            
            if pd.isna(email):
                email=""
                
            if pd.isna(country):
                country = "Sri Lanka"

            firstName = firstName.strip()
            lastName = lastName.strip()
            mobile = str(mobile).strip()

            username=firstName+lastName[0]
            password=firstName[:2]+mobile[:4]+lastName[0]

            try:
                print("Saving -> "+firstName+", "+ lastName+","+mobile+","+username+","+password)
                check = User.objects.filter(username=username)
                if bool(check):
                    print("User "+username+" already exists")
                    continue

                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
                member = Member.objects.get(user_id=user.id)
                member.country = country
                member.mobile= str(mobile)
                member.save(update_fields=['country','mobile'])
                wfile.write(username+","+password+"\n")
                
            except IntegrityError as e:
                print("ERROR "+firstName+" "+lastName+" could not be added user "+username+" already exists")
            
        wfile.close()



            

