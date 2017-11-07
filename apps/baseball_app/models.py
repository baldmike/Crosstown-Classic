from __future__ import unicode_literals
 
from django.db import models
 
class Player(models.Model):
    team = models.CharField(max_length = 30)
    order = models.IntegerField()
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    position = models.CharField(max_length = 30)
    strike_num = models.IntegerField(default = 20)
    hr_num = models.IntegerField(default = 25)
    single_num = models.IntegerField(default = 35)
    double_num = models.IntegerField(default = 40)
    triple_num = models.IntegerField(default = 44)
    hbp_num = models.IntegerField(default = 45)
    
    


    


