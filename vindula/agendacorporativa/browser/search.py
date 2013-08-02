# coding: utf-8
from Products.CMFCore.utils import getToolByName

from AccessControl.SecurityManagement import newSecurityManager, getSecurityManager, setSecurityManager
from DateTime import DateTime

from copy import copy

def busca_commitment(context,username,portlet=False):

	ctool = getToolByName(context, 'portal_catalog') 
	path = context.portal_url.getPortalObject().getPhysicalPath()
	date_range_query = { 'query': DateTime(), 'range': 'min'}

	query = {'path': {'query':'/'.join(path)},
		 	 'portal_type': ('Commitment',),
			 'sort_on':'getStart_datetime',
			 # 'sort_order':'descending',
			}

	if portlet:
		query['getStart_datetime'] = date_range_query

	#Busca por conpromissos do probrio usuario
	query1 = copy(query)
	query1['Creator'] = username 
	result1 = ctool(**query1)

	#Busca por compromissos que o usuario participa
	query2 = copy(query)
	query2['getConvidados'] = [username]
	result2 = ctool(**query2)

	#Busca por compromissos publicos
	query3 = copy(query)
	query3['review_state'] = ['published', 'internally_published', 'external', 'internal']
	result3 = ctool(**query3) 

	result = result1 + result2 + result3
	L = []
	L_UID = []
	for item in result:
		if not item.UID in L_UID:
			L.append(item)
			L_UID.append(item.UID)

	return L