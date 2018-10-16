# python-study
Study python with girlfriend

## sendmail_study —— 发送邮件
- 从files文件夹下相应的excel文件中读取对应的邮箱地址：使用xlrd库
- 发送邮件之前使用正则表达式对邮箱格式进行校验：使用re库
- 发送相应Subject，Msg_body的邮件到指定邮箱地址：使用smtplib，email库

## crawl_study —— 爬取数据
- 从指定链接获取数据：使用requests库
- 从获取到的html源代码数据中解析出需要的数据：使用lxml.etree，re(正则)库
- 最后将获取到的所有数据写入到files文件夹下的指定文件中
