#!/bin/python3
import json
import requests
from typing import Union

from vh113 import DEFAULT_IP

ALLOWED_CHANNELS = [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117]
DEFAULT_TEAMS = ['111', '112', '113', '114', '115', '116']
DEFAULT_CHANNEL = 13
DEFAULT_PASSWORD = 'vividhosting'
DEFAULT_CONFIG = {
	'blueVlans': '40_50_60',
	'channel': DEFAULT_CHANNEL,
	'channelBandwidth': '40MHz',
	'redVlans': '10_20_30',
	'stationConfigurations': {
		'red1': {
			'ssid': DEFAULT_TEAMS[0],
			'wpaKey': DEFAULT_PASSWORD
		},
		'red2': {
			'ssid': DEFAULT_TEAMS[2],
			'wpaKey': DEFAULT_PASSWORD
		},
		'red3': {
			'ssid': DEFAULT_TEAMS[4],
			'wpaKey': DEFAULT_PASSWORD
		},
		'blue1': {
			'ssid': DEFAULT_TEAMS[1],
			'wpaKey': DEFAULT_PASSWORD
		},
		'blue2': {
			'ssid': DEFAULT_TEAMS[3],
			'wpaKey': DEFAULT_PASSWORD
		},
		'blue3': {
			'ssid': DEFAULT_TEAMS[5],
			'wpaKey': DEFAULT_PASSWORD
		}
	}
}


def send_config(config: Union[dict, str], ip_address=DEFAULT_IP, timeout=0.1) -> dict:
	"""Send a given configuration object to a VH-113 at the given IP address."""
	# convert a config object to a JSON string
	if type(config) == dict:
		config = json.dumps(config)

	try:
		r = requests.post(f'http://{ip_address}/configuration', json.dumps(config), timeout=timeout)
		if r.status_code == 202:
			res = {
				'success': True
			}
			print('Success! Please wait 60 seconds for networks.')
		else:
			res = {
				'success': False,
				'error': f'Error {r.status_code} while communicating with {ip_address}',
				'debug': r.reason
			}
	except requests.exceptions.ConnectTimeout as e:
		res = {
			'success': False,
			'error': f'Couldn\'t reach a VH-113 at {ip_address}. Are you connected to the radio through the PoE injector?',
			'debug': str(e)
		}

	return res


# if run as a script
if __name__ == "__main__":
	import argparse

	# parse arguments
	parser = argparse.ArgumentParser(description='Configures a connected VH-113 field access point for up to 6 robots.')
	parser.add_argument('-d', '--debug', action='store_true', help='print out data before sending')
	parser.add_argument('-a', '--ip-address', type=str, help='VH-113 IP address', default=DEFAULT_IP)
	parser.add_argument('-p', '--password', type=str, help='password for all SSIDs', default=DEFAULT_PASSWORD)
	parser.add_argument('-c', '--channel', type=int, choices=ALLOWED_CHANNELS, help='Wi-Fi 6 GHz channel', default=DEFAULT_CHANNEL)
	parser.add_argument('teams', type=int, nargs=argparse.REMAINDER, help='team numbers in order: red1 blue1 red2 blue2 red3 blue3')
	args = parser.parse_args()

	# update list of team numbers
	teams = DEFAULT_TEAMS

	# build configuration object
	configuration = DEFAULT_CONFIG
	configuration['channel'] = args.channel
	for i in range(6):
		key = f'{"red" if i % 2 == 0 else "blue"}{i // 2 + 1}'
		configuration['stationConfigurations'][key]['wpaKey'] = args.password
		if i < len(args.teams):
			configuration['stationConfigurations'][key]['ssid'] = args.teams[i]

	# print configuration object if debug was enabled
	if args.debug:
		print(configuration)

	# send configuration object to VH-113
	result = send_config(configuration)
	if result['success']:
		print('Success! Please wait 60 seconds for networks.')
	else:
		print(result['error'])
