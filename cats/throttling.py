from rest_framework import throttling

import datetime


class WorkingHoursRateThrottle(throttling.BaseThrottle):

    def allow_request(self,request,view):
        now = datetime.datetime.now().hour
        if now>=13 and now<16:
            return False
        return True
