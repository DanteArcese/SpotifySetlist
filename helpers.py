import json
import math
import os
from time import localtime, sleep, strftime

def center(text, padding=' ', length=100, clear=False, display=True):
	'''
	Center text at specified length with specified padding surrounding.

	Args:
		text: Text to center.
		padding: Single-character padding used to center text.
		length: Total length of the output string after centering.
		clear: If True, clears the terminal before printing.
		display: If True, prints the centered text; else returns it.

	Returns:
		None if display is True; otherwise the centered text string.
	'''
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	padding_count = max(0, (length - len(text)) // 2)
	left_padding = padding * padding_count
	right_padding = padding * (length - len(text) - padding_count)
	centered_text = f'{left_padding}{text}{right_padding}'
	if display:
		print(centered_text)
	else:
		return centered_text

def header():
	'''Clear previous output and display header text.'''
	os.system('cls' if os.name == 'nt' else 'clear')
	print('')
	center('SpotifySetlist by Dante Arcese')
	center('-', '-')

def load_from_json(file):
	'''
	Load JSON file into a dictionary. If file doesn't exist or contains invalid JSON,
	writes an empty dictionary to the file and returns it.

	Args:
		file: JSON filename.

	Returns:
		Dictionary loaded from JSON or empty dict if file missing/invalid.
	'''
	try:
		with open(os.path.relpath(file), 'r') as myfile:
			return json.load(myfile)
	except (IOError, json.JSONDecodeError):
		with open(os.path.relpath(file), 'w') as myfile:
			json.dump({}, myfile)
		return {}

def smart_sleep(delay):
	'''
	Sleeps for a specified amount of time, displaying a countdown message.

	Args:
		delay: Number of seconds to sleep.
	'''
	for a in range(delay, 0, -1):
		print(f'{center(f"Sleeping for {a:,} seconds...", display=False)}\r', end='', flush=True)
		sleep(1)
	center(f'[{smart_time()}] Successfully slept for {delay:,} seconds.')

def smart_time():
	'''Return the local time in YYYY-MM-DD HH:MM:SS 24hr format.'''
	return str(strftime('%Y-%m-%d %H:%M:%S', localtime()))

def set_spotify_environment(config):
	'''
	Sets the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables
	from a configuration file if they are not already set in the environment.

	Args:
		config: Dictionary loaded from JSON config containing the key
				'environmentVariables' which points to a file path. That
				file should contain the client ID and secret.

	Returns:
		None
	'''
	if not os.getenv('SPOTIPY_CLIENT_ID') or not os.getenv('SPOTIPY_CLIENT_SECRET'):
		environ = load_from_json(config['environmentVariables'])
		os.environ['SPOTIPY_CLIENT_ID'] = environ.get('SPOTIPY_CLIENT_ID', '')
		os.environ['SPOTIPY_CLIENT_SECRET'] = environ.get('SPOTIPY_CLIENT_SECRET', '')
		os.environ['SPOTIPY_REDIRECT_URI'] = config.get('redirectURI', '')