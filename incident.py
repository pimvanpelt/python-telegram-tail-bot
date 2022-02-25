'''

'''

import logging
import time
from datetime import datetime

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pttb.incident')
logger.addHandler(NullHandler())

global incident_counter
incident_counter = 0

class Incident():
    def __init__(self, trigger, duration, message):
        global incident_counter

        self.id = incident_counter
        incident_counter += 1
        self.trigger = trigger
        self.message = message
        self.duration = duration
        self.loglines = []
        self.created = time.time()
        self.expiry = self.created + self.duration

    def getid(self):
        return self.id

    def feedlog(self, logline):
        self.loglines.append(logline)
        pass

    def expired(self):
        expired = time.time() > self.expiry
        if expired:
            logger.debug("incident has expired")
            return True

        return False

    def render(self):
        ret = "Incident: %d\nMessage: %s\n\nLoglines:\n<pre>\n" % (self.id, self.message)
        for l in self.loglines:
            ret += l + "\n"
        ret += "</pre>\n"
        return ret
