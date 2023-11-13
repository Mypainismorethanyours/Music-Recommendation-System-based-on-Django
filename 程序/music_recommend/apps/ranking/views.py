import re

from django.db.models import Max, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from index.models import Song, Dynamic,Music
from .predict import predict_baseon_item
def check(str):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False
class RankingView(View):

    def get(self, request):
        from .tests import main
        results = Music.objects.all()
        #
        # for i in results:
        #     url = main(i.name)
        #     if not url:
        #         url = ''
        #
        #     Music.objects.filter(id=i.id).update(
        #         url=url
        #     )


            #rint('{}已更新{}'.format(i.name,url))
        # 热搜歌曲
        search_song = Dynamic.objects.all().order_by('-dynamic_plays')[0]
        music_type = Song.objects.filter(song_id=search_song.song_id).first().song_type
        songs = Song.objects.filter(song_type=music_type).all()
        print(music_type)
        # 歌曲分类列表
        # All_list = Song.objects.values('song_type').distinct() # 去重
        # 歌曲信息列表
        song_type = request.GET.get('type', '')

        return render(request, 'ranking/ranking.html', {'songs':songs})


def predict(request):
    inputText = request.POST.get("name")
    result= predict_baseon_item(str(inputText))
    print('1111',result)
    result_list = []
    if not result:
        pid = Music.objects.filter(name=inputText).first().pid
        all_data = Music.objects.filter(pid=pid).all()
        if len(all_data) > 10:
            all_data = all_data[0:10]
        for i in all_data:
            result_dict = {
                'name':i.name,
                'singer':i.singer,
                'src':'/static/songFile/体面.m4a',

            }
            result_list.append(result_dict)
    else:
        for i in result:
            obj_music = Music.objects.filter(name=i).first()
            result_dict = {
                'name': i,
                'src': '/static/songFile/体面.m4a',
            }
            result_list.append(result_dict)
            print(result_list)
    return JsonResponse({'input_text': inputText, 'result_list': result_list})