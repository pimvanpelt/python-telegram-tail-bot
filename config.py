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
import yaml
import time
from datetime import datetime

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pttb.config')
logger.addHandler(NullHandler())

class Config():
    def __init__(self, config='/etc/pttb/pttb.yaml'):
        self.config = config
        self.yaml = None

    def read(self):
        logger.debug("Reading config from %s" % self.config)
        try:
          with open(self.config, "r") as f:
              self.yaml = yaml.load(f, Loader = yaml.FullLoader)
              logger.debug("Config: %s" % self.yaml)
        except:
            logger.error("Couldn't read config from %s" % self.config)
            return False
        if not 'telegram' in self.yaml:
            logger.error("Missing telegram entry in %s" % self.config)
            return False
        if not 'token' in self.yaml['telegram']:
            logger.error("Missing telegram.token entry in %s" % self.config)
            return False
        if not 'chat-id' in self.yaml['telegram']:
            logger.error("Missing telegram.chat-id entry in %s" % self.config)
            return False
        if not 'triggers' in self.yaml:
            self.yaml['triggers'] = []
        if not 'silences' in self.yaml:
            self.yaml['silences'] = []
        return True

    def write(self):
        logger.debug("Writing config to %s" % self.config)
        return False

    def token_get(self):
        try:
            return self.yaml['telegram']['token']
        except:
            return ""

    def chatid_get(self):
        try:
            return int(self.yaml['telegram']['chat-id'])
        except:
            return 0

    def trigger_list(self):
        return self.yaml['triggers']

    def trigger_exists(self, regexp):
        idx=0
        for t in self.yaml['triggers']:
            if t['regexp'] == regexp:
                logger.warning("trigger '%s' exists at idx %d" % (regexp, idx))
                return True
            idx += 1
        return False

    def trigger_add(self, regexp, duration=10, message=""):
        if self.trigger_exists(regexp):
            msg = "trigger '%s' already exists" % regexp
            logger.warning(msg)
            return [False, msg]

        self.yaml['triggers'].append({"regexp": regexp, "duration": duration, "message": message })
        msg = "added trigger '%s' duration %d message '%s'" % (regexp, duration, message)
        logger.debug(msg)
        return [True,msg]

    def trigger_del(self, idx):
        if idx < 0 or idx >= len(self.yaml['triggers']):
          msg = "trigger idx out of bounds (0..%d)" % (len(self.yaml['triggers'])-1)
          logger.warning(msg)
          return [False, msg]

        del self.yaml['triggers'][idx]
        msg = "removed trigger index %d" % idx
        logger.debug(msg)
        return [True, msg]

    def silence_list(self):
        return self.yaml['silences']

    def silence_exists(self, regexp):
        idx=0
        for t in self.yaml['silences']:
            if t['regexp'] == regexp:
                logger.warning("silence '%s' exists at idx %d" % (regexp, idx))
                return True
            idx += 1
        return False

    def silence_add(self, regexp, duration=3600, message=""):
        logger.debug("Adding silence '%s' duration %d message '%s'" % (regexp, duration, message))
        if self.silence_exists(regexp):
            msg = "silence '%s' already exists" % regexp
            logger.warning(msg)
            return [False, msg]

        expiry = time.time() + duration
        self.yaml['silences'].append({"regexp": regexp, "expiry": expiry, "message": message })
        expiry_str = datetime.utcfromtimestamp(expiry).strftime('%Y-%m-%d %H:%M:%S UTC')
        msg = "added silence '%s' expiry '%s' message '%s'" % (regexp, expiry_str, message)
        return [True, msg]

    def silence_del(self, idx):
        if idx < 0 or idx >= len(self.yaml['silences']):
          msg = "silence idx out of bounds (0..%d)" % (len(self.yaml['silences'])-1)
          logger.warning(msg)
          return [False, msg]

        del self.yaml['silences'][idx]
        msg = "removed silence index %d" % idx
        logger.debug(msg)
        return [True, msg]
