import base64
import io
import urllib

import matplotlib.pyplot as plt
from django.shortcuts import render
from sympy import *

x = symbols('x')
xy = symbols('xy')
y = symbols('y')
c = symbols('=')

def home(request):
    if request.POST:
        init_printing()
        data = request.POST.get('expressao')
        f = Lambda(x, data)
        derivada = diff(f(x), x)
        plt.plot(range(2))
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        graph = urllib.parse.quote(string)
        uri = {
            'image': graph,
            'derivada': pretty(derivada)
        }
        return render(request, 'derivada.html', {'data': uri})
    return render(request, 'derivada.html')