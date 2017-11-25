import scrapy
from scrapy.selector import Selector
from splashtry.items import SplashtryItem

from scrapy_splash import SplashRequest
import json



class MySpider(scrapy.Spider):
    name="ssplash"
    allowed_domains=["twitter.com"]
    start_urls = ["https://twitter.com/hashtag/mentalhealth?src=hash"]

    def start_requests(self):
        for url in self.start_urls:
            script="""
            function wait_for(splash, condition)
                 while not condition() do
                      assert(splash:runjs("window.scrollTo(0,document.body.scrollHeight)"))
                      splash:wait(1)
                 end
            end
            function main(splash)
               assert(splash:go(splash.args.url))
               assert(splash:set_viewport_full())
               assert(splash:wait(0.1))


               assert(splash:runjs("window.scrollTo(0,document.body.scrollHeight)"))
               splash:wait(2)
               wait_for(splash, function()
                    local h=splash:evaljs("document.body.scrollHeight")
                    local t=splash:evaljs("document.body.scrollTop")
                    if h==t+768 then 
                       return true
                    else 
                       return false
                    end
               end)
           
                 
               return splash:html()
            end
            """
                 
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'args':{'lua_source':script,},
                    'endpoint':'execute',
                }
            })

    def parse(self, response):
        sel=Selector(response)
        items=[]
        account=response.xpath('//a[@class="account-group js-account-group js-action-profile js-user-profile-link js-nav"]')
        emails=account.xpath('.//span[@class="username u-dir"]/b/text()').extract()
        profile_names=response.xpath('//strong[@class="fullname show-popup-with-id "]/text()').extract()
        times=response.xpath('.//div[@class="stream-item-header"]/small/a/span[@class="u-hiddenVisually"]/text()').extract()

        for email, profile_name, time in zip(emails, profile_names, times):
            item=SplashtryItem()
            item['email']=email
            item['profile_name']=profile_name
            item['time']=time
            item['fallower_num']="0"
            items.append(item)
        return items


