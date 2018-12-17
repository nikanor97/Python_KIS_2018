from collections import Generator
from random import randint


class Agent(Generator):
    
    def __init__(self, kb, name):
        self.kb = kb
        self.name = name
        self.inp = None

    def send(self, msg):
        l = len(self.kb)
        num = randint(1, l)
        return self.kb['text'][num - 1]
        
    def throw(self, typ=None, val=None, tb=None):
        super().throw(typ, val, tb)

    def __str__(self):
        return str("Agent(" + self.name + ")")

    def __repr__(self):
        return str(self)
