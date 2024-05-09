# views.py
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger    
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
import requests


def device_logs(request):
    # Get fromDate and toDate from request parameters
    from_date = request.GET.get('fromDate')
    to_date = request.GET.get('toDate')

    # Validate fromDate and toDate
    if from_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponseBadRequest("Invalid fromDate format. Please use YYYY-MM-DD.")
    else:
        from_date = datetime.today().date()

    if to_date:
        try:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponseBadRequest("Invalid toDate format. Please use YYYY-MM-DD.")
    else:
        to_date = datetime.today().date()

    # Fetch data from the API using settings.API_URL and settings.API_KEY
    api_url = settings.API_URL
    api_key = settings.API_KEY
    params = {
        "APIKey": api_key,
    }
    # Include fromDate and toDate in params if they are provided
    if from_date:
        params["FromDate"] = from_date.strftime('%Y-%m-%d')
    if to_date:
        params["ToDate"] = to_date.strftime('%Y-%m-%d')

    response = requests.get(api_url, params=params)
    data = response.json()
    # By passing Pagination. To enable it comment out the next line 47 and uncomment the rest of the lines.
    # return render(request, 'device_logs.html', {'logs': data})
    # Paginate the data
    paginator = Paginator(data, 10)  # Show 10 logs per page
    page_number = request.GET.get('page')
    try:
        logs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    return render(request, 'device_logs.html', {'logs': logs, 'fromDate': from_date, 'toDate': to_date})
