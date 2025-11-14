from django.shortcuts  import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from config.globals import BaseContextView, data, navbar
from django.views.generic import TemplateView, CreateView, UpdateView,ListView, DetailView, DeleteView, FormView
from ..models import *
from ..forms import *
