from django import forms
from models import TweetsPorData
from dateutil import parser
import datetime

class CoordForm(forms.Form):
    coordx = forms.CharField(label='Latitude:', max_length=20)
    coordy = forms.CharField(label='Longitude:', max_length=20)

class ReportForm(forms.Form):
    dataInicio = forms.ChoiceField(choices=[],)
    dataFim = forms.ChoiceField(choices=[])
    dimensao = forms.ChoiceField(choices=[('data','Data') , ('user','Usuario'), ('local','Local')])

    def is_valid(self,dInicio,dFim):
        if not super(ReportForm,self).is_valid():
            return False

        if parser.parse(dFim) < parser.parse(dInicio):
            return False
        else:
            return True


    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        datas = TweetsPorData.objects.all().values_list("data","data").distinct()
        l= []
        for k,v in datas:
            l.append((k.isoformat(),k.isoformat()))

        self.fields['dataInicio'].choices = sorted(l,key=lambda tup: tup[1])
        self.fields['dataFim'].choices = sorted(l,reverse=True,key=lambda tup: tup[1])