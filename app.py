import subprocess
import shlex
import re
import os
from IPy import IP
from flask import Flask, make_response, abort, current_app, render_template
from utils import ListConverter, abort_when_error
from config import configs


IPSET_NAME_MAX = 20
PAC_MAX_CHAIN_PROXIES = 20


app = Flask(__name__)
app.config.from_object(configs[os.environ.get('g2wconf', 'dev')])
app.url_map.converters['list'] = ListConverter


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ipset/<path:args>')
@abort_when_error
def ipset(args):
    name, addr = args.split(',')
    if name and addr and check_valid_ipset(name, addr):
        return make_resp_with_cmd_stdout(
                    create_cmd(*addr.split(':'), name=name), name + '_ipset.conf')
    abort(404)


def check_valid_ipset(name, addr):
    return len(name) <= IPSET_NAME_MAX and re.match("^[a-zA-Z0-9_]*$", name)\
            and check_addr(*addr.split(':'))


@app.route('/dnsq/<path:args>')
@abort_when_error
def dnsq(args):
    ip, port = args.split(':')
    if check_addr(ip, port):
        return make_resp_with_cmd_stdout(create_cmd(ip, port), 'gfwlist_dnsmasq.conf')
    abort(404)


def make_resp_with_cmd_stdout(cmd, filename):
    resp = make_response(subprocess.check_output(cmd))
    resp.headers["Content-Disposition"] = \
        'attachment; filename=' + filename
    return resp


def create_cmd(ip, port, name=None):
    command = shlex.split(' '.join([
                            current_app.config['G2D_PTAH'],
                            '-l',
                            current_app.config['TXTLIST_PTAH'],
                            '-d',
                            ip,
                            '-p',
                            port,
                            '-o -',
            ]))
    if not name:  # without ipset name
        command.extend(['-i', '-'])
    else:
        command.extend(['-i', name])
    return command


@app.route('/pac/<list:proxies>')
@abort_when_error
def pac(proxies):
    if len(proxies) <= PAC_MAX_CHAIN_PROXIES: # allow max 10 chain proxies
        all_args = []
        for p in proxies:
            pass_check, arg = check_and_parse_pac_args(p.split(','))
            if pass_check:
                all_args.append(arg)
            else:
                abort(404)

        if all_args:
            command = shlex.split(' '.join([
                                'genpac --gfwlist-url="-"',
                                '--gfwlist-local=' + current_app.config['TXTLIST_PTAH'],
                                '-p',
                                ''.join(['"', '; '.join(all_args), '"']),
                                '--user-rule="||naver.jp"',
                    ]))
            return make_resp_with_cmd_stdout(command, 'gfwlist.pac')
    abort(404)


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


def check_and_parse_pac_args(type_addr):
    pass_check, arg = False, None
    if len(type_addr) == 2:
        proxy_type, addr = type_addr
        if proxy_type in ['h', 's'] and check_addr(*addr.split(':')):
            pass_check = True
            arg = create_proxy_arg(proxy_type, addr)
    return pass_check, arg


def create_proxy_arg(proxy_type, addr):
    args = {
        's': ['SOCKS5 ', addr, '; ', 'SOCKS ', addr],
        'h': ['PROXY ', addr],
    }
    return ''.join(args[proxy_type])


if __name__ == '__main__':
    app.run()
