from plone.app.layout.viewlets import ViewletBase
from datetime import datetime
import arrow

CONFERENCE_START_DATE = datetime(2015, 10, 12)


class DaysToConferenceViewlet(ViewletBase):

    def date(self):
        return CONFERENCE_START_DATE

    def human(self):
        return arrow.get(CONFERENCE_START_DATE).humanize()
# from ploneconf.site.behaviors.social import ISocial
#
class SocialViewlet(ViewletBase):
    pass

#     def lanyrd_link(self):
#         adapted = ISocial(self.context)
#         return adapted.lanyrd
