# -*- coding: utf-8 -*-
"""Definition of the MJ content type
"""

from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import base

from Products.ATContentTypes.content.event import ATEventSchema
from Products.ATContentTypes.content.file import ATFileSchema
from Products.ATContentTypes.interfaces import IATEvent, IATFile

from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.content import schemata

from plone.app.blob.field import BlobField, ImageField

# -*- Message Factory Imported Here -*-
from mj.agenda import agendaMessageFactory as _

from mj.agenda.interfaces.interfaces import IMJEvento
from mj.agenda.config import PROJECTNAME

ATFileSchema['file'].primary = False
ATFileSchema['file'].schemata = 'Arquivo'
ATFileSchema['file'].required = False

MJEventoSchema = ATEventSchema.copy() + ATFileSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name='event_categoria',
        required=False,
        searchable=True,
        schemata='categorization',
        widget=atapi.SelectionWidget(
            label=_(u"Categoria do evento"),
            description=_(u"Selecione a categoria do evento"),
            format='select',),
        vocabulary='getCategoria',
    ),

))


schemata.finalizeATCTSchema(MJEventoSchema, moveDiscussion=False)


class MJEvento(base.ATCTContent):
    """
    `"""
    implements(IMJEvento, IATEvent, IATFile)

    meta_type = "MJEvento"
    portal_type = 'MJEvento'
    schema = MJEventoSchema

    security = ClassSecurityInfo()

    def getCategoria(self):
        catalog = getToolByName(self, 'portal_catalog')
        categorias = catalog(portal_type='MJCategoria',
                           sort_on='id',)
        listCategorias = DisplayList()
        if categorias:
            listCategorias.add('', '')
            for i in categorias:
                categoria = i.Title
                cor = i.cor_categoria
                listCategorias.add(cor, categoria)
        return listCategorias


atapi.registerType(MJEvento, PROJECTNAME)
