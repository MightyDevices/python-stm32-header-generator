from collections import namedtuple

# header processor class
class HeaderProcessor:
    # constructor
    def __init__(self, name):
        self.name = name
    # build #define entry
    @staticmethod
    def _define(label, value=''):
        return {'entry': 'define', 'label': label, 'value':value}
    # build a include entry
    @staticmethod
    def _include(self):
        return {'entry': ''}