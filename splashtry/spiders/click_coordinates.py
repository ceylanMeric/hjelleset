        # -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
import base64
from PIL import Image
import io

class Get_Page_Spider(scrapy.Spider):
    name = "click_coordinates"

    def start_requests(self):

        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            assert(splash:set_viewport_full())
            assert(splash:wait(0.1))
            --local x = splash:select('#cboxClose')
            --local xbounds = x:bounds()
            --assert(x:mouse_click{x=xbounds.width/2, y=xbounds.height/2})
            --assert(splash:wait(0.5))
            --splash:mouse_click(560,93)
            --assert(splash:wait(0.3))

            -- <input type="text" class="text-input email-input js-signin-email" name="session[username_or_email]"   
            local search_input = splash:select('input[name="session[username_or_email]"]') 
            search_input:send_text("XXXXXXXXXX")
            local search_input = splash:select('input[name="session[password]"]')
            --<input type="password" class="text-input" name="session[password]"
            search_input:send_text("XXXXXXX")
            assert(splash:wait(1))
            --<input type="submit" class="EdgeButton EdgeButton--primary EdgeButton--medium submit js-submit"
            local submit_button = splash:select('input[class^="EdgeButton EdgeButton--primary EdgeButton--medium submit js-submit"]')
            submit_button:click()

            assert(splash:wait(2))


            local image = assert(splash:png{render_all=true})

            return {png=image}
            --return { html = splash:html(), png = splash:png() }
      end
        
        end
        """
        """
        function wait_for(splash, condition)
                 while not condition() do
                      assert(splash:runjs("window.scrollTo(0,document.body.scrollHeight)"))
                      splash:wait(0.5)
                 end
            end
            function main(splash)
               assert(splash:go(splash.args.url)) 
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
            
                 
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'args':{'lua_source':script,'timeout':1200,},
                    'endpoint':'execute',

        """

        url = 'https://twitter.com/hashtag/mentalhealth?src=hash'

        yield SplashRequest(url=url,  
            endpoint='execute', callback = self.after_render, args={
            'lua_source': script,
            'url' : url,
            })
    

    def after_render(self,response):
        png_bytes = base64.b64decode(response.data['png'])
        image = Image.open(io.BytesIO(png_bytes))
        image.save('click.png')
        #yield {'title':response.xpath('//title/text()').extract()}"""
        #return {'response_body' : response.body }