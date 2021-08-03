import requests
import json
import time


class ICSservice:
    def __init__(self, IP):
        self.IP = IP
        self._apikey = None
        self._session = requests.Session() 
        self._prefix = f'http://{IP}/api'

    def login(self, username, password):
        request = '/'.join([self._prefix, 'login', username, password])
        # print(request)
        response = self._session.get(request)
        assert response.status_code == 200
        # print(response.text)
        self._apikey = json.loads(response.text)['i']

    def logout(self):
        # This function doesn't appear to work.
        request = '/'.join([self._prefix, 'logout', self._apikey])
        # request = f'http://{IP}/en/user/logout'
        # print(request)
        response = self._session.get(request)
        assert response.status_code == 200
        # print(response.text)
        # self._apikey = None
        # self._sessionid = None

    def _checkloggedin(self):
        if self._apikey is None:
            raise RuntimeError("Not logged in")

    def get(self, line, address, channel, item):
        self._checkloggedin()
        request = '/'.join(
            [
                self._prefix,
                'getItem',
                self._apikey,
                str(line),
                str(address),
                str(channel),
                item,
            ]
        )
        # print(request)
        response = self._session.get(request)
        assert response.status_code == 200
        # print(response.text)
        return json.loads(response.text)

    def set(self, line, address, channel, item, value):
        self._checkloggedin()
        request = '/'.join(
            [
                self._prefix,
                'setItem',
                self._apikey,
                str(line),
                str(address),
                str(channel),
                item,
                value,
            ]
        )
        response = requests.get(request)
        assert response.status_code == 200

    def is_ramping(self, channel_tuple):
        line, address, channel = channel_tuple
        data2 = ics.get(line, address, channel, "Status.ramping")
        return bool(int(data2[0]['c'][0]['d']['v']))

    def set_voltage(self, channel_tuple, voltage, post_wait=1):
        """Set voltage of a channel_tuple (line, address, channel) in volts, and wait
        until ramping finishes. Wait an additional post_wait seconds after ramping
        completes"""
        line, address, channel = channel_tuple
        ics.set(line, address, channel, "Control.voltageSet", str(voltage))
        # time.sleep(1)
        while self.is_ramping(channel_tuple):
            pass
        time.sleep(post_wait)

    def get_voltage(self, channel_tuple):
        """Get voltage of a channel_tuple (line, address, channel) in volts"""
        line, address, channel = channel_tuple
        reponse = ics.get(line, address, channel, "Status.voltageMeasure")
        return float(reponse[0]['c'][0]['d']['v'])



if __name__ == '__main__':
    IP = 'REDACTED'
    username = 'REDACTED'
    password = 'REDACTED'

    ics = ICSservice(IP)
    ics.login(username, password)
    CHAN = (0, 3, 3)
    v = ics.get_voltage(CHAN)
    print("current_value:", v)
    if abs(v) < 15:
        v = 20
    else:
        v = 10
    ics.set_voltage(CHAN, v)
    v = ics.get_voltage(CHAN)
    print(v)
    
