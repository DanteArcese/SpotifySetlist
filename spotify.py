import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rapidfuzz import fuzz

class Spotify:
	def __init__(self, username, scope):
		'''Initialize Spotify class with some attributes.

		Attributes:
			spotify: Authorized Spotipy instance.
		'''
		token = spotipy.util.prompt_for_user_token(username, scope)
		self.spotify = spotipy.Spotify(auth=token)

	def get_track_id(self, song):
		def strip_feat(title):
			return title.split('(')[0].strip()

		results = self.spotify.search(song['query'], limit=10, offset=0, type='track', market=None)['tracks']['items']
		if not results:
			return None

		artist_lower = song['artist'].lower()
		song_name_lower = strip_feat(song['songName'].lower())

		# Filter by artist match
		filtered_results = [
			item for item in results
			if item.get('is_playable', True)  # defaults to True if missing
			and any(artist_lower == artist['name'].lower() for artist in item['artists'])
			]

		if not filtered_results:
			return None

		# Score each result
		scored = []
		best_score = 0

		for item in filtered_results:
			track_name = item['name']
			track_name_clean = strip_feat(track_name.lower())
			score = fuzz.ratio(song_name_lower, track_name_clean)
			best_score = max(best_score, score)
			scored.append((item, score))

		if best_score < 60:
			return None

		# Select top matches
		top_matches = [item for item, score in scored if score == best_score]

		# Tie-breaking
		def tie_breaker(item):
			is_explicit = item['explicit']
			popularity = item.get('popularity', 0)
			main_artist_first = (item['artists'][0]['name'].lower() == artist_lower)
			title_length = len(item['name'])
			return (is_explicit, popularity, main_artist_first, -title_length)

		best_track = sorted(top_matches, key=tie_breaker, reverse=True)[0]
		
		return best_track['uri'].split(':')[2]