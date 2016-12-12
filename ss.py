#! /usr/bin/env python3

import os, socket, random, json


socket_server = ('127.0.0.1', 50001) # address of Shadowsocks manager
bufsize = 1024 * 8


def send(op):
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.connect(socket_server)

    print('SS 操作命令: %s' % op)

    cli.send(op.encode())
    msg = cli.recv(bufsize).decode() # 收到的数据应当是 ASCII 编码.
    print('SS: 操作结果: %s' % msg)

    cli.close()

    return msg


def ping(src=False):
    msg = send('ping') # You'll receive 'pong'
    j = msg.split()[1] # JSON

    if src: # 返回原始 JSON
        return j
    else:
        return json.loads(j)


def open_port(server_port, password):
    r = False
    cmd = 'add: {"server_port": %s, "password": "%s"}' % (server_port, password)
    msg = send(cmd)

    if msg == 'ok':
        r = True

    return r


def close_port(server_port):
    r = False
    cmd = 'remove: {"server_port": %s"}' % server_port
    msg = send(cmd)

    if msg == 'ok':
        r = True

    return r


def reopen_port(server_port, password):
    r = False
    msg = close_port(server_port)
    msg = open_port(server_port, password)

    if msg == 'ok':
        r = True

    return r


# 直接运行显示当前服务器流量
if __name__ == '__main__':
    print(ping())
