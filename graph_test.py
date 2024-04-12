import ipywidgets
import numpy as np
import matplotlib.pyplot as plt
import math
from sympy import *
import multiprocessing
import asyncio


#def mirrored(maxval, inc=1):
#    x = np.arange(inc, maxval, inc)
#    if x[-1] != maxval:
#        x = np.r_[x, maxval]
#    return np.r_[-x[::-1], 0, x]
#
#def graph(formula, x_range1, x_range2):
#    average = math.ceil((abs(x_range1)+abs(x_range2))/2)
#    plots = 50*(average)
#    x = mirrored(plots, 0.01)
#    #x = np.linspace(x_range1, x_range2, plots)
#    print(x)
#    y = eval(formula)
#    plt.plot(x, y, label=f'y = {formula}')
#    for i in x:
#        if math.isnan(i):
#            plt.axvline(i)
#    plt.xlim(x_range1*2, x_range2*2)
#    plt.title(f'Graph of y = {formula}')
#    plt.xlabel('x-axis')
#    plt.ylabel('y-axis')
#    plt.grid(alpha=.4, linestyle='--')
#    plt.legend()
#    plt.show()
#
#graph('1/(x+1)', -1.5, 1.5)


#def linear(w,x,b):
#    return w*x + b
#
#def logistic(z):
#    return 1/(1+math.e**(-z))
#
#def plt_logistic(a, b):
#    x = np.linspace(-20,20, 100)
#    h = linear(a,x,b)
#    y = logistic(h)
#    plt.ylim(-5,5)
#    plt.xlim(-5,5)
#    plt.plot(x,h)
#    plt.plot(x,y)
#    plt.grid()
#    plt.show()
#
#
#ipywidgets.interact(plt_logistic, a = (-10,10,0.1), b = (-10,10,0.1))



#def integral(symbol, upper_limit=None, lower_limit=None):
#    print(f'{upper_limit} {lower_limit}')
#    init_printing(use_unicode=False, wrap_line=False)
#    x = Symbol(symbol, positive=True)
#    if upper_limit and lower_limit:
#        return integrate(x**2, (x, lower_limit, upper_limit))
#    else:
#        return integrate(x**2, x)
#
#print(integral('x', 1, 0))

def eqn_formatter(eqn, desmos=False, maths=False, string=False, der=False, double_der=False):
    if desmos:
        if 'sin^-1(' in eqn or 'asin(' in eqn:
            eqn = eqn.replace('sin^-1', r'\\arcsin')
        if 'cos^-1(' in eqn or 'acos(' in eqn:
            eqn = eqn.replace('cos^-1', r'\\arccos')
        if 'tan^-1(' in eqn or 'atan(' in eqn:
            eqn = eqn.replace('tan^-1', r'\\arctan')
        if 'E' in eqn:
            eqn = eqn.replace('E', 'e')
        if 'pi' in eqn:
            eqn = eqn.replace('pi', r'\\pi')
        if '**' in eqn:
            eqn = eqn.replace('**', '^')
        if 'sqrt(' in eqn:
            eqn = eqn.replace('sqrt(', r'\\sqrt(')
        if 'abs(' in eqn:
            eqn = eqn.replace('sqrt(', r'\\abs(')
        if 'y=' not in eqn:
            eqn = f'y={eqn}'
    if maths:
        if 'sin^-1(' in eqn:
            eqn = eqn.replace('sin^-1', 'asin')
        if 'cos^-1(' in eqn:
            eqn = eqn.replace('cos^-1', 'acos')
        if 'tan^-1(' in eqn:
            eqn = eqn.replace('tan^-1', 'atan')
        if 'e' in eqn:
            eqn = eqn.replace('e', 'E')
        if '^' in eqn:
            eqn = eqn.replace('^', '**')
        if 'y=' in eqn:
            eqn = eqn.replace('y=', '')
    if string:
        eqn = str(eqn)
        if 'asin(' in eqn:
            eqn = eqn.replace('asin', 'sin^-1')
        if 'acos(' in eqn:
            eqn = eqn.replace('acos', 'cos^-1')
        if 'atan' in eqn:
            eqn = eqn.replace('atan', 'tan^-1')
        if 'E' in eqn:
            eqn = eqn.replace('E', 'e')
        if '**' in eqn:
            eqn = eqn.replace('**', '^')
        if 'y=' not in eqn:
            if der:
                y = "y'"
            if double_der:
                y = "y''"
            eqn = f'{y}={eqn}'
    return eqn



