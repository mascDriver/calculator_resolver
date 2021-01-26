import base64
import io
import urllib

from django.shortcuts import render
from sympy import Lambda, symbols, init_printing, plot, diff, Limit, Integral, pretty, limit, integrate, sqrt

x, xy, y = symbols('x, xy, y')


def home(request):
    init_printing()
    if request.POST:
        data = request.POST.get('expressao')
        print(request.POST)
        if request.POST.get('inlineRadioOptions') == 'derivada':
            try:
                return derivada(data, request)
            except:
                return render(request, 'derivada.html', {'erro': True})
        elif request.POST.get('inlineRadioOptions') == 'integral':
            try:
                return integral(data, request)
            except:
                return render(request, 'derivada.html', {'erro': True})
        elif request.POST.get('inlineRadioOptions') == 'limite':
                return limite(data, request)
        else:
            return render(request, 'derivada.html', {'erro': True, 'motivo': 'selecione um método de calculo'})
    return render(request, 'derivada.html')


def derivada(data, request):
    f = Lambda(x, data)
    derivada = diff(f(x), x)
    graph = image(f(x))
    uri = {
        'expressao': pretty(f.expr),
        'expressao_escrita': f.expr,
        'image': graph,
        'derivada': pretty(derivada),
        'derivada_escrita': derivada,
        'erro': False
    }
    return render(request, 'derivada.html', {'data': uri})


def limite(data, request):
    ponto = data.split('->')
    expressao = ponto[1].split('=')
    lim = Limit(expressao[1].strip(), ponto[0].strip(), expressao[0].strip())
    lim_img = limit(expressao[1].strip(), ponto[0].strip(), expressao[0].strip())
    uri = {
        'expressao': pretty(lim),
        'expressao_escrita': lim,
        'image': image(expressao[1].strip()),
        'derivada_escrita': lim.doit(),
        'erro': False
    }
    return render(request, 'derivada.html', {'data': uri})


def integral(data, request):
    integ = Integral(data, x)
    integ_img = integrate(data, x)
    uri = {
        'expressao': pretty(integ),
        'expressao_escrita': integ.args,
        'derivada_escrita': integ.doit(),
        'image': image(integ_img),
        'erro': False
    }
    return render(request, 'derivada.html', {'data': uri})


def image(f):
    image = plot(f, line_color='green', show=False)
    buf = io.BytesIO()
    image.save(buf)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    graph = urllib.parse.quote(string)
    return graph