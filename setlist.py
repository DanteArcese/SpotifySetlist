import html
import json
import requests
from bs4 import BeautifulSoup
from helpers import load_from_json

class Setlist:
	def __init__(self, artist_id):
		'''Initialize Setlist class with some attributes.

		Attributes:
			artist_id: Artist ID to scrape for songs.
			base_url: Base URL of setlist.fm.
			homepage: Homepage URL of setlist.fm.
			session: Session used across all HTTP requests.
		'''
		self.artist_id = artist_id
		self.base_url = 'https://www.setlist.fm/setlists/'
		self.homepage = 'https://www.setlist.fm'
		self.session = requests.Session()

	def get_artist_id_by_name(self, artist_name):
		'''Search setlist.fm and return the artistId for a given artist name.
		
		Returns:
			setlist.fm artistId.
		'''
		from urllib.parse import quote_plus
		search_url = f'https://www.setlist.fm/search?query={quote_plus(artist_name)}'
		response = self.session.get(search_url)
		soup = BeautifulSoup(response.content, 'html.parser')

		found_artist = soup.find('div', class_='searchTopArtist')
		if found_artist:
			anchor = found_artist.find('a', href=True, title=lambda t: t and 'setlists' in t.lower())
			if anchor:
				href = anchor['href']
				if href.startswith('setlists/'):
					return href.replace('setlists/', '').replace('.html', '')
		return None

	def get_songs(self):
		'''Obtains the songs on an artist's recent setlists from setlist.fm.

		Returns:
			List of dictionaries containing a Spotify query and the main artist behind the song.
		'''
		response = self.session.get(self.base_url + self.artist_id)
		soup = BeautifulSoup(response.content, 'html.parser')

		# Extract and normalize artist name
		artist = (tag := soup.find('meta', attrs={'property': 'qc:artist'})) and tag.get('content')

		# Prepare deduping set and result container
		seen = set()
		results = []

		# Loop through each setlist preview block
		setlist_previews = soup.find_all('div', class_='setlistPreview')

		for preview in setlist_previews:
			# Skip if the setSummary is empty (no songs listed yet)
			set_summary = preview.find('div', class_='setSummary')
			if not set_summary or not set_summary.find('li'):
				continue

			# Find the individual setlist page URL
			link = preview.find('a', class_='summary url')
			if not link or not link.get('href'):
				continue

			setlist_url = link['href'].replace('..', self.homepage)

			# Fetch the full setlist page
			setlist_response = self.session.get(setlist_url)
			setlist_soup = BeautifulSoup(setlist_response.content, 'html.parser')

			# Extract songs from songLabel links
			song_tags = setlist_soup.find_all('a', class_='songLabel')
			for tag in song_tags:
				song_name = tag.get_text(strip=True)
				if song_name not in seen:
					seen.add(song_name)
					results.append({
						'query': f'{song_name} {artist}',
						'artist': artist,
						'songName': song_name
					})

		return results