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

from vindula.myvindula.tools.utils import UtilMyvindula

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
    # print 'Modifie'
    set_permision_user_convidado(context)
    envia_email_user_convidado(context)

@grok.subscribe(ICommitment, IObjectInitializedEvent)        
def CreatedCommitment(context, event):
    # print 'Create'
    set_permision_user_convidado(context)
    envia_email_user_convidado(context,True)


def set_permision_user_convidado(context):
    if not 'portal_factory' in context.getPhysicalPath():
        for username, roles in context.get_local_roles():
            if not 'Owner' in roles:
                context.manage_delLocalRoles([username])

        for username in context.getConvidados():
            context.manage_setLocalRoles(username, ['Reader'])

def envia_email_user_convidado(context,is_edit=True):
    tools = UtilMyvindula()
    list_user = [context.getOwner().getUserName()]
    list_user += context.getConvidados()

    titulo_compromisso = context.Title()
    link_agenda = '%s/minha-agenda' % context.portal_url()
    data_compromisso =  '%s às %s' %(context.start_datetime.strftime('%d/%m/%Y %H:%M'),
                                     context.end_datetime.strftime('%d/%m/%Y %H:%M'))

    if is_edit:
        assunto = 'O Compromisso %s foi editado.' % titulo_compromisso
    else:
        assunto = 'O Compromisso %s foi criado.' % titulo_compromisso

    msg = '''Olá, %s você acaba de ser convidado a participar do compromisso %s,
             que será realizado no pedíodo de  %s. <br/> 
            
             Para maiores informações acesse o <a href="%s"> link </a>.''' 

    for username in list_user:
        obj_user = tools.get_prefs_user(username)
        email = obj_user.get('email')

        if email:
            tools.envia_email(context, msg %(obj_user.get('name',username),
                                             titulo_compromisso,
                                             data_compromisso,
                                             link_agenda), assunto, email)

