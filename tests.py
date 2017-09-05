# coding: utf-8
import os
import unittest
from flask import url_for
from app import app
from config import Test


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config.from_object(Test)
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.test_client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_ctx.pop()

    def get_resp_text_content(self, resp):
        return resp.get_data(as_text=True)

    def test_index(self):
        resp = self.test_client.get(url_for('index'))
        self.assertTrue(u'功夫网列表转换' in self.get_resp_text_content(resp))

    def test_ipset(self):
        resp = self.test_client.get(url_for('ipset', args='ipsetname,127.0.0.1:1024'))
        self.assertTrue('rules for dnsmasq' in self.get_resp_text_content(resp))
        self.assertTrue('# end' in self.get_resp_text_content(resp))

    def test_ipset_missing_setname(self):
        resp = self.test_client.get(url_for('ipset', args='127.0.0.1:1024'))
        self.assertEqual(404, resp.status_code)

    def test_ipset_missing_port(self):
        resp = self.test_client.get(url_for('ipset', args='setname,127.0.0.1:'))
        self.assertEqual(404, resp.status_code)

    def test_ipset_invalid_port(self):
        resp = self.test_client.get(url_for('ipset', args='setname,127.0.0.1:999999'))
        self.assertEqual(404, resp.status_code)

    def test_dnsmasq(self):
        resp = self.test_client.get(url_for('dnsq', args='127.0.0.1:1024'))
        self.assertTrue('rules for dnsmasq' in self.get_resp_text_content(resp))
        self.assertTrue('# end' in self.get_resp_text_content(resp))

    def test_dnsmasq_missing_port(self):
        resp = self.test_client.get(url_for('ipset', args='127.0.0.1:'))
        self.assertEqual(404, resp.status_code)

    def test_dnsmasq_invalid_port(self):
        resp = self.test_client.get(url_for('ipset', args='127.0.0.1:999999'))
        self.assertEqual(404, resp.status_code)

    def test_pac_socks_proxy(self):
        resp = self.test_client.get('/pac/s,127.0.0.1:1024')
        self.assertTrue('SOCKS5 127.0.0.1:1024; SOCKS 127.0.0.1:1024' in self.get_resp_text_content(resp))

    def test_pac_http_proxy(self):
        resp = self.test_client.get('/pac/h,127.0.0.1:1024')
        self.assertTrue('PROXY 127.0.0.1:1024' in self.get_resp_text_content(resp))

    def test_pac_missing_proxy_type(self):
        resp = self.test_client.get('/pac/,127.0.0.1:1024')
        self.assertEqual(404, resp.status_code)

    def test_pac_invalid_proxy_type(self):
        resp = self.test_client.get('/pac/heyhey,127.0.0.1:1024')
        self.assertEqual(404, resp.status_code)

    def test_pac_missing_port(self):
        resp = self.test_client.get('/pac/s,127.0.0.1:')
        self.assertEqual(404, resp.status_code)


if __name__ == '__main__':
    unittest.main()
