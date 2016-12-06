from .views import not_superuser

def superuser_required(function):
    """确认是否为"超级用户", 非超级用户返回一个错误页面(not_superuser)."""
    def wrapper(request, *args, **kwargs): # views 函数构造
        if request.user.is_superuser:
            return(function(request, *args, **kwargs))
        else:
            return(not_superuser(request))
    return wrapper
