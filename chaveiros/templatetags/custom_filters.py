# yourapp/templatetags/custom_filters.py
from django import template
from datetime import date

register = template.Library()

@register.filter
def idade(data_nascimento):
    if not data_nascimento:
        return ""
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade
