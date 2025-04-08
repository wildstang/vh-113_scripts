#!/bin/python3
import json
import requests

from vh113 import DEFAULT_IP


def get_status(ip_address=DEFAULT_IP, timeout=0.5) -> dict:
	"""Requests the status of a VH-113 located at the given IP address."""
	try:
		# send a status request
		r = requests.get(f'http://{ip_address}/status', timeout=timeout)

		# parse valid return statuses
		if r.status_code == 200:
			res = json.loads(r.text)
			res['success'] = True
		else:
			res = {
				'success': False,
				'error': f'Error {r.status_code} while communicating with {ip_address}',
				'debug': r.reason
			}
	except (requests.exceptions.ConnectTimeout, OSError) as e:
		res = {
			'success': False,
			'error': f'Couldn\'t reach a VH-113 at {ip_address}. Are you connected to the radio through the PoE injector?',
			'debug': str(e)
		}

	return res


# if run as a script
if __name__ == "__main__":
	import time
	import argparse

	# parse arguments
	parser = argparse.ArgumentParser(description='Continually logs the status of a connected VH-113 field access point.')
	parser.add_argument('-a', '--ip-address', type=str, help='VH-113 IP address', default=DEFAULT_IP)
	parser.add_argument('-d', '--debug', action='store_true', help='print out each received status block')
	parser.add_argument('-m', '--mac', action='store_true', help='print out MAC address of connected robots')
	parser.add_argument('-s', '--strength', action='store_true', help='print out strength of connected robots')
	parser.add_argument('-b', '--bandwidth', action='store_true', help='print out bandwidth of connected robots')
	args = parser.parse_args()

	# get status, forever
	while True:
		try:
			# send a status request
			start = time.monotonic()
			result = get_status(args.ip_address)

			# parse valid return statuses
			if result['success']:
				print('-----')
				print(result['status'], 'Channel:', result['channel'], 'Bandwidth:', result['channelBandwidth'], 'Red VLANs:', result['redVlans'], 'Blue VLANs:', status['blueVlans'])
				for key in result['stationStatuses']:
					station: dict = result['stationStatuses'][key]
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
					print(result)
			else:
				print(result['error'])
		# exit on ctrl + c
		except KeyboardInterrupt:
			break

		# run once per second
		if time.monotonic() - start < 1:
			time.sleep(1 - (time.monotonic() - start))
