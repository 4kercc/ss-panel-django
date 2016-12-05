from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def index(request):
    c = {
        'title': '首页',
    }
    return render_to_response(request, 'panel/index.html', c)


@require_safe
def status(request):
    c = {
        'title': '资金状态',
    }
    return render_to_response(request, 'panel/index.html', c)
