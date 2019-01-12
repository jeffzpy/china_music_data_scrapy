import scrapy
import json

class WWYMusicSpider(scrapy.Spider):
    name = 'WWYMusicSpider'
    start_urls = ['https://music.163.com/discover/playlist']

    def parse(self, response):
        typeList = response.xpath('//*[@id="cateListBox"]/div[2]/dl')
        # print(typeList)
        print('------------------------------')

        for tagItem in typeList:
            musicType = tagItem.xpath('.//dt/text()').extract_first()
            print(musicType)

            if musicType == '风格':
                for tagItem2 in tagItem.xpath('.//dd/a'):
                    musicType2 = tagItem2.xpath('.//text()').extract_first()
                    linkAddress = tagItem2.xpath('.//@href').extract_first()

                    musicListAddrPerType = response.urljoin(linkAddress)
                    # print(musicType2, linkAddress, musicListAddrPerType)
                    if musicType2 == '摇滚':
                        yield scrapy.Request(url = musicListAddrPerType, callback = self.parse_collectionList, meta = {'musicType': musicType ,'musicSubType': musicType2})
                    # break
                # break
                # print('musicType打印结束------------------------------')

        # print('------------------------------')
        # print(tagList)

    def parse_collectionList(self, response):
        print('执行方法 parse_collectionList')
        musicType = response.meta['musicType']
        musicSubType = response.meta['musicSubType']
       
        musicList = response.xpath('//*[@id="m-pl-container"]/li')
        for musicItem in musicList:
            setLinkAddress = musicItem.xpath('.//div/a/@href').extract_first()

            musicDetailList = 'https://music.163.com'+ setLinkAddress
            yield scrapy.Request(url = musicDetailList, callback = self.parse_musicList, meta = {'musicType': musicType ,'musicSubType': musicSubType}, priority = 2)
            # break
        # return
        nextPageUrl = response.xpath('//*[@id="m-pl-pager"]/div/a[11]/@href').extract_first()
        if nextPageUrl:
            nextPageUrl = nextPageUrl.replace(' ','')
            absoluteNextPageUrl = 'https://music.163.com'+ nextPageUrl.replace('\t','')
            yield scrapy.Request(url = absoluteNextPageUrl, callback = self.parse_collectionList, meta = {'musicType': musicType ,'musicSubType': musicSubType}, priority = 1)
        else:
            print("Find none")            

    def parse_musicList(self, response):
        print('parse_musicList')
        musicType = response.meta['musicType']
        musicSubType = response.meta['musicSubType']
        musicList = response.xpath('//*[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li')

        for item in musicList:
            musicSubLink = item.xpath('.//a/@href').extract_first()
            musicID = musicSubLink[9:]

            url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + musicID + '?csrf_token=6c4f0275a0bb05a9b51ffe894847b4fb'

            musicName = item.xpath('.//text()').extract_first()

            print('请求歌曲评论数目开始 musicID = ', musicID)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
            metaDic = {'musicType':musicType, 'musicSubType':musicSubType, 'musicName':musicName}
            formdata = {'params':'3bOPmgxtNeOnln31wRtL4lg6wu8XlSTJ7u1/hKZOQtM3jpGRr14cczX8rH8mW51IRd+eSCPS1X42ZVxVPED3rtKxk+o28UqyOT8pP6yhiHiDPymnIMWuGGMRIc8jLEtKnkIpd+quR+YCIgJ9E57SQLsULOcB13VkPUuiciPtoTA0Er07SWq19WoyOb7cStBAT9VNr5ToswiBdOOJKewg2qVj8dWFQapsEtLeCFmQ5do=', 'encSecKey':'78b1b25b04d8b9ee311447e7af1aa9bb3e77f52f9d0bb9ef22875d08b484218de2003a003593018eb68393cf851287b1e9010ae499d5c05fc2fc31c33316cf11fb1429be4f838a68dea133f89810da7a8db955064446b27f02e6da20acdf6a58a161150feb1a2f9da4ec98ee2a10003775710d5afed2eb682d35f573bc1f28d9'}
            yield scrapy.FormRequest(url, formdata = formdata, callback = self.parse_music, headers = headers, meta = metaDic, priority = 10)

    def parse_music(self, response):
        print('最后解析啦')        
        musicType = response.meta['musicType']
        musicSubType = response.meta['musicSubType']
        musicName = response.meta['musicName']

        # print(response.text)
        # str1 = response.xpath('//*[@id="cnt_comment_count"]').extract()
        comment = json.loads(response.text)
            
        commentNum = comment['total']

        musicItemDic = {
            'tab':musicType,
            'subTab':musicSubType,
            'title':musicName,
            'commemtNum':commentNum
        }

        if int(commentNum) > 10000:
            print('我想要的数据', musicItemDic)
            yield musicItemDic
        else:
            print('过滤掉的数据', musicItemDic)
