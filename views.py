from collections import OrderedDict

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.views import logout, password_change
from django.contrib.auth.models import User as UserAuth

from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.decorators import login_required

from .ss import SS
from .models import User, Flow, In, Out
from .decorators import superuser_required


s = SS()


def port_test(port):
    """端口打开测试"""
    flow = s.ping()
    return str(port) in flow.keys()


def port_op(panel, op):
    """端口操作"""
    port = panel.port
    password = panel.password

    port_is_open = port_test(port)

    r = False

    if op == 'open_port':
        op_str = '打开端口'
        if port_is_open:
            r = True
        else:
            r = s.open_port(port, password)
    elif op == 'reopen_port':
        op_str = '重启端口'
        if port_is_open:
            r = s.reopen_port(port, password)
        else:
            r = s.open_port(port, password)
    elif op == 'close_port':
        op_str = '关闭端口'
        if port_is_open:
            r = s.close_port(port)
        else:
            r = True
    else:
        op_str = '未知的(%s)' % op

    if r:
        r_str = '成功'
    else:
        r_str = '失败'

    op_dict = {
        'op_str': op_str,
        'r_str': r_str,
    }

    return op_dict


@require_safe
def index_main(request):
    """可以将此页加为主站点的首页.

    可以将以下语句加入工程的 urls.py:

    import panel.views

    urlpatterns 内添加:

    url(r'^$', panel.views.index_main),
    """
    return redirect('panel:index')


@require_safe
def quit(request):
    """logout"""
    logout(request)
    c = {
        'title': '退出成功',
        'info': '感谢您的使用, 再见.',
        'link_url': 'panel:index',
        'link_text': '重新登录',
    }
    return render(request, 'panel/info.html', c)


def password_change_panel(request):
    return password_change(request,
        template_name='panel/password_change_form.html',
        post_change_redirect='panel:password_change_done'
    )


def password_change_done(request):
    c = {
        'title': '修改密码',
        'info': '您的密码已修改成功.',
        'link_url': 'panel:index',
        'link_text': '返回首页',
    }
    return render(request, 'panel/info.html', c)


@require_safe
@login_required
def index(request):
    panel = request.user.user # panel.models.User
    c = {
        'title': '首页',
        'panel': panel,
        's': s,
        'online': port_test(panel.port),
    }
    return render(request, 'panel/index.html', c)


@require_safe
@login_required
@superuser_required
def status(request):
    """统计服务器当前各端口流量."""
    flow = s.ping()
    flows_srt = {}

    for k, v in flow.items():
        flow_readable = v / 1024 / 1024
        if flow_readable > 1024:
            flow_srt = '%.3f GB' % (flow_readable / 1024)
        else:
            flow_srt = '%.3f MB' % flow_readable
        flows_srt[k] = flow_srt

    c = {
        'title': '服务器状态',
        'panel_title': '当前流量',
        'flow': OrderedDict(sorted(flows_srt.items())),
    }
    return render(request, 'panel/status.html', c)


@require_safe
@login_required
@superuser_required
def users(request):
    """User list."""
    users = User.objects.all().values()

    # 向 User 列表中增加端口实时状态和当前流量.
    flow = s.ping()
    user_status = []
    user_list = [item for item in users]
    for u in user_list:
        # user is fk, lost in dict.
        u['user'] = UserAuth.objects.get(id=u['user_id'])

        if str(u['port']) in flow.keys():
            u['online'] = True
            # 转换为 MB 和 GB
            flow_readable = flow[str(u['port'])] / 1024 / 1024
            if flow_readable > 1024:
                flow_srt = '%.3f GB' % (flow_readable / 1024)
            else:
                flow_srt = '%.3f MB' % flow_readable
            u['flow'] = flow_srt
        else:
            u['online'] = False
            u['flow'] = '0.000 MB'

        user_status.append(u)

    c = {
        'title': '用户列表',
        'users': user_status,
    }
    return render(request, 'panel/users.html', c)


@require_safe
@login_required
@superuser_required
def gold(request):
    """统计资金收支状态."""
    gold_in = In.objects.all().aggregate(Sum('num'))['num__sum']
    gold_out = Out.objects.all().aggregate(Sum('num'))['num__sum']
    gold_sum = gold_in + gold_out

    c = {
        'title': '资金状态',
        'gold_sum': gold_sum,
        'gold_in': gold_in,
        'gold_out': gold_out,
    }
    return render(request, 'panel/gold.html', c)


@require_safe
@login_required
@superuser_required
def gold_method(request, method):
    """统计资金收支明细."""
    title = ''
    gold_sum = 0.0
    gold_list = []

    if method == 'in':
        title = '收入明细'
        gold_sum = In.objects.all().aggregate(Sum('num'))['num__sum']
        gold_list = In.objects.all().order_by('-date')
    elif method == 'out':
        title = '支出明细'
        gold_sum = Out.objects.all().aggregate(Sum('num'))['num__sum']
        gold_list = Out.objects.all().order_by('-date')

    c = {
        'title': title,
        'gold_sum': gold_sum,
        'gold_list': gold_list,
        'method': method,
    }
    return render(request, 'panel/gold_method.html', c)


@require_POST
@login_required
@superuser_required
def ss_op_admin(request):
    """管理员操作用户的 Shadowsocks 端口."""
    username = request.POST['username']
    panel = UserAuth.objects.get(username=username).user
    op = request.POST['op']

    r = port_op(panel, op)

    c = {
        'title': '操作结果',
        'info': '对 %s 的 %s 操作, 执行结果: %s.' % (username, r['op_str'], r['r_str']),
        'link_url': 'panel:users',
        'link_text': '返回用户列表',
    }
    return render(request, 'panel/info.html', c)


@require_POST
@login_required
def ss_op(request):
    """用户操作自己的 Shadowsocks 端口."""
    panel = request.user.user # panel.models.User
    op = request.POST['op']

    r = port_op(panel, op)

    c = {
        'title': '操作结果',
        'info': '%s 操作, 执行结果: %s.' % (r['op_str'], r['r_str']),
        'link_url': 'panel:index',
        'link_text': '返回首页',
    }
    return render(request, 'panel/info.html', c)