def desmos_html_creator(desmos_eqn, eqn_str, eqn_values, desmos_der, der_values, desmos_double_der, double_der_values, eqn_asymptotes, der_asymptotes, double_der_asymptotes):
    eqn_xvals_table = ['<th class="tg-0lax">x</th>']
    eqn_yvals_table = ['<th class="tg-0lax">y</th>']
    der_xvals_table = ['<th class="tg-0lax">x</th>']
    der_yvals_table = ['<th class="tg-0lax">y\'</th>']
    double_der_xvals_table = ['<th class="tg-0lax">x</th>']
    double_der_yvals_table = ['<th class="tg-0lax">y\'\'</th>']


    for x, y in eqn_values.items():
        eqn_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        eqn_yvals_table.append(f'<th class="tg-0lax">{y}</th>')
    for x, y in der_values.items():
        der_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        der_yvals_table.append(f'<th class="tg-0lax">{y}</th>')
    for x, y in double_der_values.items():
        double_der_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        double_der_yvals_table.append(f'<th class="tg-0lax">{y}</th>')


    x_values_table_str = '\n			'.join(eqn_xvals_table)
    y_values_table_str = '\n			'.join(eqn_yvals_table)
    der_xvals_table_str = '\n			'.join(der_xvals_table)
    der_yvals_table_str = '\n			'.join(der_yvals_table)
    double_der_xvals_table_str = '\n			'.join(double_der_xvals_table)
    double_der_yvals_table_str = '\n			'.join(double_der_yvals_table)

    inFile = open('template.html')
    html = inFile.read()
    inFile.close()

    curves = []
    eqn_limits = []
    der_limits = []
    double_der_limits = []
    curves.append(f"calculator.setExpression({{ id: 'original', latex: '{desmos_eqn}', lineStyle: Desmos.Styles.SOLID }});")
    curves.append(f"calculator.setExpression({{ id: 'derivative', latex: '{desmos_der}', lineStyle: Desmos.Styles.SOLID }});")
    curves.append(f"calculator.setExpression({{ id: 'double-derivative', latex: '{desmos_double_der}', lineStyle: Desmos.Styles.SOLID }});")


    h_eqn_asymp = eqn_asymptotes['h']
    v_eqn_asymp = eqn_asymptotes['v']
    if h_eqn_asymp['oo'][0] != 'oo' and h_eqn_asymp['oo'][0] != '-oo':
        curves.append(f"calculator.setExpression({{ id: 'h_asymp_1', latex: 'y={h_eqn_asymp['oo'][0]}', lineStyle: Desmos.Styles.DASHED }});")
    if h_eqn_asymp['-oo'] != 'oo' and h_eqn_asymp['-oo'] != '-oo' and h_eqn_asymp['-oo'] != h_eqn_asymp['oo']:
        curves.append(f"calculator.setExpression({{ id: 'h_asymp_2', latex: 'y={h_eqn_asymp['-oo'][0]}', lineStyle: Desmos.Styles.DASHED }});")
    for x, y in h_eqn_asymp.items():
        eqn_limits.append(f'As x --> {x}, y --> {y[1]}.  ')
    eqn_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            curves.append(f"calculator.setExpression({{ id: 'v_asymp_{x}', latex: 'x={x}', lineStyle: Desmos.Styles.DASHED }});")
            eqn_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}.  ')
            eqn_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}.  ')
    else:
        eqn_limits.append('This equation has no vertical asymptotes')
    eqn_limits.append('<div class="space"></div>')

    h_eqn_asymp = der_asymptotes['h']
    v_eqn_asymp = der_asymptotes['v']
    for x, y in h_eqn_asymp.items():
        der_limits.append(f'As x --> {x}, y --> {y[1]}\n')
    der_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            der_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}')
            der_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}')
    else:
        der_limits.append('This equation\'s derivative has no vertical asymptotes')
    der_limits.append('<div class="space"></div>')

    h_eqn_asymp = double_der_asymptotes['h']
    v_eqn_asymp = double_der_asymptotes['v']
    for x, y in h_eqn_asymp.items():
        double_der_limits.append(f'As x --> {x}, y --> {y[1]}\n')
    double_der_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            double_der_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}')
            double_der_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}')
    else:
        double_der_limits.append('This equation\'s double derivative has no vertical asymptotes')
    double_der_limits.append('<div class="space"></div>')


    curves_str = '\n		'.join(curves)
    html = html.replace("__EQUATIONS_HERE__", f'<h1>{curves_str}</h1>')
    eqn_limits_str = '\n	'.join(eqn_limits)
    der_limits_str = '\n	'.join(der_limits)
    double_der_limits_str = '\n	'.join(double_der_limits)
    html = html.replace("__EQN_LIMITS__", f'<h1>{eqn_limits_str}</h1>')
    html = html.replace("__DER_LIMITS__", f'<h1>{der_limits_str}</h1>')
    html = html.replace("__DOUBLE_DER_LIMITS__", f'<h1>{double_der_limits_str}</h1>')

    html = html.replace('XVALUES_HERE', x_values_table_str)
    html = html.replace('YVALUES_HERE', y_values_table_str)
    html = html.replace('DERIVATIVE_X_VALUES_HERE', der_xvals_table_str)
    html = html.replace('DERIVATIVE_Y_VALUES_HERE', der_yvals_table_str)
    html = html.replace('DOUBLE_DEV_X_VALUES_HERE', double_der_xvals_table_str)
    html = html.replace('DOUBLE_DEV_Y_VALUES_HERE', double_der_yvals_table_str)

    html = html.replace('__MAIN_EQUATION__', f'<h1>MAIN EQUATION: {eqn_str}</h1>')
    html = html.replace('__DERIVATIVE_EQN__', f'<h1>DERIVATIVE EQUATION: {eqn_formatter(eqn_formatter(desmos_der, maths=True), string=True, der=True)}</h1>')
    html = html.replace('__DOUBLE_DER_EQN__', f'<h1>MAIN EQUATION: {eqn_formatter(eqn_formatter(desmos_double_der, maths=True), string=True, double_der=True)}</h1>')

    outFile = open('test_2.html', 'w')
    outFile.write(html)
    outFile.close()



