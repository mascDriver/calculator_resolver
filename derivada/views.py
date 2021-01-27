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
        if request.POST.get('inlineRadioOptions') == 'derivada':
                return derivada(data, request)
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
    graph = None
    try:
        derivate = data.split('=')
        print(derivate)
        f = Lambda(x, derivate[0].strip())
        x0 = float(derivate[1].strip())
        print(derivate[1])
        fl = Lambda(x, diff(f(x), x))
        r = Lambda(x, fl(x0) * (x - x0) + f(x0))
        p = plot(f(x), (x, -2, 2), line_color='green', show=False)
        q = plot(r(x), (x, -1.5, 1), line_color='red', show=False)
        p.extend(q)
        buf = io.BytesIO()
        p.save(buf)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        graph = urllib.parse.quote(string)
    except:
        derivate = data
        f = Lambda(x, derivate)
    deriv = diff(f(x), x)
    uri = {
        'expressao': pretty(f.expr),
        'expressao_escrita': f.expr,
        'image': graph or image(f(x)),
        'derivada': pretty(deriv),
        'derivada_escrita': deriv,
        'erro': False
    }
    return render(request, 'derivada.html', {'data': uri})


def limite(data, request):
    ponto = data.split('->')
    expressao = ponto[1].split('=')
    lim = Limit(expressao[1].strip(), ponto[0].strip(), expressao[0].strip())
    uri = {
        'expressao': pretty(lim),
        'expressao_escrita': lim,
        'image': image(lim.doit()),
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