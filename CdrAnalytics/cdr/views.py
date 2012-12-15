import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from CdrAnalytics.cdr.forms import DateRangeForm, DateTimeRangeForm
from CdrAnalytics.cdr.models import *
from CdrAnalytics.raphycharts.charts import RaphyLineChart
from datetime import datetime


def get_plot(from_date, to_date):
    return RaphyLineChart(
            data=[
                (i[0], i[1])
                for i in MaxConCallCountPerHour.objects.filter(
                    hour__gte=from_date, hour__lt=to_date
                    ).order_by('hour').values_list
                ('hour', 'max_con_count')
            ], x_axis_type="date"
    )


def max_con_call_analytics(request):
    plot = None
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            plot = get_plot(form.cleaned_data['from_date'],
                    form.cleaned_data['to_date'])
    else:
        form = DateRangeForm()
    return render_to_response('cdr/max_con_call_analytics.html',
            {'form': form, 'plot': plot},
            context_instance=RequestContext(request))


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
