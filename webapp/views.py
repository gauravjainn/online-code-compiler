import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from webapp.models import CodeUrl, CodeHistory
from webapp.utils import get_or_none, HttpJSONResponse,\
 generate_unique_uri, code_compile_result, exception_handler



class Home(View):

    # @method_decorator(csrf_exempt)
    @method_decorator(exception_handler)
    def dispatch(self, request, *args, **kwargs):
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        data = {
            'lang_choices': dict(CodeUrl.LANGUAGE_CHOICES),
        }

        uri = kwargs.get('uri')

        if not uri:
            uri = generate_unique_uri()
            return HttpResponseRedirect('/{}'.format(uri))


        cu_obj = get_or_none(CodeUrl, uri=uri.strip("/"))

        if cu_obj is None:
            uri = generate_unique_uri()
            cu_obj = CodeUrl.objects.create(uri=uri)
            return HttpResponseRedirect('/{}'.format(uri))

        data.update({
            'lang': cu_obj.lang or 'PYTHON',
            'code': cu_obj.code,
            'inp': cu_obj.inp,
            'result': json.loads(cu_obj.result or '{}'),
            'uri': uri,
        })

        return render(request, 'home.html', data)

    # Uncomment this method if you dont want to use ajax api
    # and wants normal `submit and refresh` behaviour

    # def post(self, request, *args, **kwargs):
    #     uri = request.get_full_path()

    #     lang = request.POST.get('lang')
    #     code = request.POST.get('code')

    #     data = {
    #         'lang_choices': dict(CodeUrl.LANGUAGE_CHOICES),
    #         'lang': lang or "C",
    #         'code': code,
    #     }
    #     if not all([lang, code]):
    #         return render(request, 'home.html', data)


    #     resp = code_compile_result(lang, code)

    #     cu_obj, created = CodeUrl.objects.get_or_create(uri=uri.strip("/"))

    #     # if created:
    #     #     pass # To maintain history as well ?

    #     cu_obj.lang = request.POST.get('lang')
    #     cu_obj.code = request.POST.get('code')

    #     if resp.get('message') == 'OK':
    #         print resp['run_status']['output_html']
    #         cu_obj.result = json.dumps(resp['run_status'])
    #     else:
    #         cu_obj.result = resp.get('message') or "Error"  # there is a bug in Hackerearth API

    #     cu_obj.save()

    #     return HttpJSONResponse(data)


def source_compile_and_run(request):

    data = {'success': False}

    uri = request.GET.get('uri')
    lang = request.GET.get('lang')
    code = request.GET.get('code')
    inp = request.GET.get('inp')

    resp = code_compile_result(lang, code, inp)

    if resp is None:
        # Either net is too slow or hackerearth API is down
        data.update({'result': {'error': 'Network Error'}})
        return HttpJSONResponse(data)

    resp.pop('web_link', None)
    resp.pop('code_id', None)

    cu_obj, created = CodeUrl.objects.get_or_create(uri=uri.strip("/"))

    cu_obj.lang = lang
    cu_obj.code = code.strip()
    cu_obj.inp = inp

    if resp.get('message') == 'OK' or resp.get('compile_status') == 'OK':
        cu_obj.result = json.dumps(resp['run_status'])
        data['success'] = True
    else:
        cu_obj.result = json.dumps(resp or {'message': "Unknown Error"})
        # there is a bug in Hackerearth API ??

    cu_obj.save()

    # Maintain history
    CodeHistory.objects.create(uri=uri.strip("/"), lang=lang, code=code, inp=inp)

    data['result'] = json.loads(cu_obj.result) # or resp.get('run_status')
    return HttpJSONResponse(data)


def code_history(request, uri):
    data = CodeHistory.objects.filter(uri=uri).order_by('-created_at').values_list('lang', 'code', 'inp')
    # Consider pagination/infinite-scrolling

    no_data = False if len(data) > 0 else True

    return render(request, 'history.html', {'history_list': data, 'no_data': no_data})
