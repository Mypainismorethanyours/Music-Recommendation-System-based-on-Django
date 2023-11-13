from django.db import models
from user.models import MyUser

# 歌曲分类表label
class Label(models.Model):
    label_id = models.AutoField('序号', primary_key=True)
    label_name = models.CharField('分类标签', max_length=10)

    def __str__(self):
        return self.label_name

    class Meta:
        # 设置admin界面的显示内容
        verbose_name = '歌曲分类'
        verbose_name_plural = '歌曲分类'


# 歌曲信息表song
class Song(models.Model):
    song_id = models.AutoField('序号', primary_key=True)
    song_name = models.CharField('歌名', max_length=50)
    song_singer = models.CharField('歌手', max_length=50)
    song_time = models.CharField('时长', max_length=10)
    song_album = models.CharField('专辑', max_length=50)
    song_languages = models.CharField('语种', max_length=20)
    song_type = models.CharField('类型', max_length=20)
    song_release = models.CharField('发行时间', max_length=20)
    song_img = models.CharField('歌曲图片', max_length=20)
    song_lyrics = models.CharField('歌词', max_length=50, default='暂无歌词')
    song_file = models.CharField('歌曲文件', max_length=50)
    label = models.ForeignKey('Label', on_delete=models.CASCADE, verbose_name='歌曲分类')

    def __str__(self):
        return self.song_name

    class Meta:
        # 设置admin界面的显示内容
        verbose_name = '歌曲信息'
        verbose_name_plural = '歌曲信息'


# 歌曲动态表dynamic
class Dynamic(models.Model):
    dynamic_id = models.AutoField('序号', primary_key=True)
    dynamic_plays = models.IntegerField('播放次数')
    dynamic_search = models.IntegerField('搜索次数')
    dynamic_down = models.IntegerField('下载次数')
    song = models.ForeignKey('Song', on_delete=models.CASCADE, verbose_name='歌名')

    class Meta:
        verbose_name = '歌曲动态'
        verbose_name_plural = '歌曲动态'


# 歌曲点评论comment
class Comment(models.Model):
    comment_id = models.AutoField('序号', primary_key=True)
    comment_text = models.CharField('内容', max_length=500)
    comment_user = models.CharField('用户', max_length=20)
    comment_date = models.CharField('日期', max_length=50)
    count = models.IntegerField('点赞数量', default=1)

    song = models.ForeignKey('Song', on_delete=models.CASCADE, verbose_name='歌名')

    class Meta:
        verbose_name = '歌曲评论'
        verbose_name_plural = '歌曲评论'


class Music(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=255, default='')
    singer = models.CharField(verbose_name='歌手', max_length=255, default='')
    pid = models.CharField(verbose_name='父级目录',default='', max_length=10)
    remark = models.CharField(verbose_name='描述',default='', max_length=255)
    style = models.CharField(verbose_name='类别',default='', max_length=255)
    url = models.CharField(verbose_name='歌曲地址',default='', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'music'
        verbose_name = '音乐库'
        verbose_name_plural = '音乐库'


# class DianZan(models.Model):
#     id = models.AutoField('序号', primary_key=True)
#     count = models.IntegerField('点赞数量', default=1)
#     comment = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='评论')
#
#     class Meta:
#         verbose_name = '评论点赞'
#         verbose_name_plural = '评论点赞'


class ShouCang(models.Model):
    id=models.AutoField(primary_key=True)
    music = models.ForeignKey(Song,verbose_name='歌曲',on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser,verbose_name='用户',on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)


    class Meta:
        db_table = 'shoucang'
        verbose_name = '音乐收藏'
        verbose_name_plural = '音乐收藏'