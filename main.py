import requests as rq
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
URL = "https://www.billboard.com/charts/hot-100/"
should_continue = False

#connection target website check
while not should_continue:
    date = str(input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:"))
    response = rq.get(url=f"{URL}{date}")
    if response.status_code == 200:
        should_continue = True
        response.raise_for_status()
    else:
        print("ya hedef siteye bağlanamadı ya da hatalı kullanıcı girişi")

#preparing the soup !
soup = BeautifulSoup(response.text, "html.parser")
musics = soup.select(selector="li > ul > li > h3")
musics = [i.getText().strip() for i in musics]
# musics_artists = soup.select(selector=".lrv-u-width-100p > ul > li > .c-label")
# musics_artists = [x.getText().strip() for x in musics_artists]
# musics_artists = [i for i in musics_artists if musics_artists.index(i) % 7 == 0]

# result = {}
# if len(musics_artists) == len(musics):
#     result = {f"{_+1}":{"Music":musics[_], "Artist":musics_artists[_]} for _ in range(len(musics_artists))}
#     """
#     result dict format:
#     {
#         NO:{
#             Music:music_name,
#             Artist:artist_name
#         }
#     }
#     """
#yukardaki kodlar extrem

#aşağıda auth yapıp playlist oluşturup şarkıları bulup playlist oluşturup ekliyoruz
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year =date.split("-")[0]


for song in musics:
    rslt = sp.search(q=f"track:{song} year:{year}", type="track")
    print(rslt)
    try:
        uri = rslt["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)