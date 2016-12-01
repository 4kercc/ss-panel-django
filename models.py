from django.db import models
from django.conf import settings


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户')
    status = models.BooleanField(default=False, verbose_name='状态')
    port = models.IntegerField(unique=True, verbose_name='端口')
    password = models.CharField(max_length=32, verbose_name='密码')
    setup_date = models.DateField(verbose_name='建立日期')
    end_date = models.DateField(verbose_name='结束日期')
    memo = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['setup_date',]


class Flow(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    bandwidth = models.BigIntegerField(verbose_name='带宽')

    def __str__(self):
        return '%s: %s: %s MB' % (self.user, self.date, self.bandwidth / 1024 / 1024)

    class Meta:
        verbose_name = '流量'
        verbose_name_plural = verbose_name
        ordering = ['date', 'user']


class In(models.Model):
    date = models.DateField(verbose_name='日期')
    user = models.ForeignKey(User, verbose_name='用户')
    num = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    memo = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '%s: %s: %s 元' % (self.date, self.user, self.num)

    class Meta:
        verbose_name = '收入'
        verbose_name_plural = verbose_name
        ordering = ['date',]


class Out(models.Model):
    date = models.DateField(verbose_name='日期')
    log = models.CharField(max_length=256, verbose_name='记录')
    num = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    memo = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '%s: %s: %s 元' % (self.date, self.log, self.num)

    class Meta:
        verbose_name = '支出'
        verbose_name_plural = verbose_name
        ordering = ['date',]
