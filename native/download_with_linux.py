#!/usr/bin/env python3
from __future__ import print_function

import os
import sys
import json
import struct
import subprocess

VERSION = '0.0.1'

try:
	sys.stdin.buffer

	# Python 3.x version
	# Read a message from stdin and decode it.
	def getMessage():
		rawLength = sys.stdin.buffer.read(4)
		if len(rawLength) == 0:
			sys.exit(0)
		messageLength = struct.unpack('@I', rawLength)[0]
		message = sys.stdin.buffer.read(messageLength).decode('utf-8')
		return json.loads(message)

	# Send an encoded message to stdout
	def sendMessage(messageContent):
		encodedContent = json.dumps(messageContent).encode('utf-8')
		encodedLength = struct.pack('@I', len(encodedContent))

		sys.stdout.buffer.write(encodedLength)
		sys.stdout.buffer.write(encodedContent)
		sys.stdout.buffer.flush()

except AttributeError:
	# Python 2.x version (if sys.stdin.buffer is not defined)
	print('Python 3.2 or newer is required.')
	sys.exit(-1)


def install():
	home_path = os.getenv('HOME')

	manifest = {
		'name': 'download_with',
		'description': 'Download With native host',
		'path': os.path.realpath(__file__),
		'type': 'stdio',
	}
	locations = {
		'chrome': os.path.join(home_path, '.config', 'google-chrome', 'NativeMessagingHosts'),
		'chrome-beta': os.path.join(home_path, '.config', 'google-chrome-beta', 'NativeMessagingHosts'),
		'chrome-unstable': os.path.join(home_path, '.config', 'google-chrome-unstable', 'NativeMessagingHosts'),
		'chromium': os.path.join(home_path, '.config', 'chromium', 'NativeMessagingHosts'),
		'firefox': os.path.join(home_path, '.mozilla', 'native-messaging-hosts'),
		'librewolf': os.path.join(home_path, '.librewolf', 'native-messaging-hosts'),
		'waterfox': os.path.join(home_path, '.waterfox', 'native-messaging-hosts'),
		'waterfox-g4': os.path.join(home_path, '.waterfox', 'native-messaging-hosts'),
		'thunderbird': os.path.join(home_path, '.thunderbird', 'native-messaging-hosts'),
	}
	filename = 'download_with.json'

	for browser, location in locations.items():
		if os.path.exists(os.path.dirname(location)):
			if not os.path.exists(location):
				os.mkdir(location)

			browser_manifest = manifest.copy()
			if browser in ['firefox', 'thunderbird', 'librewolf', 'waterfox', 'waterfox-g4']:
				browser_manifest['allowed_extensions'] = ['downloadwith@wirlaburla.github.io']
			else:
				browser_manifest['allowed_origins'] = [
					'chrome-extension://cogjlncmljjnjpbgppagklanlcbchlno/',  # Chrome
					'chrome-extension://fbmcaggceafhobjkhnaakhgfmdaadhhg/',  # Opera
				]

			with open(os.path.join(location, filename), 'w') as file:
				file.write(
					json.dumps(browser_manifest, indent=2, separators=(',', ': '), sort_keys=True).replace('  ', '\t') + '\n'
				)

def listen():
	receivedMessage = getMessage()
	if receivedMessage == 'ping':
		sendMessage({
			'version': VERSION,
			'file': os.path.realpath(__file__)
		})
	else:
		devnull = open(os.devnull, 'w')
		subprocess.Popen(receivedMessage, stdout=devnull, stderr=devnull)
		sendMessage(None)


if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'install':
			install()
			sys.exit(0)
	allowed_extensions = [
		'downloadwith@wirlaburla.github.io',
		'chrome-extension://cogjlncmljjnjpbgppagklanlcbchlno/',
		'chrome-extension://fbmcaggceafhobjkhnaakhgfmdaadhhg/',
	]
	for ae in allowed_extensions:
		if ae in sys.argv:
			listen()
			sys.exit(0)

	print('This is the Download With native helper, version %s.' % VERSION)
	print('Run this script again with the word "install" after the file name to install.')
