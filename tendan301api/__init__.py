import requests
import base64
import json


class TendaError(Exception):
    pass


class TendaManager:

    __AUTH_URL = 'http://{}/login/Auth'
    __GET_QOS = 'http://{}/goform/getQos'
    __SET_QOS = 'http://{}/goform/setQos'
    __COOKIE = ''

    def __init__(self, IP, PASSWORD):
        self.IP = IP
        self.PASSWORD = PASSWORD
        self.__AUTH_URL = self.__AUTH_URL.format(IP)
        self.__GET_QOS = self.__GET_QOS.format(IP)
        self.__SET_QOS = self.__SET_QOS.format(IP)
        self.do_login()

    def __encodeB64(self, string):
        return base64.encodebytes(string.encode()).decode("utf-8")[0:-1]

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

    def get_online_devices(self):
        request_headers = {
            'Cookie': 'bLanguage=en; {}'.format(self.__COOKIE),
            'DNT': '1',
            'Host': '192.168.0.1',
            'Referrer': 'http://192.168.0.1/index.html'
        }

        params = {
            'modules': 'onlineList'
        }

        response = requests.get(
            self.__GET_QOS, params, headers=request_headers, allow_redirects=False)

        if response.status_code == 302:
            self.do_login()
            return self.get_online_devices()
        else:
            return response.json()['onlineList']

    def get_black_list(self):
        request_headers = {
            'Cookie': 'bLanguage=en; {}'.format(self.__COOKIE),
            'DNT': '1',
            'Host': '192.168.0.1',
            'Referrer': 'http://192.168.0.1/index.html'
        }

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

        request_headers = {
            'Cookie': 'bLanguage=en; {}'.format(self.__COOKIE),
            'DNT': '1',
            'Host': '192.168.0.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referrer': 'http://192.168.0.1/index.html'
        }

        online_list = self.get_online_devices()
        black_list = self.get_black_list()
        qos_list = ''

        should_be_online = list(filter(
            lambda online_device: online_device['qosListMac'] != mac_address, online_list))
        should_be_blocked = list(filter(
            lambda online_device: online_device['qosListMac'] == mac_address, online_list))[0]

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

    def Test(self):
        print(self.__COOKIE)