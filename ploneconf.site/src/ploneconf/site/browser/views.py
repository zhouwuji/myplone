from Products.Five.browser import BrowserView
from operator import itemgetter
from plone import api
from plone.dexterity.browser.view import DefaultView
import transaction


class DemoView(BrowserView):

    def the_title(self):
        s = 'hello'
        # import pdb;pdb.set_trace()
        # s = u'A list of great trainings:'
        # s = self.econtext.user
        brains = api.content.find(context=self.context)
        brain = brains[0]
        obj = brain.getObject()
        # obj.click
        transaction.commit()
        return s

    # def get_user(self):
    #     return self.econtext.user

    def talks(self):
        results = []
        data = [
            {'title': 'Dexterity is the new default!',
             'subjects': ('content-types', 'dexterity')},
            {'title': 'Mosaic will be the next big thing.',
             'subjects': ('layout', 'deco', 'views'),
             'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
            {'title': 'The State of Plone',
             'subjects': ('keynote',)},
            {'title': 'Diazo is a powerful tool for theming!',
             'subjects': ('design', 'diazo', 'xslt')},
            {'title': 'Magic templates in Plone 5',
             'subjects': ('templates', 'TAL'),
             'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'},
        ]
        for item in data:
            try:
                url = item['url']
            except KeyError:
                url = 'https://www.google.com/search?q=%s' % item['title']
            talk = dict(
                title=item['title'],
                subjects=', '.join(item['subjects']),
                url=url
            )
            results.append(talk)
        return sorted(results, key=itemgetter('title'))

    def context_info(self):
        context = self.context
        title = context.title
        portal_type = context.portal_type
        url = context.absolute_url()
        return u"This is the {0}, '{1}' at {2}".format(portal_type, title, url)




class SomeOtherView(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        some_talk = portal['dexterity-for-the-win']
        training_view = api.content.get_view('training', some_talk, self.request)
        return training_view.context_info()


class TalkView(DefaultView):
    """ The default view for talks"""
    def set_click(self):
        brains = api.content.find(context=self.context)
        brain = brains[0]
        obj = brain.getObject()
        if hasattr(obj, 'click') and (obj.click==1):
            return
        else:
            obj.click = 1
            transaction.commit()
    def get_click(self):
        brains = api.content.find(context=self.context)
        brain = brains[0]
        obj = brain.getObject()
        if hasattr(obj, 'click'):
            return obj.click
        else:
            return None

class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        results = []
        brains = api.content.find(context=self.context, portal_type='talk')
        for brain in brains:
            talk = brain.getObject()
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'audience': ', '.join(talk.audience),
                'type_of_talk': talk.type_of_talk,
                'speaker': talk.speaker,
                'uuid': brain.UID,
            })
        return results

    def get_news(self):

        portal_catalog = api.portal.get_tool('portal_catalog')
        return portal_catalog(
            portal_type='News Item',
            review_state='published',
            sort_on='effective',
        )

    def keynotes(self):

        portal_catalog = api.portal.get_tool('portal_catalog')
        brains = portal_catalog(
            portal_type='Talk',
            review_state='published')
        results = []
        for brain in brains:
            # There is no catalog-index for type_of_talk so we must check
            # the objects themselves.
            talk = brain.getObject()
            if talk.type_of_talk == 'Keynote':
                results.append(talk)
        return results
