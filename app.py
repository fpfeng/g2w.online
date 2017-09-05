import subprocess
import shlex
import re
import os
from IPy import IP
from flask import Flask, make_response, abort, current_app, render_template
from utils import ListConverter
from config import configs


app = Flask(__name__)
app.config.from_object(configs[os.environ.get('g2wconf', 'dev')])
app.url_map.converters['list'] = ListConverter


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ipset/<path:args>')
def ipset(args):
    try:
        name_addr = args.split(',')
        name, addr = name_addr
        if name and addr and check_valid_ipset(name, addr):
            ip, port = addr.split(':')
            command = create_cmd_str(ip, port, name)
            return maek_resp_from_stdout(command, name + '_ipset.conf')
        abort(404)
    except:
        abort(404)


@app.route('/dnsq/<path:args>')
def dnsq(args):
    try:
        ip, port = args.split(':')
        if check_addr(ip, port):
            command = create_cmd_str(ip, port)
            return maek_resp_from_stdout(command, 'gfwlist_dnsmasq.conf')
        abort(404)
    except:
        abort(404)


def maek_resp_from_stdout(cmd, filename):
    stdout = subprocess.check_output(cmd)
    resp = make_response(stdout)
    resp.headers["Content-Disposition"] = \
        'attachment; filename=' + filename
    return resp


def create_cmd_str(ip, port, name=None):
    command = shlex.split(
              current_app.config['G2D_PTAH'] +
              ' -l ' +
              current_app.config['TXTLIST_PTAH'] +
              ' -d ' +
              ip +
              ' -p ' +
              port +
              ' -o -')
    if not name:  # without ipset
        command += ['-i', '-']
    else:  # with ipset
        command += ['-i', name]
    return command


def check_valid_ipset(name, addr):
    pass_check = False
    if len(name) <= 20 and re.match("^[a-zA-Z0-9_]*$", name)\
            and check_addr(*addr.split(':')):
            pass_check = True
    return pass_check


@app.route('/pac/<list:proxies>')
def pac(proxies):
    try:
        if len(proxies) <= 10:
            all_args = []
            for p in proxies:
                pass_check, arg = check_vaild_pac(p.split(','))
                if pass_check:
                    all_args.append(arg)
            to_str = '"' + '; '.join(all_args) + '"'
            command = shlex.split(
                            'genpac --gfwlist-url="-" ' +
                            '--gfwlist-local=' +
                            current_app.config['TXTLIST_PTAH'] +
                            ' -p ' +
                            to_str +
                            ' --user-rule="||naver.jp"')

            return maek_resp_from_stdout(command, 'gfwlist.pac')
        abort(404)
    except:
        abort(404)


def check_vaild_pac(type_addr):
    pass_check, arg = False, None
    if len(type_addr) == 2:
        p_type = type_addr[0]
        addr = type_addr[1]
        if p_type in ['h', 's'] and check_addr(*addr.split(':')):
            pass_check = True
            arg = create_proxy_arg(p_type, addr)
    return pass_check, arg


def check_addr(ip, port):
    pass_check = True
    if ip and port and 0 < int(port) < 65536:
        try:
            _ = IP(ip)
        except ValueError:
            pass_check = False
    else:
        pass_check = False
    return pass_check


def create_proxy_arg(p_type, addr):
    arg = ''
    if p_type == 's':
        arg = 'SOCKS5 ' + addr + '; ' + 'SOCKS ' + addr
    else:
        arg = 'PROXY ' + addr
    return arg


if __name__ == '__main__':
    app.run()
