#!/bin/python3
import json
import time
import argparse
import requests

# parse arguments
parser = argparse.ArgumentParser(description='Continually logs the status of a connected VH-113 field access point.')
parser.add_argument('-a', '--ip-address', type=str, help='VH-113 IP address', default='192.168.69.1')
parser.add_argument('-d', '--debug', action='store_true', help='print out each received status block')
parser.add_argument('-m', '--mac', action='store_true', help='print out MAC address of connected robots')
parser.add_argument('-s', '--strength', action='store_true', help='print out strength of connected robots')
parser.add_argument('-b', '--bandwidth', action='store_true', help='print out bandwidth of connected robots')
args = parser.parse_args()

while True:
	try:
		# send a status request
		start = time.monotonic()
		r = requests.get(f'http://{args.ip_address}/status', timeout=0.5)

		# parse valid return statuses
		if r.status_code == 200:
			status = json.loads(r.text)
			print('-----')
			print(status['status'], 'Channel:', status['channel'], 'Bandwidth:', status['channelBandwidth'], 'Red VLANs:', status['redVlans'], 'Blue VLANs:', status['blueVlans'])
			for key in status['stationStatuses']:
				station = status['stationStatuses'][key]
				if station['isLinked']:
					print(key, station['ssid'], 'CONNECTED')
					if args.mac:
						print('- MAC      ', station['macAddress'])
					print('- Status   ', station['connectionQuality'])
					if args.strength:
						print('- SNR      ', station['signalNoiseRatio'])
						print('- Strength', station['signalDbm'], 'dBm')
					if args.bandwidth:
						print('- Bandwidth', station['bandwidthUsedMbps'], 'Mbps')
						print('- Tx Rate  ', station['txRateMbps'], 'Mbps')
						print('- Rx Rate  ', station['rxRateMbps'], 'Mbps')
				else:
					print(key, station['ssid'], 'disconnected')

			# print the whole JSON object if debug is enabled
			if args.debug:
				print(status)
		else:
			print(f'Error {r.status_code} while communicating with {args.ip_address}')
			break
	except (requests.exceptions.ConnectTimeout, OSError):
		print(f'Couldn\'t reach a VH-113 at {args.ip_address}. Are you connected to the radio through the PoE injector?')
	except KeyboardInterrupt:
		break

	# run once per second
	if time.monotonic() - start < 1:
		time.sleep(1 - (time.monotonic() - start))
