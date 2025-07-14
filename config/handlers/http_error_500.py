import traceback, sys, json

import emails as send_email

from django.shortcuts import render
from django.http import QueryDict


def http_error_500(request):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    def safe_dict_repr(d):
        if hasattr(d, 'dict'):
            return d.dict()
        if isinstance(d, QueryDict):
            return dict(d.lists())
        return dict(d)
    
    headers = safe_dict_repr(request.headers)

    if request.method == 'GET': params = safe_dict_repr(request.GET)
    elif request.method == 'POST': params = safe_dict_repr(request.POST)
    elif request.method == 'PUT': params = safe_dict_repr(request.PUT)
    elif request.method == 'DELETE': params = safe_dict_repr(request.DELETE)
    elif request.method == 'PATCH': params = safe_dict_repr(request.PATCH)
    else: params = {}
    
    send_email.dev.handle_error_500(request, {
        'site_name': 'Sasori imports',
        'request': request,
        'headers': json.dumps(headers, indent=2, ensure_ascii=False),
        'params': json.dumps(params, indent=2, ensure_ascii=False),
        'error_traceback': error_traceback,
    })
     
    return render(request, 'errors/500.html', status=500)