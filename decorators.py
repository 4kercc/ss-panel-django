from django.shortcuts import render


def not_superuser(request):
    """logout"""
    c = {
        'title': '没有使用权',
        'info': '您没有使用此功能的权利, 请返回主页.',
        'link_url': 'panel:index',
        'link_text': '返回主页',
    }
    return render(request, 'panel/info.html', c)


def superuser_required(function):
    """确认是否为"超级用户", 非超级用户返回一个错误页面(not_superuser)."""
    def wrapper(request, *args, **kwargs): # views 函数构造
        if request.user.is_superuser:
            return(function(request, *args, **kwargs))
        else:
            return(not_superuser(request))
    return wrapper
