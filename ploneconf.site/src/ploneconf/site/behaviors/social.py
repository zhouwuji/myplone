# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class ISocial(model.Schema):

    directives.fieldset(
        'social',
        label=u'Social',
        fields=('lanyrd',),
    )

    lanyrd = schema.URI(
        title=u"Lanyrd link",
        description=u"Add URL",
        required=False,
    )
