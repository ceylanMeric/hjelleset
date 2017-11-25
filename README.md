# hjelleset
Crawling twitter with Scrapy- Splash
NOTE: READ BEFORE RUN.

There are trysplash and click_coordinates files, in the Spiders folder.
Trysplash download tweets from hashtag but it is limited because we didn't look page with twiter account. 
This file work. Output is twet.json.
Click_coordinates file, try to enter account and print screenshot of page to get unlimited content. 
After false enterance trying with account informations, I have banned from twitter. Thus, my workings stop here.
This file doesn't work properly. Output is click.png.
  

-----------------------------------------------------------------------------------
command run: docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600

-----------

scrapy crawl spider ssplash -o twet.json

=============

