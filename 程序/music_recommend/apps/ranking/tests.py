import requests
import os
import bs4
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

headers = {
     'user - agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.116Safari / 537.36'
}

#创建文件夹
if not os.path.exists('D:/网易云音乐'):
    os.mkdir('D:/网易云音乐')

# 实现无可视化界面（固定写法）
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#获取音乐id
def get_music_ids(url):
    # 初始化browser对象
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    # 访问该url
    browser.get(url=url)
    # 由于网页中有iframe框架，进行切换
    browser.switch_to.frame('g_iframe')
    # 等待0.5秒
    sleep(0.5)
    # 抓取到页面信息
    page_text = browser.execute_script("return document.documentElement.outerHTML")
    # 退出浏览器
    browser.quit()
    # 提取音乐的id，名字，歌手名
    soup = bs4.BeautifulSoup(page_text, 'html.parser')
    music_ids = soup.select("div[class='td w0'] a")  # 音乐id
    music_id = music_ids[0].get("href")
    music_id = music_id.split('=')[-1]
    return music_id

#获取音乐名称
def get_music_names(url):
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    browser.get(url=url)
    browser.switch_to.frame('g_iframe')
    sleep(0.5)
    page_text = browser.execute_script("return document.documentElement.outerHTML")
    browser.quit()
    soup = bs4.BeautifulSoup(page_text, 'html.parser')
    music_names = soup.select("div[class='td w0'] a b")  # 音乐名字
    music_name=music_names[0].get("title")
    return music_name

#获取歌手名称
def get_music_singers(url):
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    browser.get(url=url)
    browser.switch_to.frame('g_iframe')
    sleep(0.5)
    page_text = browser.execute_script("return document.documentElement.outerHTML")
    browser.quit()
    soup = bs4.BeautifulSoup(page_text, 'html.parser')
    music_singers = soup.select("div[class='td w1'] a")
    music_singer=music_singers[0].string
    return music_singer

#下载音乐
def download_music(url,name,singer):
    print(url)
    response=requests.get(url=url,headers=headers)
    music_data=response.content
    music_path_name='{}_{}.mp3'.format(name,singer)
    music_path='D:/网易云音乐/'+music_path_name
    with open(music_path,'wb') as f:
        f.write(music_data)
        print(music_path_name,'下载成功')

#主函数
def main(name):
    try:
        url = 'https://music.163.com/#/search/m/?s=' + name + '&type=1'
        #music_name=get_music_names(url)
        #musice_singer=get_music_singers(url)
        music_id=get_music_ids(url)
        music_url= 'http://music.163.com/song/media/outer/url?id=' + music_id + '.mp3'
        browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
        browser.get(url=music_url)
        sleep(0.5)
        page_text = browser.execute_script("return document.documentElement.outerHTML")
        browser.quit()
        soup = bs4.BeautifulSoup(page_text, 'html.parser')
        music_source=soup.select("video source")
        source_url=music_source[0].get('src')
        return source_url
    except Exception as e:
        return ''
    #download_music(source_url,music_name,musice_singer)

if __name__ =='__main__'    :
    main()

