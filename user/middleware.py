import datetime


class ActivityMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            today = datetime.date.today()
            profile = request.user.get_profile()
            if profile.last_active is None:
                try:
                    profile.last_active = today
                    profile.save()
                except:
                    pass

            if profile.last_active is not None \
                    and profile.last_active < today:
                profile.last_active = today
                profile.save()