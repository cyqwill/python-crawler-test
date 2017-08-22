# python爬虫测试练习

##第一个python爬虫的小项目

准备做一个收集马蜂窝中游记的爬虫，收集一个地点的所有游记
的文字内容，然后通过对文字内容进行语义情感分析，得出各个
地点的好感程度。

test中是些测试的小例子，requests/selenium等测试

### -----

目前以三亚为例，通过城市页面，使用游记的ajax接口，获取所有游记的链接
通过各个链接访问单独的游记页面，下载游记内容

(mfw-links-crawler)通过地点单页，获取地点的所有游记的链接

(mfw-logs-crawler)简单使用多进程处理+随机代理处理了一下，爬取速度快了一点。

(proxy)完成一个简单的离线proxy获取工具，后期可使用别的动态代理池维护工具

(mfw-logs-parser)游记内容解析，应用jieba,snownlp提取游记内容的关键词，
情感指数，可是没有相关模型，简单先填一下

TODO：
游记的语义分析
游记深层次属性提取，图片数量，评论数等
重新梳理一下架构，拆分抓取页面与解析页面功能，结合消息队列等工具，分化功能
同步爬取，多进程，多线程，分布式
评论的爬取，由评论内容，统计游记的好坏
