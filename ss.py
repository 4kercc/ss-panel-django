#! /usr/bin/env python3

import os, socket, random, json, configparser


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(BASE_DIR)

    config = configparser.ConfigParser()
    config.sections()
    config.read(os.path.join(BASE_DIR, 'config.ini'))

    server_ip = config['server']['ip']
    timeout = int(config['server']['timeout'])
    method = config['server']['method']
    name = config['server']['name']

    manager_ip = config['manager']['ip']
    manager_port = int(config['manager']['port'])


class SS:
    c = Config()
    socket_server = (c.manager_ip, c.manager_port) # address of Shadowsocks manager
    bufsize = 1024 * 8


    def send(self, op):
        cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli.connect(self.socket_server)

        print('SS CMD: %s' % op)

        cli.send(op.encode())
        msg = cli.recv(self.bufsize).decode() # 收到的数据应当是 ASCII 编码.
        print('SS RST: %s' % msg)

        cli.close()

        return msg


    def ping(self, src=False):
        msg = self.send('ping') # You'll receive 'pong'
        j = msg.split()[1] # JSON

        if src: # 返回原始 JSON
            return j
        else:
            return json.loads(j)


    def open_port(self, server_port, password):
        r = False
        cmd = 'add: {"server_port": %s, "password": "%s"}' % (server_port, password)
        msg = self.send(cmd)

        if msg == 'ok':
            r = True
        print('open_port %s: %s' % (server_port, r))
        return r


    def close_port(self, server_port):
        r = False
        cmd = 'remove: {"server_port": %s}' % server_port
        msg = self.send(cmd)

        if msg == 'ok':
            r = True
        print('close_port %s: %s' % (server_port, r))
        return r


    def reopen_port(self, server_port, password):
        r = False
        r = self.close_port(server_port)
        r = self.open_port(server_port, password)

        print('reopen_port %s: %s' % (server_port, r))
        return r


# 直接运行显示当前服务器流量
if __name__ == '__main__':
    c = Config()
    print(c.server_ip, c.timeout, c.method, c.manager_ip, c.manager_port)
    s = SS()
    print(s.socket_server)
    print(s.ping())
