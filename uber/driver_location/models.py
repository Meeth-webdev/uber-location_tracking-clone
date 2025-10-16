from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICE=(
        ('customer','Customer'),
        ('driver','Driver')
    )
    user_type=models.CharField(max_length=20,choices=USER_TYPE_CHOICE,default='customer')
    phone_number=models.CharField(max_length=15,blank=True)


class Ride(models.Model):
    RIDE_STATUS=(
        ('requested','REQUESTED'),
        ('accepted','ACCEPTED'),
        ('in_progress','IN_PROGRESS'),
        ('completed','COMPLETED'),
        ('cancelled','CANCELLED')        
    )

    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer_rides')
    driver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='driver_rides')

    pickup_adress=models.TextField()
    dropoff_adress=models.TextField()
    status=models.CharField(max_length=10,choices=RIDE_STATUS,default='requested')
    created_at=models.DateTimeField(auto_now_add=True)
    accepted_at=models.DateTimeFiled(null=True,blank=True)
    completed_at=models.DateTimeField(null=True,blank=True)


    class Meta:
        ordering=['-created_at']


class DriverLocation(models.Model):
    driver=models.OneToOneField(User,on_delete=models.CASCADE,related_name='last_known_location')
    latitude=models.DecimalField(max_digits=9,decimal_places=6)
    longitude=models.DecimalField(max_digits=9,decimal_places=6)
    last_updated=models.DateTimeField(auto_now=True)




    
