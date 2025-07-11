import requests
from bs4 import BeautifulSoup

class Billboard:
	def __init__(self, top_artists):
		'''Initialize Setlist class with some attributes.

		Attributes:
			top_artists: Number of top artists to gather.
			url: URL of the Billboard Artist 100 chart.
		'''
		self.top_artists = top_artists
		self.url = 'https://www.billboard.com/charts/artist-100/'

	def get_billboard_top_artists(self):
		'''Obtains top artists from billboard.com.

		Returns:
			List of Billboard top artist names.
		'''
		response = requests.get(self.url)
		soup = BeautifulSoup(response.content, 'html.parser')
		artists = []
		containers = soup.find_all('div', class_='o-chart-results-list-row-container')
		for container in containers:
			tag = container.find('h3', id='title-of-a-story')
			if tag:
				artist = tag.get_text(strip=True)
				if artist and artist not in artists:
					artists.append(artist)
					if len(artists) == self.top_artists:
						return artists

		return artists