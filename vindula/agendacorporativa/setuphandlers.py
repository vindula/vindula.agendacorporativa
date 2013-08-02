# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-vindula.agendacorporativa:default'

def set_AllowedType_Members(context):
    portal = context.getSite()
    Types = ['Folder','Image','File','Commitment'] 
    
    if 'Members' in portal.keys():
        folder_members = portal['Members']
        folder_members.setConstrainTypesMode(1) # 1 pasta com restrição de conteudo / 0 sem restrição de conteudo
        folder_members.setImmediatelyAddableTypes(Types)
        folder_members.setLocallyAllowedTypes(Types)
        
def create_index(context):

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it                                                                                  
    # is quite safe.
    ctx = context._site
    logger = logging.getLogger('vindula.agendacorporativa')

    catalog = getToolByName(ctx, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('getConvidados', 'KeywordIndex'),
			  )
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)

    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

    if 'getStart_datetime' in indexes:
        catalog.manage_reindexIndex(ids=['getStart_datetime'])