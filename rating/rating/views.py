from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from .models import Professor, Module, User, Rate
from .serializers import ProfessorSerializer, ModuleSerializer, UserSerializer, RateSerializer

import json
import hashlib
from decimal import *
from datetime import datetime

class ModuleList(APIView):

    def get(self, request):
        try:
            cookie = request.COOKIES["key"]
            if cookie == "":
                return Response([{"result":3}])
            user = User.objects.get(cookie=cookie)
            try:
                allModule = Module.objects.all()
                allModule_serializer = ModuleSerializer(allModule, many=True)
                module_list = []
                for module in allModule:
                    professors = module.professor_set.all().values()
                    professor_list = []
                    for professor in professors:
                        professor_list.append(professor['name'])

                    module_serializer = ModuleSerializer(module)
                    newModule = module_serializer.data
                    newModule['professors']=professor_list
                    module_list.append(newModule)
                module_list.append({"result":1})
                return Response(module_list)

            except:
                return Response([{"result":0}])
        except:
            return Response([{"result":2}])

    def post(self,request):
        return Response([{"result":0}])

class Register(APIView):
    def post(self,request):
        try:
            info = request.data
            name = info['name']
            email = info['email']
            password = info['password']

            validator = EmailValidator()
            validator(email)

            try:
                isUserExist = User.objects.get(name=name)
                return Response({"result":0})

            except:
                salt = "Zelda first in the world"
                hash = hashlib.sha256()
                hash.update((password+salt+name).encode("utf8"))
                hashpw = hash.hexdigest()

                try:
                    newUser = User.objects.create(name=name, email=email, password=hashpw)
                    return Response({"result":1})

                except Exception as e:
                    return Response({"result":2})

        except:
            return Response({"result":3})

    def get(self,request):
        return Response({"result":4})

class Login(APIView):
    def get(self,request):
        try:
            info = request.data
            name = info['name']
            password = info['password']

            salt = "Zelda first in the world"
            hash = hashlib.sha256()
            hash.update((password+salt+name).encode("utf8"))
            hashpw = hash.hexdigest()
            isUserExist = User.objects.get(name=name, password=hashpw)

            if isUserExist.cookie == '':
                hash = hashlib.sha256()
                hash.update(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").encode("utf8"))
                hashCookie = hash.hexdigest()
                isUserExist.cookie = hashCookie
                isUserExist.save()
                return Response({"result":1,"cookie":hashCookie})
            elif isUserExist.cookie == request.COOKIES["key"]:
                return Response({"result":2})
            elif isUserExist.cookie != request.COOKIES["key"]:
                return Response({"result":3,"cookie":isUserExist.cookie})

        except:
            return Response({"result":0})

    def post(self,request):
        return Response({"result":4})

class Logout(APIView):
    def post(self,request):
        return Response({"result":0})

    def get(self,request):
        try:
            cookie = request.COOKIES["key"]
            if cookie == "":
                return Response({"result":2})
            user = User.objects.get(cookie=cookie)
            user.cookie = ""
            user.save()
            return Response({"result":1,"cookie":user.cookie})
        except:
            return Response({"result":0})

class RateProcess(APIView):
    def post(self,request):
        info = request.data
        userCookie = request.COOKIES["key"]
        if userCookie == "":
            return Response({"result":0})
        try:
            user = User.objects.get(cookie=userCookie)
            professorId = info["professorId"]
            moduleCode = info["moduleCode"]
            year = info["year"]
            semester = info["semester"]
            rating = info["rating"]
            module = Module.objects.get(nameId=moduleCode, year=year, semester=semester)
            professor = Professor.objects.get(nameId=professorId, modules=module)
            try:
                score = float(rating)
                isRatingExists = Rate.objects.get(score=score, professor=professor, user=user)
                return Response({"result":2})
            except:
                score = float(rating)
                if (score >= 1) and (score <=5):
                    newRating = Rate.objects.create(score=score, professor=professor, user=user)
                    return Response({"result":1})
                else:
                    return Response({"result":3})
        except:
            return Response({"result":0})

    def get(self,request):
        return Response({"result":4})

class Average(APIView):
    def get(self,request):
        try:
            cookie = request.COOKIES["key"]
            if cookie == "":
                return Response({"result":3})
            user = User.objects.get(cookie=cookie)

            info = request.data
            professorId = info["professorId"]
            moduleCode = info["moduleCode"]
            moduleList = Module.objects.filter(nameId=moduleCode)
            ratingNum = 0
            ratingSum = 0
            for module in moduleList:
                try:
                    professor = Professor.objects.get(nameId=professorId, modules=module)
                    ratingList = Rate.objects.filter(professor=professor)
                    for rating in ratingList:
                        ratingNum = ratingNum + 1
                        ratingSum = ratingSum + rating.score
                except:
                    pass
            result = Decimal(ratingSum/ratingNum).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            return Response({"result":1, "averageScore":result})
        except:
            return Response({"result":2})

    def post(self,request):
        return Response({"result":0})

class View(APIView):
    def post(self,request):
        return Response({"result":0})

    def get(self,request):
        try:
            cookie = request.COOKIES["key"]

            if cookie == "":
                return Response({"result":3})

            user = User.objects.get(cookie=cookie)
            professorList = Professor.objects.all()
            professorsId = []
            professorsName = []
            professorsDic = {}
            for professor in professorList:
                if (professor.nameId in professorsId):
                    ratingList = Rate.objects.filter(professor=professor)
                    ratingSum = professorsDic[professor.nameId]
                    for rating in ratingList:
                        ratingSum[0] = ratingSum[0] + 1
                        ratingSum[1] = ratingSum[1] + rating.score
                    professorsDic[professor.nameId] = ratingSum
                else:
                    professorsId.append(professor.nameId)
                    professorsName.append(professor.name)
                    ratingList = Rate.objects.filter(professor=professor)
                    ratingSum = [0,0]
                    for rating in ratingList:
                        ratingSum[0] = ratingSum[0] + 1
                        ratingSum[1] = ratingSum[1] + rating.score
                    professorsDic[professor.nameId] = ratingSum
            result = []
            for i in range(len(professorsName)):
                infos = []
                infos.append(professorsId[i])
                infos.append(professorsName[i])
                infos.append(Decimal(professorsDic[professorsId[i]][1]/professorsDic[professorsId[i]][0]).quantize(Decimal('1.'), rounding=ROUND_HALF_UP))
                result.append(infos)
            return Response({"result":1, "ratings":result})

        except:
            return Response({"result":2})
