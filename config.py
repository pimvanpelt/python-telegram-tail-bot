'''

'''

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pttb.config')
logger.addHandler(NullHandler())

class Config():
    def __init__(self, config='/etc/pttb/pttb.yaml'):
        self.config = config
        self.triggers=[]
        self.silences=[]

    def read(self):
        logger.debug("Reading config from %s" % self.config)
        return False

    def write(self):
        logger.debug("Writing config to %s" % self.config)
        return False

    def trigger_list(self):
        logger.debug("Returning trigger list ..")
        return self.triggers

    def trigger_add(self, regexp, duration=10):
        logger.debug("Adding trigger '%s' duration %d" % regexp, duration)
        return False

    def trigger_del(self, idx):
        logger.debug("Removing trigger index %d" % idx)
        return False

    def silence_list(self):
        logger.debug("Returning silence list ..")
        return self.silences

    def silence_add(self, regexp, duration=10):
        logger.debug("Adding silence '%s' duration %d" % regexp, duration)
        return False

    def silence_del(self, idx):
        logger.debug("Removing silence index %d" % idx)
        return False
