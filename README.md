<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DanteArcese/SpotifySetlist">
    <img src="https://pbs.twimg.com/profile_images/1157026525566259200/mh3J6vIw_400x400.jpg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">SpotifySetlist</h3>

  <p align="center">
    Automated Spotify playlists with setlist.fm as the source.
    <br />
    <br />
    <a href="https://github.com/DanteArcese/SpotifySetlist/issues">Report Bug</a>
    ·
    <a href="https://github.com/DanteArcese/SpotifySetlist/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DanteArcese/SpotifySetlist.git
   ```
2. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create a Spotify developer application if you don't yet have one ([reference link](https://developer.spotify.com/dashboard/applications))
4. Set your Spotify ClientId and ClientSecret as the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables respectively ([reference doc](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

5. Edit config.json to your liking
   ```sh
   {
       "environmentVariables": "..\\Credentials\\credentials.json", # File where sensitive environment variables are stored
       "redirectURI": "http://localhost:8080/callback", # Obtained from https://developer.spotify.com/dashboard/applications
       "topArtists": 10, # Number of Billboard Top 100 artists to gather setlists for; 0 to only collect setlists for artists configured manually
       "username": "yap8b0pkw7hdeqbfydk2cyj0a", # Obtained from https://www.spotify.com/us/account/overview
       "playlists": [
           {
               "artistId": "young-thug-3bdd88c8", # Obtained from back-half of setlist.fm URL (Ex: https://www.setlist.fm/stats/young-thug-3bdd88c8.html)
               "artistName": "Young Thug", # Artist name
               "playlistId": "5GUwELpSDAMqIEqfdJmozJ", # Obtained from back-half of playlist URL (Ex: https://open.spotify.com/playlist/5GUwELpSDAMqIEqfdJmozJ); leave blank to create new playlist
               "scope": "playlist-modify-public" # Authorization scope for modifying the aforementioned playlistId (playlist-modify-public or playlist-modify-private)
           }
       ]
   }
   ```
6. Run main.py

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Scrape setlist.fm more conservatively

See the [open issues](https://github.com/DanteArcese/SpotifySetlist/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Dante Arcese - DanteArcese@gmail.com

Project Link: [https://github.com/DanteArcese/SpotifySetlist](https://github.com/DanteArcese/SpotifySetlist)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DanteArcese/SpotifySetlist.svg?style=for-the-badge
[contributors-url]: https://github.com/DanteArcese/SpotifySetlist/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DanteArcese/SpotifySetlist.svg?style=for-the-badge
[forks-url]: https://github.com/DanteArcese/SpotifySetlist/network/members
[stars-shield]: https://img.shields.io/github/stars/DanteArcese/SpotifySetlist.svg?style=for-the-badge
[stars-url]: https://github.com/DanteArcese/SpotifySetlist/stargazers
[issues-shield]: https://img.shields.io/github/issues/DanteArcese/SpotifySetlist.svg?style=for-the-badge
[issues-url]: https://github.com/DanteArcese/SpotifySetlist/issues