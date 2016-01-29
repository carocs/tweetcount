from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import twittercontroller, reportcontroller
from .forms import CoordForm, ReportForm
import thread

# Create your views here.
def index(request):
    return search(request)

def search(request):
    if request.method =='POST':
        form = CoordForm(request.POST)
        if form.is_valid():
            lista = twittercontroller.search_tweets(request.POST['coordx'],request.POST['coordy'])
            thread.start_new(twittercontroller.search_tweets_week,(request.POST['coordx'],request.POST['coordy']))
            context = {'form':form, 'lista': lista}
            return render(request,'tweeter/search.html',context)

    else:
        form = CoordForm()
    context = {'form':form}
    return render(request,'tweeter/search.html',context)

def report(request):
    if request.method == 'POST':
        form1=ReportForm(request.POST)

        if form1.is_valid(request.POST['dataInicio'],request.POST['dataFim']):
            print 'antess'
            result = reportcontroller.generate_report(request.POST['dataInicio'],
                                                       request.POST['dataFim'],request.POST['dimensao'])

            context = { 'result': result,
                        'form1': form1
                        }
            context['dimensao'] = request.POST['dimensao']
            return render(request, 'tweeter/report.html',context)
    else:
        form1 = ReportForm()
        context = {'form1': form1}
        return render(request,'tweeter/report.html', context)



