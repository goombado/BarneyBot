from __future__ import absolute_import
import sympy
import collections
from contextlib import contextmanager
import stepprinter
from stepprinter import functionnames, Rule, replace_u_var
from datetime import datetime
from pprint import pprint

from sympy.integrals.manualintegrate import (
    manualintegrate, _manualintegrate, integral_steps, evaluates,
    ConstantRule, ConstantTimesRule, PowerRule, AddRule, URule,
    PartsRule, CyclicPartsRule, TrigRule, ExpRule, ArctanRule,
    AlternativeRule, DontKnowRule, RewriteRule, ReciprocalRule
)

# Need this to break loops
# TODO: add manualintegrate flag to integrate
_evaluating = None
@evaluates(DontKnowRule)
def eval_dontknow(context, symbol):
    global _evaluating
    if _evaluating == context:
        return None
    _evaluating = context
    result = sympy.integrate(context, symbol)
    _evaluating = None
    return result


def contains_dont_know(rule):
    if isinstance(rule, DontKnowRule):
        return True
    else:
        for val in rule._asdict().values():
            if isinstance(val, tuple):
                if contains_dont_know(val):
                    return True
            elif isinstance(val, list):
                if any(contains_dont_know(i) for i in val):
                    return True
    return False

def filter_unknown_alternatives(rule):
    if isinstance(rule, AlternativeRule):
        alternatives = list([r for r in rule.alternatives if not contains_dont_know(r)])
        if not alternatives:
            alternatives = rule.alternatives
        return AlternativeRule(alternatives, rule.context, rule.symbol)
    return rule

