# -*- coding: utf-8 -*-
from five import grok
from vindula.agendacorporativa import MessageFactory as _

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent, ATContentTypeSchema
from Products.ATContentTypes.content import schemata
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from vindula.agendacorporativa.content.interfaces import ICommitment
from vindula.agendacorporativa.config import *

from DateTime import DateTime

from Products.UserAndGroupSelectionWidget.at import widget

from Products.Archetypes.interfaces import IObjectEditedEvent, IObjectInitializedEvent


Commitment_schema = ATContentTypeSchema + Schema((

    DateTimeField(
        name='start_datetime',
        default_method = 'getDefaultTime',
        widget=CalendarWidget(
            label=_(u"Data Inicial"),
            description=_(u"Selecione o período inicial desse compromisso."),
            # show_hm = 0,
            format = '%d/%m/%Y %H:%M',
        ),
        required=True,
    ),

    DateTimeField(
        name='end_datetime',
        default_method = 'getDefaultTime',
        widget=CalendarWidget(
            label=_(u"Data de Termino"),
            description=_(u"Selecione o período de termino desse compromisso."),
            # show_hm = 0,
            format = '%d/%m/%Y %H:%M',
        ),
        required=True,
    ),
    
    LinesField(
	    name="convidados",
	    multiValued=1,
	    widget = widget.UserAndGroupSelectionWidget(
	        label=_(u"Usuário que participarão desse compromisso"),
	        description=_(u"Selecione os usuarios que participarão desse compromisso."),
	        usersOnly=True,
	        ),
	    required=False,
	),

))

finalizeATCTSchema(Commitment_schema, folderish=False)

Commitment_schema.changeSchemataForField('location', 'default')
Commitment_schema.moveField('description', before='location')


invisivel = {'view':'invisible','edit':'invisible',}
# Dates
L = ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['excludeFromNav','allowDiscussion']

for i in L:
    Commitment_schema[i].widget.visible = invisivel 


class Commitment(ATCTContent):
    """ Commitment """
    security = ClassSecurityInfo()
    
    implements(ICommitment)    
    portal_type = 'Commitment'
    _at_rename_after_creation = True
    schema = Commitment_schema

    def getDefaultTime(self):
        return DateTime()

registerType(Commitment, PROJECTNAME) 


@grok.subscribe(ICommitment, IObjectEditedEvent)        
def ModifiedCommitment(context, event):
	print 'Modifie'
	set_permision_urer_convidado(context)

@grok.subscribe(ICommitment, IObjectInitializedEvent)        
def CreatedCommitment(context, event):
	print 'Create'
	set_permision_urer_convidado(context)

def set_permision_urer_convidado(context):
    if not 'portal_factory' in context.getPhysicalPath():
        for username, roles in context.get_local_roles():
            if not 'Owner' in roles:
                context.manage_delLocalRoles([username])

        for username in context.getConvidados():
            context.manage_setLocalRoles(username, ['Reader'])




