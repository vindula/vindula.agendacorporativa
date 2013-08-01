# coding: utf-8
from five import grok
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

import json
from datetime import datetime
from copy import copy

grok.templatedir('templates')

class MyAgendaView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('minha-agenda')

    def __init__(self,context,request):
        super(MyAgendaView,self).__init__(context,request)
        self.portal_membership = getToolByName(context, 'portal_membership')
        self.static = context.absolute_url() + '/++resource++vindula.agendacorporativa'

    def getHomeFolder(self):
        folder = self.portal_membership.getHomeFolder()
        if folder:
            return folder.absolute_url()

        return ''

    def checkHomeFolder(self):
        """ Check if exist homeFolder """
        homefolder = self.portal_membership.getHomeFolder()
        if homefolder:
            return True
        else:
            return False

class MyCommitmentView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('my_events')        

    retorno = []

    def render(self):
        self.request.response.setHeader("Content-type","application/json")
        self.request.response.setHeader("charset", "UTF-8")
        return json.dumps(self.retorno,ensure_ascii=False)

    def update(self):
        context = self.context

        ctool = getToolByName(context, 'portal_catalog') 
        membership = getToolByName(context, 'portal_membership') 

        path = context.portal_url.getPortalObject().getPhysicalPath()

        user_logado = membership.getAuthenticatedMember()
        username = user_logado.getUserName()

        query = {'path': {'query':'/'.join(path)},
                 'portal_type': ('Commitment',),
                 'sort_on':'created',
                 'sort_order':'descending',
                 }

        #Busca por conpromissos do probrio usuario
        query1 = copy(query)
        query1['Creator'] = username 
        result1 = ctool(**query1)

        #Busca por compromissos que o usuario participa
        query2 = copy(query)
        query2['getConvidados'] = [username]
        result2 = ctool(**query2)

        result = result1 + result2
        L =[]

        for item in result:
            obj = item.getObject()
            data_evento = '%s às %s' %(obj.start_datetime.strftime('%d/%m/%Y %H:%M'),
                                       obj.end_datetime.strftime('%d/%m/%Y %H:%M'))
            descricao = '''<span> <b>Descrição:</b> %s <br />\n
                                 <b>Data:</b> %s <br />\n
                                 <b>Local:</b> %s <br />\n
                       </span>''' %(obj.Description(),data_evento, obj.getLocation())

            if obj.getOwner().getUserName() == username:
                read_more = '''
                               <span> <br />\n
                                  <a href="%s" style="text-decoration: underline;">
                                    <i>Editar seu compromisso</i>
                                  </a><br />\n
                               </span>''' %(obj.absolute_url()+'/edit')

                descricao += read_more

            allday = (obj.getEnd_datetime() - obj.getStart_datetime()) > 1.0
            event = {"id": "UID_%s" % obj.UID(),
                     "title": obj.Title(),
                     "description": descricao,
                     "start": obj.getStart_datetime().rfc822(),
                     "end": obj.getEnd_datetime().rfc822(),
                     "url": obj.absolute_url(),
                     "allDay" : allday
                     }

            L.append(event)

        self.retorno = L
