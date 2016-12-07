#! /usr/bin/env python3

import os, socket, random


socket_server = '/var/run/shadowsocks-manager.sock' # address of Shadowsocks manager
bufsize = 1024 * 8


def send(op):
    socket_client = '/tmp/ss-client.sock.' + str(random.randrange(100000000)) # address of the client

    if os.path.isfile(socket_client):
        os.unlink(socket_client)

    cli = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    cli.bind(socket_client)
    cli.connect(socket_server)

    cli.send(op.encode())
    msg = cli.recv(bufsize).decode() # 收到的数据应当是 ASCII 编码.

    cli.close()
    os.unlink(socket_client)

    return msg


def ping():
    msg = send(b'ping') # You'll receive 'pong'
    return msg.split()[1] # JSON


def add(server_port, password):
    r = False
    cmd = 'add: {"server_port": %s, "password": "%s"}' % (server_port, password)
    msg = send(cmd)

    if msg == 'ok':
        r = True

    return r


def remove(server_port):
    r = False
    cmd = 'remove: {"server_port": %s"}' % server_port
    msg = send(cmd)

    if msg == 'ok':
        r = True

    return r


# 直接运行显示当前服务器流量
if __name__ == '__main__':
    print(ping())
