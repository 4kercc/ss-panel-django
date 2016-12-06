from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.db.models import Sum

from .models import In, Out


@require_safe
def index(request):
    c = {
        'title': '首页',
    }
    return render(request, 'panel/index.html', c)


@require_safe
def status(request):
    """统计服务器状态, 属于管理页面."""
    c = {
        'title': '服务器状态',
    }
    return render(request, 'panel/status.html', c)


@require_safe
def gold(request):
    """统计资金收支状态, 属于管理页面."""
    gold_in = In.objects.all().aggregate(Sum('num')).num__sum
    gold_out = Out.objects.all().aggregate(Sum('num')).num__sum
    gold_sum = gold_in + gold_out
    c = {
        'title': '资金状态',
        'gold_sum': gold_sum,
        'gold_in': gold_in,
        'gold_out': gold_out,
    }
    return render(request, 'panel/gold.html', c)
