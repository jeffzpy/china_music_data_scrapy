import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # start_urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]

    # def start_requests(self):
    #     start_urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=None)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def start_requests(self):
        urlstr = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_327156?csrf_token=87f74ee215e2e93793ecb6d0cd5b5500'

        print('请求歌曲评论数目开始')
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
        metaDic = {'type':'1'}
        formdata = {'params':'BOiJ0/CvvfnTjiI07ux85moiV3ATYONAqsxx1f4oMAKIcSaEWlZiMzi3dMaTpFPmrO83RaxF5kJI/fRP3NU3HCLFMVvg4Or2/g/rvclo1Ghkf2TDVc0mB/fZAjvLoQ29m1tNQEvZ3EhUOyFGCFblYZDKrcDItv+oT8/Cu5FlX88xHPwEZKFih1vcFymGAAeO6p0J5pSlBpf0JGs2urHbHsBGpAJVRHegvtPqvoe+rkc=', 'encSecKey':'0e3a7e1e0c6a67433ad199c06a34a2aaeddee47b41f41f7529c8bbca5cb921ca51e5150814d06315a6f49fe265b7be6160ec2c47005c247fe16bff47f9c25428995811e4966e9947cef8f0a3504b11b1d7341b76f7fc47c0135f72b82035c22241304d75d1255a58c66f791fe137057b00e24b09e325c10200a025862f336fb3'}
        # return scrapy.http.Request(url = urlstr, callback = self.parse, method = 'POST', body = json.dumps(formdata), headers = headers, errback = self.errorCallback)
        return [scrapy.FormRequest(urlstr, formdata = formdata, callback = self.parse, headers = headers)]


    def errorCallback(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        self.logger.info(response.text)    
        print('喜欢酸的甜就是真的我 ', response.text)
        return
            
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)