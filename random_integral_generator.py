from sympy import *
from sympy.integrals.manualintegrate import manualintegrate, integral_steps
import random
from io import BytesIO
from datetime import datetime
import os
import pdflatex

def random_integral_generator(amount, unit):
    integral_types = ['normal', 'log', 'trig', 'inverse trig']
    if unit == 4:
        integral_types.extend(['by parts', 'partial fracs', ''])

x = Symbol('x')
init_printing()
y = (x**2 + 6*x + 9)/(x**3)
print(integral_steps(y, x))
y_int_str = Integral(y)
y_int = manualintegrate(y, x)
obj = BytesIO()
preamble = "\\documentclass[11pt,a4paper]{article}\n\\usepackage{amsmath,amsfonts}\n\n" \
    "\\title{Random Integrals}\n\\author{Created by Barney}\n \\date{"+ f"{datetime.now().strftime('%d/%m/%Y')}" + "}\n\n\\begin{document}\n\n" \
        "\\begin{titlepage}\n\\maketitle\n\\end{titlepage}\nQuestion 1:\\\\\\\\"

#preview(y_int, output='png', viewer='file', filename='test_latex.png', euler=False, preamble=preamble)
text = f'{preamble}\n${latex(y_int_str, inv_trig_style="power", ln_notation=True)}$\\\\\\\\${latex(y_int, inv_trig_style="power", ln_notation=True)}$\n\n\\end{{document}}'



outFile = open('test_latex_2.tex', 'w')
outFile.write(text)
outFile.close()

os.system('pdflatex test_latex_2.tex')

#outFile = open('test_latex.pdf', 'w')
#outFile.write(pdf)
#outFile.close()