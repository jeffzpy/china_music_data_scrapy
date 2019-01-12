import scrapy

class MusicSpider(scrapy.Spider):
    """docstring for MusicSpider"""

    name = 'MusicSpider'

    start_urls = ['http://music.taihe.com/tag']

    def parse(self, response):
        # filename = 'MusicSpider.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        tagList = response.xpath('//*[@id="subPage"]/div[2]/div/div/div[2]/div/div/div/dl')
        print('------------------------------')
        for tagItem in tagList:
            musicType = tagItem.xpath('.//dt/text()').extract_first()
            # print(musicType)

        # if musicType == '心情':
            for tagItem2 in tagItem.xpath('.//span'):
                musicType2 = tagItem2.xpath('.//a/text()').extract_first()
                linkAddress = tagItem2.xpath('.//@href').extract_first()

                musicListAddrPerType = response.urljoin(linkAddress)
                # print(musicType2, linkAddress, musicListAddrPerType)
                # if musicType2 == '激情':
                yield scrapy.Request(url = musicListAddrPerType, callback = self.parse_detail, meta = {'musicType': musicType ,'musicSubType': musicType2})

            # print('musicType打印结束------------------------------')

        # print('------------------------------')
        # print(tagList)

    def parse_detail(self, response):
        # print('========')
        musicType = response.meta['musicType']
        musicSubType = response.meta['musicSubType']
       
        musicList = response.xpath('//*[@id="subPage"]/div[2]/div[1]/div/div[3]/div/div[2]/div[1]/ul/li')
        # print(musicList)
        for musicItem in musicList:
            musicName = musicItem.xpath('.//div/span[4]/a/text()').extract_first()

            # print(musicName)
            yield {
                'tab':musicType,
                'subTab':musicSubType,
                'title':musicName
            }
        # print('Find start')
        nextPageUrl = response.xpath('//*[@id="subPage"]/div[2]/div[1]/div/div[3]/div/div[2]/div[2]/div/div/a[@class="page-navigator-next"]/@href').extract_first()
        # print(nextPageUrl)

        if nextPageUrl:
            # print('Find It')
            nextPageUrl = nextPageUrl.replace(' ','')
            # print('下一页 组合前 url =', nextPageUrl.replace('\t',''), response.url)
            absoluteNextPageUrl = 'http://music.taihe.com'+ nextPageUrl.replace('\t','')
            # print('下一页 url =', absoluteNextPageUrl)
            yield scrapy.Request(url = absoluteNextPageUrl, callback = self.parse_detail, meta = {'musicType': musicType ,'musicSubType': musicSubType})
        else:
            print("Find none")            


