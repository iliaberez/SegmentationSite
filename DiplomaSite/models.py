from django.db import models

class ElementHistory(object):
    def __init__(self, numberPacient, Date, Disease):
        self.numberPacient = numberPacient
        self.Date = Date
        self.Disease = Disease