class IntegralPrinter(object):
    def __init__(self, rule):
        self.rule = rule
        self.print_rule(rule)
        self.u_name = 'u'
        self.u = self.du = None

    def print_rule(self, rule):
        if isinstance(rule, ConstantRule):
            self.print_Constant(rule)
        elif isinstance(rule, ConstantTimesRule):
            self.print_ConstantTimes(rule)
        elif isinstance(rule, PowerRule):
            self.print_Power(rule)
        elif isinstance(rule, AddRule):
            self.print_Add(rule)
        elif isinstance(rule, URule):
            self.print_U(rule)
        elif isinstance(rule, PartsRule):
            self.print_Parts(rule)
        elif isinstance(rule, CyclicPartsRule):
            self.print_CyclicParts(rule)
        elif isinstance(rule, TrigRule):
            self.print_Trig(rule)
        elif isinstance(rule, ExpRule):
            self.print_Exp(rule)
        elif isinstance(rule, ArctanRule):
            self.print_Arctan(rule)
        elif isinstance(rule, AlternativeRule):
            self.print_Alternative(rule)
        elif isinstance(rule, DontKnowRule):
            self.print_DontKnow(rule)
        elif isinstance(rule, RewriteRule):
            self.print_Rewrite(rule)
        elif isinstance(rule, ReciprocalRule):
            self.print_Reciprocal(rule)
        else:
            self.append(repr(rule))

    def print_Constant(self, rule):
        with self.new_item():
            self.append("The integral of a constant is the constant "
                        "times the variable of integration:\\\\\n")
            self.append("${}$\\\\\\\\\n".format(
                self.format_math_display(
                    sympy.Eq(sympy.Integral(rule.constant, rule.symbol),
                           _manualintegrate(rule))))
            )

    def print_ConstantTimes(self, rule):
        with self.new_item():
            self.append("The integral of a constant times a function "
                        "is the constant times the integral of the function:\\\\\n")
            self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                sympy.Eq(
                    sympy.Integral(rule.context, rule.symbol),
                    rule.constant * sympy.Integral(rule.other, rule.symbol))))
            )
            with self.new_level():
                self.print_rule(rule.substep)
            self.append("So, the result is: ${}$\\\\\\\\\n".format(
                self.format_math(_manualintegrate(rule))))

    def print_Power(self, rule):
        with self.new_item():
            self.append("The integral of ${}$ is ${}$ when ${}$:\\\\\\\\\n".format(
                self.format_math(rule.symbol ** sympy.Symbol('n')),
                self.format_math((rule.symbol ** (1 + sympy.Symbol('n'))) /
                                 (1 + sympy.Symbol('n'))),
                self.format_math(sympy.Ne(sympy.Symbol('n'), -1)),
            ))
            self.append("${}$\\\\\\\\\n".format(
                self.format_math_display(
                    sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                           _manualintegrate(rule))))
            )
    def print_Add(self, rule):
        with self.new_item():
            self.append("Integrate term-by-term:\\\\\n")
            for substep in rule.substeps:
                with self.new_level():
                    self.print_rule(substep)
            self.append("The result is: ${}$\\\\\\\\\n".format(
                self.format_math(_manualintegrate(rule))))

    def print_U(self, rule):
        with self.new_item(), self.new_u_vars() as (u, du):
            # commutative always puts the symbol at the end when printed
            dx = sympy.Symbol('d' + rule.symbol.name, commutative=0)
            self.append("Let ${}$.\\\\\\\\\n".format(
                self.format_math(sympy.Eq(u, rule.u_func))))
            self.append("Then let ${}$ and substitute ${}$:\\\\\\\\\n".format(
                self.format_math(sympy.Eq(du, rule.u_func.diff(rule.symbol) * dx)),
                self.format_math(rule.constant * du)
            ))

            integrand = rule.constant * rule.substep.context.subs(rule.u_var, u)
            self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                sympy.Integral(integrand, u)))
            )

            with self.new_level():
                self.print_rule(replace_u_var(rule.substep, rule.symbol.name, u))

            self.append("Now substitute ${}$ back in:\\\\\\\\\n".format(
                self.format_math(u)))

            self.append("${}$\\\\\\\\\n".format(self.format_math_display(_manualintegrate(rule))))

    def print_Parts(self, rule):
        with self.new_item():
            self.append("Use integration by parts:\\\\\n")

            u, v, du, dv = [sympy.Function(f)(rule.symbol) for f in 'u v du dv'.split()]
            self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                r"""\int \operatorname{u} \operatorname{dv}
                = \operatorname{u}\operatorname{v} -
                \int \operatorname{v} \operatorname{du}"""
            )))

            self.append("Let ${}$ and let ${}$.\\\\\\\\\n".format(
                self.format_math(sympy.Eq(u, rule.u)),
                self.format_math(sympy.Eq(dv, rule.dv))
            ))
            self.append("Then ${}$.\\\\\\\\\n".format(
                self.format_math(sympy.Eq(du, rule.u.diff(rule.symbol)))
            ))

            self.append("To find ${}$:\\\\\\\\\n".format(self.format_math(v)))

            with self.new_level():
                self.print_rule(rule.v_step)

            self.append("Now evaluate the sub-integral.\\\\\n")
            self.print_rule(rule.second_step)

    def print_CyclicParts(self, rule):
        with self.new_item():
            self.append("Use integration by parts, noting that the integrand"
                        " eventually repeats itself.\\\\\n")

            u, v, du, dv = [sympy.Function(f)(rule.symbol) for f in 'u v du dv'.split()]
            current_integrand = rule.context
            total_result = sympy.S.Zero
            with self.new_level():

                sign = 1
                for rl in rule.parts_rules:
                    with self.new_item():
                        self.append("For the integrand ${}$:\\\\\\\\\n".format(self.format_math(current_integrand)))
                        self.append("Let ${}$ and let ${}$.\\\\\\\\\n".format(
                            self.format_math(sympy.Eq(u, rl.u)),
                            self.format_math(sympy.Eq(dv, rl.dv))
                        ))

                        v_f, du_f = _manualintegrate(rl.v_step), rl.u.diff(rule.symbol)

                        total_result += sign * rl.u * v_f
                        current_integrand = v_f * du_f

                        self.append("Then ${}$.\\\\\\\\\n".format(
                            self.format_math(
                                sympy.Eq(
                                    sympy.Integral(rule.context, rule.symbol),
                                    total_result - sign * sympy.Integral(current_integrand, rule.symbol)))
                        ))
                        sign *= -1
                with self.new_item():
                    self.append("Notice that the integrand has repeated itself, so "
                                "move it to one side:\\\\\n")
                    self.append("${}$\\\\\\\\\n".format(
                        self.format_math_display(sympy.Eq(
                            (1 - rule.coefficient) * sympy.Integral(rule.context, rule.symbol),
                            total_result
                        ))
                    ))
                    self.append("Therefore,\\\\\\\\\n")
                    self.append("${}$\\\\\\\\\n".format(
                        self.format_math_display(sympy.Eq(
                            sympy.Integral(rule.context, rule.symbol),
                            _manualintegrate(rule)
                        ))
                    ))


    def print_Trig(self, rule):
        with self.new_item():
            text = {
                'sin': "The integral of sine is negative cosine:\\\\\n",
                'cos': "The integral of cosine is sine:\\\\\n",
                'sec*tan': "The integral of secant times tangent is secant:\\\\\n",
                'csc*cot': "The integral of cosecant times cotangent is cosecant:\\\\\n",
            }.get(rule.func)

            if text:
                self.append(text)

            self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                       _manualintegrate(rule))))
            )

    def print_Exp(self, rule):
        with self.new_item():
            if rule.base == sympy.E:
                self.append("The integral of the exponential function is itself.\\\\\n")
            else:
                self.append("The integral of an exponential function is itself"
                            " divided by the natural logarithm of the base.\\\\\n")
            self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                       _manualintegrate(rule))))
            )

    def print_Reciprocal(self, rule):
        with self.new_item():
            self.append("The integral of ${}$ is ${}$.\\\\\\\\\n".format(
                self.format_math(1 / rule.func),
                self.format_math(_manualintegrate(rule))
            ))

    def print_Arctan(self, rule):
        with self.new_item():
            self.append("The integral of ${}$ is ${}$.\\\\\\\\\n".format(
                self.format_math(1 / (1 + rule.symbol ** 2)),
                self.format_math(_manualintegrate(rule))
            ))

    def print_Rewrite(self, rule):
        with self.new_level():
            with self.new_item():
                self.append("Rewrite the integrand:\\\\\n")
                self.append("${}$\\\\\\\\\n".format(self.format_math_display(
                    sympy.Eq(rule.context, rule.rewritten))))
                self.print_rule(rule.substep)

    def print_DontKnow(self, rule):
        with self.new_item():
            self.append("Don't know the steps in finding this integral.\\\\\n")
            self.append("But the integral is\\\\")
            self.append("${}$".format(self.format_math_display(sympy.integrate(rule.context, rule.symbol))))


