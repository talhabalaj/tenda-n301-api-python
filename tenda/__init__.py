import requests
import base64
import json

from requests.api import request


class TendaError(Exception):
    pass

class TendaManager(object):

    __AUTH_URL = 'http://{}/login/Auth'
    __GET_QOS = 'http://{}/goform/getQos'
    __SET_QOS = 'http://{}/goform/setQos'
    __REBOOT_URL = 'http://{}/goform/sysReboot'
    __WIFI_SETTINGS_URL = 'http://{}/goform/getWifi'
    __COOKIE = ''

    def __init__(self, IP, PASSWORD):
        self.IP = IP
        self.PASSWORD = PASSWORD
        self.__AUTH_URL = self.__AUTH_URL.format(IP)
        self.__GET_QOS = self.__GET_QOS.format(IP)
        self.__SET_QOS = self.__SET_QOS.format(IP)
        self.__REBOOT_URL = self.__REBOOT_URL.format(IP)
        self.do_login()

    def __encodeB64(self, string):
        return base64.b64encode(string.encode()).decode("utf-8")

    def __bake_requests(self):
        return {
            'Cookie': 'bLanguage=en; {}'.format(self.__COOKIE),
            'DNT': '1',
            'Host': '%s' % (self.IP),
            'Referrer': 'http://%s/index.html' % (self.IP)
        }

    def do_login(self):
        form_data = {
            'password': self.__encodeB64(self.PASSWORD)
        }
        try:
            response = requests.post(
                self.__AUTH_URL, form_data, allow_redirects=False)
        except requests.exceptions.RequestException as e:
            raise TendaError(e)

        if 'Set-Cookie' in response.headers:
            self.__COOKIE = response.headers['Set-Cookie'].split(';')[0]
        else:
            raise TendaError('Authentication Failed')

    def get_online_devices_with_stats(self):
        request_headers = self.__bake_requests()

        params = {
            'modules': 'onlineList'
        }

        response = requests.get(
            self.__GET_QOS, params, headers=request_headers, allow_redirects=False)

        if response.status_code == 302:
            self.do_login()
            return self.get_online_devices_with_stats()
        else:
            return response.json()['onlineList']
        
    def limit_device(self, mac_address, download_speed, upload_speed):
        def set_limit_settings(device):
            device['qosListUpLimit'] = str(float(upload_speed))
            device['qosListDownLimit'] = str(float(download_speed))

        request_headers = self.__bake_requests()

        online_list = self.get_online_devices_with_stats()
        black_list = self.get_black_list()
        qos_list = ''

        should_be_online = list(filter(
            lambda online_device: online_device['qosListMac'] != mac_address, online_list))
        should_be_limited = list(filter(
            lambda online_device: online_device['qosListMac'] == mac_address.casefold(), online_list))

        if len(should_be_limited) > 0:
            should_be_limited = should_be_limited[0]
        else:
            raise TendaError('The device is not connected.')

        set_limit_settings(should_be_limited)
        should_be_online.append(should_be_limited)

        for online_device in should_be_online:
            qos_list += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                online_device['qosListHostname'], online_device['qosListRemark'], online_device['qosListMac'], online_device['qosListUpLimit'], online_device['qosListDownLimit'], online_device['qosListAccess'])

        for blocked_device in black_list:
            qos_list += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                blocked_device['qosListHostname'], blocked_device['qosListRemark'], blocked_device['qosListMac'], blocked_device['qosListUpLimit'], blocked_device['qosListDownLimit'], blocked_device['qosListAccess'])

        form_data = {
            'module1': 'qosList',
            'qosList': qos_list
        }

        response = requests.post(self.__SET_QOS, data=form_data,
                                 headers=request_headers, allow_redirects=False)

        err = response.json()['errCode']
        if err == '0':
            return True

    def get_black_list(self):
        request_headers = self.__bake_requests()

        params = {
            'modules': 'blackList'
        }

        response = requests.get(
            self.__GET_QOS, params, headers=request_headers, allow_redirects=False)

        if response.status_code == 302:
            self.do_login()
            return self.get_black_list()
        else:
            return response.json()['blackList']

    def block_device(self, mac_address):
        def set_block_settings(device):
            device['qosListAccess'] = 'false'
            device['qosListUpLimit'] = '0'
            device['qosListDownLimit'] = '0'

        request_headers = self.__bake_requests()

        online_list = self.get_online_devices_with_stats()
        black_list = self.get_black_list()
        qos_list = ''

        should_be_online = list(filter(
            lambda online_device: online_device['qosListMac'] != mac_address, online_list))
        should_be_blocked = list(filter(
            lambda online_device: online_device['qosListMac'] == mac_address.casefold(), online_list))

        if len(should_be_blocked) > 0:
            should_be_blocked = should_be_blocked[0]
        else:
            raise TendaError('The device is not connected.')

        set_block_settings(should_be_blocked)
        black_list.append(should_be_blocked)

        for online_device in should_be_online:
            qos_list += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                online_device['qosListHostname'], online_device['qosListRemark'], online_device['qosListMac'], online_device['qosListUpLimit'], online_device['qosListDownLimit'], online_device['qosListAccess'])

        for blocked_device in black_list:
            qos_list += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                blocked_device['qosListHostname'], blocked_device['qosListRemark'], blocked_device['qosListMac'], blocked_device['qosListUpLimit'], blocked_device['qosListDownLimit'], blocked_device['qosListAccess'])

        form_data = {
            'module1': 'qosList',
            'qosList': qos_list
        }

        response = requests.post(self.__SET_QOS, data=form_data,
                                 headers=request_headers, allow_redirects=False)

        err = response.json()['errCode']
        if err == '0':
            return True

    def get_wifi_settings(self):
        request_headers = self.__bake_requests()

        form_data = {
            'modules': 'wifiAgvCfg, wifiTime'
        }

        response = requests.post(
            self.__REBOOT_URL, data=form_data, headers=request_headers, allow_redirects=False)

        if response.status_code == 302:
            self.do_login()
            return self.reboot()
        else:
            err = response.json()['errCode']
            if err == '0':
                return True

    def reboot(self):
        request_headers = self.__bake_requests()

        form_data = {
            'module1': 'sysOperate',
            'action': 'reboot'
        }

        response = requests.post(
            self.__WIFI_SETTINGS_URL, data=form_data, headers=request_headers, allow_redirects=False)

        if response.status_code == 302:
            self.do_login()
            return self.get_wifi_settings()
        else:
            err = response.json()['errCode']
            if err == '0':
                return True
