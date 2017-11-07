from __future__ import unicode_literals
 
from django.db import models
 
class Player(models.Model):
    order = models.IntegerField()
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    position = models.CharField(max_length = 30)
    strike_num = models.IntegerField()
    out_num = models.IntegerField()
    single_num = models.IntegerField()
    double_num = models.IntegerField()
    triple_num = models.IntegerField()
    
    


    


