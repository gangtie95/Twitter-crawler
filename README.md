#Twitter Crawler
该项目主要使用selenium和beautifulsoup爬取Twitter特定网页的博文，姓名，用户名，转，赞，分享等内容。
项目不需要登录Twitter账号，可以直接运行爬取。  
**启动前，需要自己解决翻墙问题**
------------
##Requirement
> python==3.7.9  
> selenium==3.141.0  
> beautifulsoup4==4.9.3  
> pandas==1.2.1
--------------
##说明
1. 为了方便，爬下来的数据保存成了CSV和xlsx两种格式，CSV文件如果用Excel打开，可能会乱码，需要手动改一下编码
2. 目前测试，大多数网站都可以爬取，如果有无法爬取的网站，有可能是标签变动了，建议修改标签再使用

##运行
首先将*twitter_url_network.txt*文件中的网址改为 自己所需爬取的网址  
直接运行*Twitter-crawler.py*

或者
> python Twitter-crawler.py
