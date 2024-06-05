from flask import request,jsonify
from config import app
from ytmusicapi import YTMusic

@app.route('/band/<bandname>', methods=['GET'])
def get_songs(bandname):
    ytmusic = YTMusic()
    search_results = ytmusic.search(bandname,filter="songs", limit=6)
    lyricsList = []
    for song in search_results[:6]:
        videoIdOfSong = song["videoId"]
        browseIdOfSong = ytmusic.get_watch_playlist(videoId=videoIdOfSong)
        if browseIdOfSong and "lyrics" in browseIdOfSong:
            try:
                lyricsOfSong = ytmusic.get_lyrics(browseIdOfSong["lyrics"])
                if lyricsOfSong:
                    if song["thumbnails"] and len(song["thumbnails"]) > 0 and "url" in song["thumbnails"][0]:
                        lyricsList.append({"videoId":song["videoId"],"thumbnail": song["thumbnails"][0]["url"], "title":song["title"],"lyrics":lyricsOfSong})
                    else:
                        lyricsList.append({"title":song["title"],"lyrics":lyricsOfSong})

                    # lyricsList[song["title"]] = lyricsOfSong
                    # print(lyricsOfSong)
            except Exception as e:
                print("lyrics not found")

                
    browseId=ytmusic.get_watch_playlist(videoId="Kx7B-XvmFtE")

    return lyricsList

if __name__=="__main__":

    app.run(debug=False, host='0.0.0.0', port=5000)
