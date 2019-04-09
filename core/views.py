from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404

from core.forms import
from datetime import date

# Create your views here.
def index(request):
