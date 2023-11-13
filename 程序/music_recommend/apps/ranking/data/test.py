# _*_ coding: utf-8 _*_
# @Time : 2022/11/7 19:58 
# @Author : xxx 
# @Version：V 0.1
# @File : test.py
# @desc :

for line in open('./popular.playlist', 'r', encoding='UTF-8'):
    contents = line.strip().split("\t")
    name, tags, playlist_id, subscribed_count = contents[0].split("##")
    #print(name,tags,playlist_id,subscribed_count)
    for song in contents[1:]:
        try:
            song_id, song_name, artist, popularity = song.split(":::")
            print(song_name,artist,popularity)
        except Exception as e:
            print("song format error", e)
            print(song + "\n")
