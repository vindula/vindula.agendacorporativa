# coding: utf-8
from five import grok
from vindula.agendacorporativa.content.interfaces import ICommitment

from Products.CMFCore.utils import getToolByName

from datetime import datetime

grok.templatedir('templates')

class CommitmentView(grok.View):
    grok.context(ICommitment)
    grok.require('zope2.View')
    grok.name('view')