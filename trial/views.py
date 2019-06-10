from django.shortcuts import render,redirect
from django.views.generic import TemplateView

def index(request):
	return redirect("/posts/")