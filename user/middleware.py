import datetime
from user.models import Profile


class ActivityMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            today = datetime.date.today()
            profile = request.user.profile
            if profile.last_active is None:
                profile.last_active = today
                profile.save()
            else:
                profile.last_active = today
                profile.save()
