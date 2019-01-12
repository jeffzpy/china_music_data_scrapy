# -*- coding: utf-8 -*-
import scrapy
import json


class Qqsingerspider(scrapy.Spider):
    name = 'QQSinger'
    allowed_domains = ['y.qq.com']
    start_urls = ['https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI8933079022457886&g_tk=5381&jsonpCallback=getUCGI8933079022457886&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"comm":{"ct":24,"cv":10000},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":2,"genre":-100,"index":-100,"sin":0,"cur_page":1}}}']

    currentPageIndex = 1

    def parse(self, response):
        responseText = response.text
        leftPosIndex = responseText.index('(')

        contentText = responseText[leftPosIndex + 1:len(responseText)-1]

        dic = json.loads(contentText)
        singerList = dic['singerList']['data']['singerlist']
        for singerItem in singerList:
            country = singerItem['country']
            if len(country) == 0:
                country = '其它'
            yield {'tab':'人物', 'subTab':'歌手', 'title':singerItem['singer_name'], 'country':country}

        self.currentPageIndex = self.currentPageIndex + 1

        if self.currentPageIndex < 2:
            nextPageURLStr = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI8933079022457886&g_tk=5381&jsonpCallback=getUCGI8933079022457886&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"comm":{"ct":24,"cv":10000},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":-100,"sin":%d,"cur_page":%d}}}' %(self.currentPageIndex*80, self.currentPageIndex)
            yield scrapy.Request(url = nextPageURLStr, callback = self.parse)
        else:
            print('-------此次爬虫结束-------')
            self.logger.info('-------此次爬虫结束-------')
