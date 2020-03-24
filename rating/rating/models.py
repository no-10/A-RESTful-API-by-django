from django.db import models

# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=50)
    nameId = models.CharField(max_length=20)
    year = models.SmallIntegerField()
    semester = models.SmallIntegerField(choices=[(1,'semester 1'),(2,'semester 2')])

    def __str__(self):
        return '%s %d semester %d' % (self.name, self.year, self.semester)

class Professor(models.Model):
    name = models.CharField(max_length=30)
    nameId = models.CharField(max_length=20)
    modules = models.ManyToManyField(Module)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=512)
    cookie = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.name

class Rate(models.Model):
    score = models.DecimalField(max_digits=3, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.score)+' '+self.user.name+' '+self.professor.nameId
