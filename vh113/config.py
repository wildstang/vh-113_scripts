#!/bin/python3
import json
import argparse
import requests

# defaults
teams = ['111', '112', '113', '114', '115', '116']
channels = [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117]

# parse arguments
parser = argparse.ArgumentParser(description='Configures a connected VH-113 field access point for up to 6 robots.')
parser.add_argument('-d', '--debug', action='store_true', help='print out data before sending')
parser.add_argument('-a', '--ip-address', type=str, help='VH-113 IP address', default='192.168.69.1')
parser.add_argument('-p', '--password', type=str, help='password for all SSIDs', default='vividhosting')
parser.add_argument('-c', '--channel', type=int, choices=channels, help='Wi-Fi 6 GHz channel', default=13)
parser.add_argument('teams', type=int, nargs=argparse.REMAINDER, help='team numbers in order: red1 blue1 red2 blue2 red3 blue3')
args = parser.parse_args()

# update list of team numbers
for i in range(min(len(args.teams), 6)):
	teams[i] = str(args.teams[i])

# build configuration object
data = {
	'blueVlans': '40_50_60',
	'channel': args.channel,
	'channelBandwidth': '40MHz',
	'redVlans': '10_20_30',
	'stationConfigurations': {
		'red1': {
			'ssid': teams[0],
			'wpaKey': args.password
		},
		'red2': {
			'ssid': teams[2],
			'wpaKey': args.password
		},
		'red3': {
			'ssid': teams[4],
			'wpaKey': args.password
		},
		'blue1': {
			'ssid': teams[1],
			'wpaKey': args.password
		},
		'blue2': {
			'ssid': teams[3],
			'wpaKey': args.password
		},
		'blue3': {
			'ssid': teams[5],
			'wpaKey': args.password
		}
	}
}

# print configuration object if debug was enabled
if args.debug:
	print(data)

# send configuration object to VH-113
try:
	r = requests.post(f'http://{args.ip_address}/configuration', json.dumps(data), timeout=0.1)
	if r.status_code == 202:
		print('Success! Please wait 60 seconds for networks.')
	else:
		print(r.status_code, r.reason)
except requests.exceptions.ConnectTimeout:
	print(f'Couldn\'t reach a VH-113 at {args.ip_address}. Are you connected to the radio through the PoE injector?')
