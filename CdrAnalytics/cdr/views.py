import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from CdrAnalytics.cdr.forms import DateRangeForm, DateTimeRangeForm
from CdrAnalytics.cdr.models import *
from datetime import datetime


def get_plot(from_date, to_date):
    return {
            'plots': [
                        (datetime.strftime(i[0], '%Y-%m-%d %I:00%p'), i[1])
                        for i in MaxConCallCountPerHour.objects.filter(
                            hour__gte=from_date, hour__lt=to_date
                            ).order_by('hour').values_list
                        ('hour', 'max_con_count')
                     ],
            'min_date': datetime.strftime(from_date, '%b %d, %Y'),
            'max_date': datetime.strftime(to_date, '%b %d, %Y')
    }


def max_con_call_analytics(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            plot = get_plot(form.cleaned_data['from_date'],
                    form.cleaned_data['to_date'])
            return HttpResponse(json.dumps(plot), mimetype="application/json")
    else:
        form = DateRangeForm()
    return render_to_response('cdr/max_con_call_analytics.html',
            {'form': form}, context_instance=RequestContext(request))


def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))


def pi_call_stats_analytics(request):
    if request.method == "POST":
        form = DateTimeRangeForm(request.POST)
        if form.is_valid():
            plot = CallDetailRecord.objects.get_status_counts(
                    form.cleaned_data['from_time'],
                    form.cleaned_data['to_time']
                )
            return HttpResponse(json.dumps(plot), mimetype="application/json")
    else:
        form = DateTimeRangeForm()
    return render_to_response('cdr/pi_call_stats.html',
            {'form': form}, context_instance=RequestContext(request))