def table_builder(discons, eqn, x):
    eqn_values = {}
    x_values = []
    y_values = []
    if discons:
        for value in discons:
            for i in range(-3, 4):
                a = value + i
                if a not in eqn_values.keys():
                    eqn_values[a] = 0
        for i in eqn_values.keys():
            if i in discons:
                eqn_values[i] = '*'
            else:
                eqn_values[i] = eqn.subs(x, i)
    else:
        for i in range(-3, 4):
            eqn_values[i] = eqn.subs(x, i)
    
    return eqn_values


def maths_operations(eqn):
    x = Symbol('x', real=True)
    eqn = eval(eqn)
    eqn_discons = singularities(eqn, x)
    eqn_values = table_builder(eqn_discons, eqn, x)

    der = diff(eqn, x)
    der_discons = singularities(der, x)
    der_values = table_builder(der_discons, der, x)

    double_der = diff(eqn, x, x)
    double_der_discons = singularities(double_der, x)
    double_der_values = table_builder(double_der_discons, double_der, x)
    #for index, value in enumerate(y_values):
    #    y_values[index] = '%g'%(value) # remove trailing zeroes
    return eqn, eqn_values, der, der_values, double_der, double_der_values

async def asymptote_calculator(eqn):
    x = Symbol('x', real=True)
    h_asymptotes = {}

    pos_inf_h = limit(eqn, x, oo)
    if eqn.subs(x, 100000) > pos_inf_h:
        pos_inf_h_str = f'{pos_inf_h} from the +ve'
    else:
        pos_inf_h_str = f'{pos_inf_h} from the -ve'
    neg_inf_h = limit(eqn, x, -oo)
    if eqn.subs(x, -100000) > neg_inf_h:
        neg_inf_h_str = f'{neg_inf_h} from the +ve'
    else:
        neg_inf_h_str = f'{neg_inf_h} from the -ve'
    h_asymptotes['oo'] = [pos_inf_h, pos_inf_h_str]
    h_asymptotes['-oo'] = [neg_inf_h, neg_inf_h_str]



    n, d = fraction(simplify(eqn))
    denom_roots = solve(d)
    async def v_solver(eqn, x, denom_roots):
        v_asymptotes = {}
        if denom_roots:
            for root in denom_roots:
                v_asymptotes[root] = {}
                v_asymptotes[root]['+'] = limit(eqn, x, root)
                v_asymptotes[root]['-'] = limit(eqn, x, root, dir='-')
        return v_asymptotes

    if denom_roots:
        try:
            v_asymptotes = await asyncio.wait_for(v_solver(eqn, x, denom_roots), timeout=30)
        except:
            v_asymptotes = 'It took too long to calculate the vertical asymptotes give me a simpler equation smh'
        else:
            asymptotes = {}
            asymptotes['h'] = h_asymptotes
            asymptotes['v'] = v_asymptotes
    else:
        asymptotes = {}
        asymptotes['h'] = h_asymptotes
        asymptotes['v'] = 'That equation has no vertical asymptotes'

    return asymptotes


async def graph_creator():
    eqn_str = input('What would you like to graph? Make sure to use proper brackets, "^" is "to the power of", and use "*" with all instances of multiplication (e.g. 2*x, not 2x) ')

    maths_eqn = eqn_formatter(eqn_str, maths=True)


    eqn, eqn_values, der, der_values, double_der, double_der_values = maths_operations(maths_eqn)

    desmos_eqn = eqn_formatter(eqn_str, desmos=True)
    desmos_der = eqn_formatter(str(der), desmos=True)
    desmos_double_der = eqn_formatter(str(double_der), desmos=True)

    eqn_asymptotes = await asymptote_calculator(eqn)
    der_asymptotes = await asymptote_calculator(der)
    double_der_asymptotes = await asymptote_calculator(double_der)


    desmos_html_creator(desmos_eqn, eqn_str, eqn_values, desmos_der, der_values, desmos_double_der, double_der_values, eqn_asymptotes, der_asymptotes, double_der_asymptotes)

asyncio.run(graph_creator())