from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
# Create your views here.
from article import models
from .models import *
import json
from django.db import transaction


#should be singleton so all the errors to be added to the same instance? still thinking?!
def error_logger(error):
	errorFile=[]
	exeption_type='exeption type:'+str(type(error).__name__) 
	exeption_message='exeption message:'+str(error)
	errorFile.append((exeption_type,exeption_message))
	print('errorFile',errorFile)
	
#create is_valid method for model as the one in model form	
def is_valid(obj):
	try:
		#Django model method that validate the instance data with the model validation
		#and return nothing or exception 
		obj.full_clean()

	except Exception as e:
		error_logger(e)
		isValid =False

	else:
		isValid =True

	finally:
		return isValid

#______________________________Factory design patern return the table instance ______________________
class Factory:

	def generate_instance(self,table,data):

		interface=self.get_interface(table)
		try:
			instance= interface(data)
			
		except Exception as e:
			error_logger(e)
			instance=None
		finally:
			return instance


	def get_interface(self,table):

		if table=='Account':
			return self._dataToAccount

		elif table=='APN':
			return self._dataToAPN
		elif table=='AccessLinkAccount':
			return self._dataToAccessLinkAccount
			
		elif table=='MarwanAccount':
			return self._dataToMarwanAccount

		elif table=='SIM':
			return self._dataToSIM

		elif table=='Gateway':
			return self._dataToGateway

	def _dataToAccount(self,data):

		account=Account(
			account_id=data['account_id'],
			account_name=data['account_name'],
			operator_account_id=data['operator_account_id'],
			)
		return account


	def _dataToAPN(self,data):

		apn=APN(
			apn_name=data['apn_name'],
			)

		return apn


	def _dataToAccessLinkAccount(self,data):

		accessLinkAccount=AccessLinkAccount(
			access_link_account_number=data['access_link_account_number'],
			)

		return accessLinkAccount


	def _dataToMarwanAccount(self,data):

		marwanAccount=MarwanAccount(
			marwan_account_number=data['marwan_account_number'],
			host_name_1=data['host_name_1'],
			host_name_2=data['host_name_2'],
			)

		return marwanAccount


	def _dataToSIM(self,data):

		sim=SIM(
			iccid=data['iccid'],
			apn=APN.objects.get(apn_name=data['apn_name'])
			)

		return sim


	def _dataToGateway(self,data):

		gateway=Gateway(
			serial=data['serial'],
			project=data['project'],
			imie=data['imie'],
			sim=SIM.objects.get(iccid=data['iccid'])
			)

		return gateway


#-----------------------take the instance from the factory validate it and save --------------------------------------------------
def create_row_of(request,table,**data):

	factory=Factory()
	tableInstance=factory.generate_instance(table,data)

	if tableInstance and  is_valid(tableInstance):
		tableInstance.save()
		pk=tableInstance.pk
		return HttpResponse('success with pk ='+str(pk))
	else:
		return HttpResponse('error check the log')

#def add_manyToManyRelation():
#	relationDetails={
#	table1:{name:'Account','searchKey':operator_account_id,'value':'value'},
#	table2:{name:'APN','searchKey':apn_name,'value':'value','relation_column_name':'relation_column_name'}
#	}
#t1=relationDetails['table1']
#t2=relationDetails['table2']
#t1_Model_name=t1['name']
#t2_Model_name=t2['name']
#t1_instance=t1_Model_name.objects.get(t1[searchKey]=t1['value'])
#t2_instance=t2_Model_name.objects.get(t2[searchKey]=t2['value'])
#t1_instance.t1[relation_column_name].add(t2_instance)
