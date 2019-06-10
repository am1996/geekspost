from django import template
register = template.Library()

@register.filter(name='index')
def index(l,t):
	num = list(l).index(t) % 2
	return num