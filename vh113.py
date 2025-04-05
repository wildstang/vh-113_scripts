import json
import requests

ip = '192.168.69.1'

data = {
	'blueVlans': '40_50_60',
	'channel': 13,
	'channelBandwidth': '40MHz',
	'redVlans': '10_20_30',
	'stationConfigurations': {
		'blue1': {
			'ssid': '112',
			'wpaKey': 'vividhosting'
		},
		'blue2': {
			'ssid': '114',
			'wpaKey': 'vividhosting'
		},
		'blue3': {
			'ssid': '116',
			'wpaKey': 'vividhosting'
		},
		'red1': {
			'ssid': '111',
			'wpaKey': 'vividhosting'
		},
		'red2': {
			'ssid': '113',
			'wpaKey': 'vividhosting'
		},
		'red3': {
			'ssid': '115',
			'wpaKey': 'vividhosting'
		}
	}
}

r = requests.post(f'http://{ip}/configuration', json.dumps(data))

print(r.status_code, r.reason)