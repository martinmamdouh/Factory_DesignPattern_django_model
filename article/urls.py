from django.urls import path

from . import views

urlpatterns = [

path('new/<str:table>/',views.create_row_of,
		#{'account_id':'6','account_name':'6','operator_account_id':'6'}
		#{'apn_name':'m2m233'}
		#{'access_link_account_number':1}
		#{
		#'marwan_account_number':1,
		#'host_name_1':'host_name_1',
		#'host_name_2':'host_name_1'
		#}
		{'iccid':123456587878453,'apn_name':'m2m333333333'}
	)
]
