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
#----------------------- DAO Part which is the only one responsible to write in database.-------------------------------------
def create_row_of(table,**data):

	factory=Factory()
	tableInstance=factory.generate_instance(table,data)

	if tableInstance and  is_valid(tableInstance):
		newRow=tableInstance.save()

		return newRow
	else:
		return None

def add_manyToManyRelation(relationDetails):# :RelationDetailsInterface

	parentTableInstance=relationDetails.parentTableInstance.
	childTableInstance=relationDetails.childTableInstance
	childRelationColName=relationDetails.childRelationColName

	try:
		newRelation=childTableInstance.childRelationColName.add(parentTableInstance)
	except Exception as e:
		error_logger(e)
		newRelation=None
	finally:
		return newRelation


def get_row_or_None(table,pk):
	try:
		instance=table.objects.get(pk=pk)

	except DoesNotExist as e:
		error_logger(e)
		instance=None

	finally:
		return  instance



class RelationDetailsInterface()
	def __init__(self,parentTableInstance,childTableInstance,childRelationColName):
		self.parentTableInstance=parentTableInstance;
		self.childTableInstance=childTableInstance;
		self.childRelationColName=childRelationColName;





class ApnBL:

	def __init__(self,data):
		self.data=data

	def validat(self,data):
		pass

	def create_new(self):

		apn=create_row_of('APN',data)
		account=get_row_or_None('Account',self.data['account_pk'])
		if account:
			relationDetails=RelationDetailsInterface(account,apn,'account')
			newRelation=add_manyToManyRelation(relationDetails)
		if not account or not newRelation :
			apn.delete()
			return False
		return True 



	



