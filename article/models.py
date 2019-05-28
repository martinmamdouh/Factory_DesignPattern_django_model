from django.db import models

# Create your models here.
from django.db import models


class Account(models.Model):
    id=models.BigAutoField(primary_key=True)
    account_id=models.BigIntegerField('Account ID',blank=False,unique=True)
    account_name=models.CharField('Account Name',max_length=100,blank=False,unique=True)
    operator_account_id=models.BigIntegerField('Account ID',blank=False,unique=True)
    
    class Meta:
        db_table = 'account_tb'

class APN(models.Model):
    id=models.BigAutoField(primary_key=True)
    apn_name=models.CharField('APN Name',max_length=100,blank=False,unique=True)
    account=models.ManyToManyField(Account)

    class Meta:
        db_table = 'apn_tb'

class AccessLinkAccount(models.Model):
    id=models.BigAutoField(primary_key=True)
    access_link_account_number=models.BigIntegerField('Access Link Account Number',blank=False,unique=True)
    apn=models.ManyToManyField(APN)

    class Meta:
        db_table = 'access_link_account_tb'

class MarwanAccount(models.Model):
    id=models.BigAutoField(primary_key=True)
    marwan_account_number=models.BigIntegerField('Access Link Account Number',blank=False,unique=True)
    host_name_1=models.CharField('First Host Name',max_length=100,blank=False)
    host_name_2=models.CharField('Second Host Name',max_length=100,blank=False)
    apn=models.ManyToManyField(APN)

    class Meta:
        db_table = 'marwan_account_tb'

class SIM(models.Model):
    id=models.BigAutoField(primary_key=True)
    iccid=models.CharField('ICCID',max_length=50,blank=False,unique=True)
    apn=models.ForeignKey(APN,on_delete=models.PROTECT)

    class Meta:
        db_table = 'sim_tb'

class Gateway(models.Model):
    id=models.BigAutoField(primary_key=True)
    serial=models.CharField('Serial Number',max_length=50,blank=False,unique=True)
    project=models.CharField('Project',max_length=50,blank=False)
    imie=models.CharField('IMIE',max_length=50,blank=False,unique=True)
    sim=models.OneToOneField(SIM,on_delete=models.PROTECT,related_name='Gateway')

    class Meta:
        db_table = 'gateway_tb'