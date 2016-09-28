from django.db import models


import datetime

class UserInfo(models.Model):
    name = models.CharField(max_length=20,blank=False)
    title = models.CharField(max_length=20,blank=True)
    countHouse = models.IntegerField(blank=False,default=0)


class Coupon(models.Model):
    name  = models.CharField(max_length=120,blank=False)
    description = models.CharField(max_length=250)
    countHouse = models.IntegerField(blank=False)

class HouseList(models.Model):
    address = models.CharField(max_length=120,blank=False)
    status = models.CharField(max_length=20,blank=False)
    description = models.CharField(max_length=250,blank=True)
    refinedDetail = models.CharField(max_length=250,blank=True)
    create_date = models.DateTimeField(default=datetime.datetime.now)
def __unicode__(self):
    return "%s / %s )" % (self.address, self.status)



class Guard(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    create_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "%s / %s / %s)" % (self.name, self.number, self.address)

class Window(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    create_date = models.DateTimeField(default=datetime.datetime.now)

class Officer(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    cellphone= models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    create_date = models.DateTimeField(default=datetime.datetime.now)

