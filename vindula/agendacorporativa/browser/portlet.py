# coding: utf-8
from five import grok
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from AccessControl.SecurityManagement import newSecurityManager, getSecurityManager, setSecurityManager
from vindula.agendacorporativa.browser.search import busca_commitment

grok.templatedir('templates')

class PortletMyAgendaView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('portlet_agenda')


    def retorno(self):
    	
    	context = self.context
        membership = getToolByName(context, 'portal_membership') 

        user_admin = membership.getMemberById('admin')
        user_logado = membership.getAuthenticatedMember()
        username = user_logado.getUserName()
        
        # stash the existing security manager so we can restore it
        old_security_manager = getSecurityManager()
        
        # create a new context, as the owner of the folder
        newSecurityManager(self.request,user_admin)

        result = busca_commitment(context,username,True)

        # restore the original context
        setSecurityManager(old_security_manager)

        return result
