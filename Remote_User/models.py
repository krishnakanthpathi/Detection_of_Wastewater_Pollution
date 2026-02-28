from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=3000)
    gender = models.CharField(max_length=300)


class predict_water_type(models.Model):

    Fid= models.CharField(max_length=300)
    Name_of_Monitoring_Location= models.CharField(max_length=300)
    Type_Water_Body= models.CharField(max_length=300)
    State_Name= models.CharField(max_length=300)
    Temperature= models.CharField(max_length=300)
    Dissolved_Oxygen_mgperL= models.CharField(max_length=300)
    pH= models.CharField(max_length=300)
    Conductivity_mhospercm= models.CharField(max_length=300)
    BOD_mgperL= models.CharField(max_length=300)
    NitrateN_NitriteN_mgperL= models.CharField(max_length=300)
    Fecal_Coliform_MPNper100ml= models.CharField(max_length=300)
    Total_Coliform_MPNper100ml= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



