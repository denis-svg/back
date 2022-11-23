from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import AvgEvents, PersonsMetric, UrlsMetric, Persons, Events
from api.serializers import EventHoursSerializer, UrlSerializer, EventTypesSerializer
from django.db.models import Count, Avg

@api_view(['GET'])
def getEventHours(request):
    event_name = request.GET.get('name')
    locale = request.GET.get('locale')
    device = request.GET.get('device')
    if event_name is None:
        event_name = 'conversion'
    if locale and device:    "value": 12
        q = AvgEvents.objects.select_related('event').select_related('event__person').values('hour').filter(
            event__event_name=event_name).filter(event__person__locale=locale).filter(event__person__device=device).annotate(count=Count('hour'))
    elif locale:
        q = AvgEvents.objects.select_related('event').select_related('event__person').values('hour').filter(
            event__event_name=event_name).filter(event__person__locale=locale).annotate(count=Count('hour'))
    elif device:
        q = AvgEvents.objects.select_related('event').select_related('event__person').values('hour').filter(
            event__event_name=event_name).filter(event__person__device=device).annotate(count=Count('hour'))
    else:
        q = AvgEvents.objects.select_related('event').values('hour').filter(event__event_name=event_name).annotate(count=Count('hour'))
    serializer = EventHoursSerializer(q, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def geteventsBy(request):
    event_name = request.GET.get('name')
    if event_name is None:
        event_name = 'conversion'
    device = request.GET.get('device')
    q = Events.objects.select_related('person').values('person__locale').annotate(count=Count('person__locale')).filter(event_name=event_name).order_by('-count')
    print(q)
    serializer = EventTypesSerializer(q, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def personsCount(request):
    metric = request.GET.get('metric')
    locale = request.GET.get('locale')
    device = request.GET.get('device')
    flag = request.GET.get('flag')
    master = request.GET.get('master')
    if flag is None:
        flag = 'false'
    if metric is None:
        metric = 'convert'
    if flag.lower() == 'false':
        flag = False
    else:
        flag = True
    if master:
        if master.lower() == 'false':
            master = False
        elif master.lower() == 'true':
            master = True
    if device and locale:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__locale=locale)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__locale=locale)
    elif device:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag)
    elif locale:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__locale=locale)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__locale=locale)
    else:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag)
    response = {"metric": metric, "metric_isnull":flag, "device":device, "locale":locale, "master_isnull":master, "count":q.count()}
    return Response(response)

@api_view(['GET'])
def personsAvg(request):
    metric = request.GET.get('metric')
    locale = request.GET.get('locale')
    device = request.GET.get('device')
    master = request.GET.get('master')
    time = request.GET.get('time')
    if time is None:
        time = False
    else:
        time = True
    flag = False
    if metric is None:
        metric = 'convert'
    if master:
        if master.lower() == 'false':
            master = False
        elif master.lower() == 'true':
            master = True
    if device and locale:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__locale=locale)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__locale=locale)
    elif device:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToConvert__isnull=flag)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(person__device=device).filter(clicksToShare__isnull=flag)
    elif locale:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__locale=locale).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__locale=locale)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__locale=locale)
    else:
        if master is not None:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag).filter(person__master_id__isnull=master)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag).filter(person__master_id__isnull=master)
        else:
            if metric == 'clicksToConvert' or metric == 'convert':
                q = PersonsMetric.objects.select_related('person').filter(clicksToConvert__isnull=flag)
            elif metric == 'clicksToShare' or metric == 'share':
                q = PersonsMetric.objects.select_related('person').filter(clicksToShare__isnull=flag)
    if metric == 'convert':
        metric = 'clicksToConvert'
    elif metric == 'share':
        metric = 'clicksToShare'
    if time:
        if metric == 'clicksToConvert':
            metric = 'timeToConvert'
        else:
            metric = 'timeToShare'
    response = {"metric": metric, "device":device, "locale":locale, "master_isnull":master, "avg":list(q.aggregate(Avg(metric)).values())[0]}
    return Response(response)

@api_view(['GET'])
def urls(request):
    locale = request.GET.get("locale")
    device = request.GET.get("device")
    n = request.GET.get("n")
    q = UrlsMetric.objects.filter(ratio_clicks__lt=1).filter(ratio_time__lt=1).filter(device=device).filter(locale=locale)
    avg = list(q.aggregate(Avg('ratio_time')).values())[0]
    
    if n is not None:
        if device is None and locale:
            q = UrlsMetric.objects.filter(ratio_clicks__lt=1).filter(ratio_time__lt=avg).filter(device=device).filter(locale=locale).order_by('-total_clicks')[:int(n)*3:3]
        else:
            q = UrlsMetric.objects.filter(ratio_clicks__lt=1).filter(ratio_time__lt=avg).filter(device=device).filter(locale=locale).order_by('-total_clicks')[:int(n)]
    else:
        if device is None and locale:
            q = UrlsMetric.objects.filter(ratio_clicks__lt=1).filter(ratio_time__lt=avg).filter(device=device).filter(locale=locale).order_by('-total_clicks')[:int(len(q))*3:3]
        else:
            q = UrlsMetric.objects.filter(ratio_clicks__lt=1).filter(ratio_time__lt=avg).filter(device=device).filter(locale=locale).order_by('-total_clicks')
    serializer = UrlSerializer(q, many=True)
    return Response(serializer.data)