import os
from helpers import *
from billboard import Billboard
from setlist import Setlist
from spotify import Spotify

def enrich_config_with_billboard(config):
	print(f'{center(f'[{smart_time()}] Gathering top {config['topArtists']} artists from Billboard...', display=False)}\r', end='')
	existing_names = {p['artistName'].lower() for p in config.get('playlists', []) if 'artistName' in p}

	setlist_scraper = Setlist(None)
	billboard_scraper = Billboard(config['topArtists'])
	new_entries = []

	artists = billboard_scraper.get_billboard_top_artists()
	for i in range(len(artists)):
		print(f'{center(f'[{smart_time()}] [{i + 1}/{len(artists)}] Gathering artistId from setlist.fm...', display=False)}\r', end='')
		artist = artists[i]
		if artist.lower() not in existing_names:
			artist_id = setlist_scraper.get_artist_id_by_name(artist)
			if artist_id:
				new_entries.append({
					'artistId': artist_id,
					'artistName': artist,
					'scope': 'playlist-modify-public',
					'playlistId': ''
				})

	if new_entries:
		config.setdefault('playlists', []).extend(new_entries)
		config['playlists'] = sorted(config['playlists'], key=lambda p: p['artistName'].lower())
		with open('config.json', 'w') as f:
			json.dump(config, f, indent=4)
		center(f"{smart_time()}] Added {len(new_entries)} new artists to config.json.")
	return config

def update_playlist(sp, config, playlist, track_ids, artist, song_count):
	playlist_id = playlist.get('playlistId')
	if not playlist_id:
		new_playlist = sp.spotify.user_playlist_create(
			config['username'],
			f'{artist} Updated Setlist',
			public=True,
			collaborative=False,
			description=f'Playlist automatically updated from recent setlist.fm setlists | Last updated: {smart_time()} ET. | github.com/DanteArcese/SpotifySetlist.'
		)
		playlist_id = new_playlist.get('id') if new_playlist else None
		if playlist_id:
			playlist['playlistId'] = playlist_id
			with open('config.json', 'w') as f:
				json.dump(config, f, indent=4)
	else:
		sp.spotify.user_playlist_change_details(
			config['username'],
			playlist_id,
			f'{artist} Updated Setlist',
			public=True,
			collaborative=False,
			description=f'Playlist automatically updated from recent setlist.fm setlists | Last updated: {smart_time()} ET. | github.com/DanteArcese/SpotifySetlist.'
		)

	if playlist_id:
		sp.spotify.playlist_replace_items(playlist_id, track_ids)
		center(f'[{smart_time()}] Successfully updated {artist} playlist with {len(track_ids):,}/{song_count:,} songs.')
	
	return config


if __name__ == '__main__':
	header()
	config = load_from_json('config.json')
	set_spotify_environment(config)

	if os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
		while True:
			if config['topArtists']:
				config = enrich_config_with_billboard(config)
			for playlist in config['playlists']:
				print(f'{center(f'[{smart_time()}] Gathering songs for {playlist['artistName']} playlist...', display=False)}\r', end='')
				scraper = Setlist(playlist['artistId'])
				songs = scraper.get_songs()

				if not songs:
					continue

				print(f'{center(f'[{smart_time()}] Gathering track IDs for {playlist['artistName']} playlist...', display=False)}\r', end='')
				sp = Spotify(config['username'], playlist['scope'])
				track_ids = [tid for tid in (sp.get_track_id(song) for song in songs) if tid]

				if track_ids:
					config = update_playlist(sp, config, playlist, track_ids, playlist['artistName'], len(songs))
			smart_sleep(3600)
	else:
		center(f'[{smart_time()}] Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET before proceeding.')