import models
from dateutil import parser
import datetime

def generate_report (dataInicio, dataFim, dimensao):
    lista =[]
    if dimensao == 'data':
        for linha in models.TweetsPorData.objects.all().values_list():
            aux = models.TweetsPorData()
            aux.data = linha[1]
            aux.ntweets = linha[2]
            aux.nchars = linha[3]
            aux.nwords = linha[4]
            aux.top3wrds = linha[5]
            lista.append(aux)
    return lista