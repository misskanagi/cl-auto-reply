# cl-auto-reply
基于GAE的草榴自动回复器

简介:
====

这是一个基于GAE的草榴自动回复器，适合新手上路使用，每天发10贴，你可以自己指定哪个时间段发（见下文）。

前置准备：
========

* 你得有一个google账号
* 你得有一个草榴账号
* 下载python 2.7， 下载地址：<https://www.python.org/downloads/>
* 下载Google App Engine SDK for Python， 下载地址：<https://cloud.google.com/appengine/downloads>
* 墙内用户可能需要用VPN或者其他的翻墙软件

部署步骤：
========

1. 进入<https://appengine.google.com/>创建一个application，记住id。
2. 进入"gae"文件夹，找到"login_info.py"并打开，将文件中的username='XXX'里面的XXX改成你的草榴账号，下面的password='XXX'里面的XXX改成你的密码。
3. 如果要修改每天发帖的时间段，用写字板打开"gae"文件夹下的"cron.yaml"，修改文件中"schedule:"后面的内容，具体语法详见<https://cloud.google.com/appengine/docs/python/config/cron>。（**注意：里面的时间用的都是UTC时间。**）
4. 最后上传app，语法：`appcfg.py --oauth2 -A [你的appid] update gae/`（确保appcfg.py在PATH变量中）。

LICENSE:
========

MIT LICENSE
