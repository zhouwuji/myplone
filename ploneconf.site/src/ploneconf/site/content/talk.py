from plone.dexterity.content import Container
from ploneconf.site.interfaces import ITalk
from zope.interface import implementer

@implementer(ITalk)
class Talk(Container):
    """Class for Talks"""
