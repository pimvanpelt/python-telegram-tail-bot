'''
Copyright (c) 2022 Pim van Pelt
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