class HTMLPrinter(IntegralPrinter, stepprinter.LaTeXPrinter):
    def __init__(self, rule):
        self.alternative_functions_printed = set()
        stepprinter.LaTeXPrinter.__init__(self)
        IntegralPrinter.__init__(self, rule)

    def print_Alternative(self, rule):
        # TODO: make more robust
        rule = filter_unknown_alternatives(rule)

        if len(rule.alternatives) == 1:
            self.print_rule(rule.alternatives[0])
            return

        if rule.context.func in self.alternative_functions_printed:
            self.print_rule(rule.alternatives[0])
        else:
            self.alternative_functions_printed.add(rule.context.func)
            with self.new_item():
                self.append("There are multiple ways to do this integral.\\\\\n")
                for index, r in enumerate(rule.alternatives):
                    self.append("\\subsection{" + "Method #{}".format(index + 1) + "}\\\\\n")
                    with self.new_level():
                        self.print_rule(r)

    def format_math_constant(self, math):
        return '${}$\\\\\\\\\n'.format(
            sympy.latex(math) + r'+ \mathrm{constant}')

    def finalize(self):
        rule = filter_unknown_alternatives(self.rule)
        answer = _manualintegrate(rule)
        latex_formatted = False
        if answer:
            simp = sympy.simplify(sympy.trigsimp(answer))
            if simp != answer:
                answer = simp
                with self.new_step():
                    self.append("Now simplify:\\\\\n")
                    self.append("${}$\\\\\\\\\n".format(self.format_math_display(simp)))
            with self.new_step():
                self.append("Add the constant of integration:\\\\\n")
                self.append("{}".format(self.format_math_constant(answer)))
        # self.lines.append('</ol>')
        # self.lines.append('<hr/>')
        self.level = 0
        self.append('The answer is:\\\\\n')
        self.append("{}".format(self.format_math_constant(answer)))
        return ' '.join(self.lines)

def print_html_steps(function, symbol):
    rule = integral_steps(function, symbol)
    pprint(rule)
    if isinstance(rule, DontKnowRule):
        raise ValueError("Cannot evaluate integral\\\\")
    a = HTMLPrinter(rule)
    return a.finalize()

if __name__ == '__main__':
    x = sympy.Symbol('x')
    y = ((x**2+4*x-7)/sympy.sqrt((4-x**2)))
    text = print_html_steps(y, x)
    y_latex = f"${sympy.latex(sympy.Integral(y), inv_trig_style='power', ln_notation=True)}$\\\\\\\\\\\\\\\\\n"
    preamble = "\\documentclass[11pt,a4paper]{article}\n\\usepackage{amsmath,amsfonts}\n\n" \
        "\\title{Random Integrals}\n\\author{Created by Barney}\n \\date{"+ f"{datetime.now().strftime('%d/%m/%Y')}" + "}\n\n\\begin{document}\n\n" \
        "\\begin{titlepage}\n\\maketitle\n\\end{titlepage}\nQuestion 1:\\\\\\\\"
    full_text = preamble + y_latex + text + "\n\\end{document}"
    outFile = open('test_file.tex', 'w')
    outFile.write(full_text)
    outFile.close()
