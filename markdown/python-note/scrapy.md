# 笔记

## Scrapy简介

爬取网站数据，提取结构性数据而编写的应用框架

## 架构概览

1. Scrapy Engine
   >引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。 详细内容查>看下面的数据流(Data Flow)部分。

   此组件相当于爬虫的“大脑”，是整个爬虫的调度中心
2. 调度器(Scheduler)
   >调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎。

   初始的爬取URL和后续在页面中获取的待爬取的URL将放入调度器中，等待爬取。同时调度器会自动去除重复的URL（如果特定的URL不需要去重也可以通过设置实现，如post请求的URL）
3. 下载器(Downloader)
   >下载器负责获取页面数据并提供给引擎，而后提供给spider。
4. Spiders
   >Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每个spider负责处理一个特定(或一些)网站
5. Item Pipeline
   >Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数据库中)。

   当页面被爬虫解析所需的数据存入Item后，将被发送到项目管道(Pipeline)，并经过几个特定的次序处理数据，最后存入本地文件或存入数据库。
6. 下载器中间件(Downloader middlewares)
   >下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的response。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。

   通过设置下载器中间件可以实现爬虫自动更换user-agent、IP等功能。
7. Spider中间件(Spider middlewares)
   >Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出(items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。
8. 数据流(Data flow)
    >引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的URL(s)。  
    >引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度。  
    >引擎向调度器请求下一个要爬取的URL。  
    >调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给>下载器(Downloader)。  
    >一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回>(response)方向)发送给引擎。  
    >引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
    >Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。  
    >引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度>器。  
    >(从第二步)重复直到调度器中没有更多地request，引擎关闭该网站。  

## 创建项目

```sh
scrapy startproject scrapyspider
```

该命令将会创建包含下列内容的scrapyspider目录:

```text
scrapyspider/
    scrapy.cfg
    scrapyspider/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```

这些文件分别是:

scrapy.cfg: 项目的配置文件。  
scrapyspider/: 该项目的python模块。之后您将在此加入代码。  
scrapyspider/items.py: 项目中的item文件。  
scrapyspider/pipelines.py: 项目中的pipelines文件。  
scrapyspider/settings.py: 项目的设置文件。  
scrapyspider/spiders/: 放置spider代码的目录。

## 编写第一个爬虫(Spider)

>Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。
>其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 item 的方法。
>为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:
>name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
>start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
>parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。

## 创建spider

```sh
scrapy genspider douban_spider https://book.douban.com/tag/
```

## 启动爬虫

打开终端进入项目所在路径(即:scrapyspider路径下)运行下列命令：

```sh
scrapy crawl douban_spider
```

## 问题

1. 禁止内置的中间件,设置USER_AGENT为none,能获取到页面。

## 命令行工具

### 全局命令:

startproject  
settings  
runspider  
shell  
fetch  
view  
version  

### 项目(Project-only)命令:
crawl  
check  
list  
edit  
parse  
genspider  
deploy  
bench  

## Items

爬取的主要目标就是从非结构性的数据源提取结构性数据

### 声明Item

Item使用简单的class定义语法以及 Field 对象来声明。例如:

```python
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
```

### Item字段

Field 对象指明了每个字段的元数据(metadata)。

### 创建item

```sh
>>> product = Product(name='Desktop PC', price=1000)
>>> print product
Product(name='Desktop PC', price=1000)
```

### 获取字段的值

```sh
>>> product['name']
Desktop PC
>>> product.get('name')
Desktop PC

>>> product['price']
1000

>>> product['last_updated']
Traceback (most recent call last):
    ...
KeyError: 'last_updated'

>>> product.get('last_updated', 'not set')
not set

>>> product['lala'] # getting unknown field
Traceback (most recent call last):
    ...
KeyError: 'lala'

>>> product.get('lala', 'unknown field')
'unknown field'

>>> 'name' in product  # is name field populated?
True

>>> 'last_updated' in product  # is last_updated populated?
False

>>> 'last_updated' in product.fields  # is last_updated a declared field?
True

>>> 'lala' in product.fields  # is lala a declared field?
False
```

### 设置字段的值

```sh
>>> product['last_updated'] = 'today'
>>> product['last_updated']
today

>>> product['lala'] = 'test' # setting unknown field
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

### 获取所有获取到的值

```sh
>>> product.keys()
['price', 'name']

>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]
```

### 复制item:

```sh
>>> product2 = Product(product)
>>> print product2
Product(name='Desktop PC', price=1000)

>>> product3 = product2.copy()
>>> print product3
Product(name='Desktop PC', price=1000)
```

### 根据item创建字典(dict)

```sh
>>> dict(product) # create a dict from all populated values
{'price': 1000, 'name': 'Desktop PC'}
```

### 根据字典(dict)创建item

```sh
>>> Product({'name': 'Laptop PC', 'price': 1500})
Product(price=1500, name='Laptop PC')

>>> Product({'name': 'Laptop PC', 'lala': 1500}) # warning: unknown field in dict
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

### 扩展Item

可以通过继承原始的Item来扩展item(添加更多的字段或者修改某些字段的元数据)。

```sh
class DiscountedProduct(Product):
    discount_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()
```

也可以通过使用原字段的元数据,添加新的值或修改原来的值来扩展字段的元数据:

```sh
class SpecificProduct(Product):
    name = scrapy.Field(Product.fields['name'], serializer=my_serializer)
```

这段代码在保留所有原来的元数据值的情况下添加(或者覆盖)了 name 字段的 serializer 。

## Spiders

Spider类定义了如何爬取某个(或某些)网站

对spider来说，爬取的循环类似下文:

1. 以初始的URL初始化Request，并设置回调函数。 当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数。
spider中初始的request是通过调用 start_requests() 来获取的。 start_requests() 读取 start_urls 中的URL， 并以 parse 为回调函数生成 Request 。

2. 在回调函数内分析返回的(网页)内容，返回 Item 对象或者 Request 或者一个包括二者的可迭代容器。 返回的Request对象之后会经过Scrapy处理，下载相应的内容，并调用设置的callback函数(函数可相同)。

3. 在回调函数内，您可以使用 选择器(Selectors) (您也可以使用BeautifulSoup, lxml 或者您想用的任何解析器) 来分析网页内容，并根据分析的数据生成item。

最后，由spider返回的item将被存到数据库(由某些 Item Pipeline 处理)或使用 Feed exports 存入到文件中

### Spider参数

Spider可以通过接受参数来修改其功能。 spider参数一般用来定义初始URL或者指定限制爬取网站的部分

在运行 crawl 时添加 -a 可以传递Spider参数:

```sh
scrapy crawl myspider -a category=electronics
```

Spider在构造器(constructor)中获取参数:

```sh
import scrapy

class MySpider(Spider):
    name = 'myspider'

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
        # ...
```

Spider参数也可以通过Scrapyd的 schedule.json API来传递


### 类crapy.spider.Spider

Spider是最简单的spider。每个其他的spider必须继承自该类(包括Scrapy自带的其他spider以及您自己编写的spider)。 Spider并没有提供什么特殊的功能。 其仅仅请求给定的 start_urls/start_requests ，并根据返回的结果(resulting responses)调用spider的 parse 方法。  

name  
定义spider名字的字符串(string)。spider的名字定义了Scrapy如何定位(并初始化)spider，所以其必须是唯一的  

allowed_domains  
可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。

start_urls  
URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。 因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取

start_requests()  
该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。
当spider启动爬取并且未制定URL时，该方法被调用。 当指定了URL时，make_requests_from_url() 将被调用来创建Request对象。 该方法仅仅会被Scrapy调用一次，因此您可以将其实现为生成器。
该方法的默认实现是使用 start_urls 的url生成Request。
如果您想要修改最初爬取某个网站的Request对象，您可以重写(override)该方法。 例如，如果您需要在启动时以POST登录某个网站，你可以这么写:

```js
def start_requests(self):
    return [scrapy.FormRequest("http://www.example.com/login",
                               formdata={'user': 'john', 'pass': 'secret'},
                               callback=self.logged_in)]

def logged_in(self, response):
    # here you would extract links to follow and return Requests for
    # each of them, with another callback
    pass
```

make_requests_from_url(url)  
该方法接受一个URL并返回用于爬取的 Request 对象。 该方法在初始化request时被 start_requests() 调用，也被用于转化url为request。
默认未被复写(overridden)的情况下，该方法返回的Request对象中， parse() 作为回调函数，dont_filter参数也被设置为开启。 (详情参见 Request).

parse(response)  
当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。
parse 负责处理response并返回处理的数据以及(/或)跟进的URL。 Spider 对其他的Request的回调函数也有相同的要求。
该方法及其他的Request回调函数必须返回一个包含 Request 及(或) Item 的可迭代的对象。  
参数:	response (Response) – 用于分析的response

log(message[, level, component])  
使用 scrapy.log.msg() 方法记录(log)message。 log中自动带上该spider的 name 属性

closed(reason)  
当spider关闭时，该函数被调用。 该方法提供了一个替代调用signals.connect()来监听 spider_closed 信号的快捷方式。

### 类scrapy.contrib.spiders.CrawlSpider

爬取一般网站常用的spider。其定义了一些规则(rule)来提供跟进link的方便的机制。 也许该spider并不是完全适合您的特定网站或项目，但其对很多情况都使用。 因此您可以以其为起点，根据需求修改部分方法。当然您也可以实现自己的spider。

除了从Spider继承过来的(您必须提供的)属性外，其提供了一个新的属性:

rules  
一个包含一个(或多个) Rule 对象的集合(list)。 每个 Rule 对爬取网站的动作定义了特定表现。 Rule对象在下边会介绍。 如果多个rule匹配了相同的链接，则根据他们在本属性中被定义的顺序，第一个会被使用。

该spider也提供了一个可复写(overrideable)的方法:
parse_start_url(response)  
当start_url的请求返回时，该方法被调用。 该方法分析最初的返回值并必须返回一个 Item 对象或者 一个 Request 对象或者 一个可迭代的包含二者对象。

爬取规则(Crawling rules)

classscrapy.contrib.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)

link_extractor  
是一个 Link Extractor 对象。 其定义了如何从爬取到的页面提取链接。

callback  
是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中每获取到链接时将会调用该函数。该回调函数接受一个response作为其第一个参数， 并返回一个包含 Item 以及(或) Request 对象(或者这两者的子类)的列表(list)。

**警告**
当编写爬虫规则时，请避免使用 parse 作为回调函数。 由于 CrawlSpider 使用 parse 方法来实现其逻辑，如果 您覆盖了 parse 方法，crawl spider 将会运行失败。

cb_kwargs  
包含传递给回调函数的参数(keyword argument)的字典。

follow  
是一个布尔(boolean)值，指定了根据该规则从response提取的链接是否需要跟进。 如果 callback 为None， follow 默认设置为 True ，否则默认为 False 。

process_links  
是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中获取到链接列表时将会调用该函数。该方法主要用来过滤。

process_request  
是一个callable或string(该spider中同名的函数将会被调用)。 该规则提取到每个request时都会调用该函数。该函数必须返回一个request或者None。 (用来过滤request)

### 类scrapy.contrib.spiders.XMLFeedSpider

XMLFeedSpider被设计用于通过迭代各个节点来分析XML源(XML feed)。 迭代器可以从 iternodes ， xml ， html 选择。 鉴于 xml 以及 html 迭代器需要先读取所有DOM再分析而引起的性能问题， 一般还是推荐使用 iternodes 。 不过使用 html 作为迭代器能有效应对错误的XML。

### 类scrapy.contrib.spiders.CSVFeedSpider

该spider除了其按行遍历而不是节点之外其他和XMLFeedSpider十分类似。 而其在每次迭代时调用的是 parse_row() 

delimiter  
在CSV文件中用于区分字段的分隔符。类型为string。 默认为 ',' (逗号)。

headers  
在CSV文件中包含的用来提取字段的行的列表。参考下边的例子。

parse_row(response, row)  
该方法接收一个response对象及一个以提供或检测出来的header为键的字典(代表每行)。 该spider中，您也可以覆盖 adapt_response 及 process_results 方法来进行预处理(pre-processing)及后(post-processing)处理。

### classscrapy.contrib.spiders.SitemapSpider


## 选择器

通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分

### 使用选择器(selectors)

Scrapy selector是以 文字(text) 或 TextResponse 构造的 Selector 实例。 其根据输入的类型自动选择最优的分析方法(XML vs HTML):

```sh
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
```

以文字构造:

```sh
>>> body = '<html><body><span>good</span></body></html>'
>>> Selector(text=body).xpath('//span/text()').extract()
[u'good']
```

以response构造:

```sh
>>> response = HtmlResponse(url='http://example.com', body=body)
>>> Selector(response=response).xpath('//span/text()').extract()
[u'good']
```

为了方便起见，response对象以 .selector 属性提供了一个selector， 您可以随时使用该快捷方法:

```sh
>>> response.selector.xpath('//span/text()').extract()
[u'good']
```

### 使用选择器

Scrapy提供了两个实用的快捷方式: response.xpath() 及 response.css():

```sh
>>> response.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]
>>> response.css('title::text')
[<Selector (text) xpath=//title/text()>]
```

.xpath() 及 .css() 方法返回一个类 SelectorList 的实例, 它是一个新选择器的列表。这个API可以用来快速的提取嵌套数据。

为了提取真实的原文数据，你需要调用 .extract() 方法如下:

```sh
>>> response.xpath('//title/text()').extract()
[u'Example website']
```

注意CSS选择器可以使用CSS3伪元素(pseudo-elements)来选择文字或者属性节点:

```
>>> response.css('title::text').extract()
[u'Example website']
```

### xpath语法

xpath//开头

1. 所有节点 //*
2. 通过 / 查找元素的子节点和通过//查找子孙节点 //li/a
3. 父节点..来查找
4. 属性匹配 用@符号进行属性过滤 '//li[@class="item-2"]'
5. 文本获取 text()方法获取节点中的文本
6. 属性获取 通过@获取属性值 //li/a/@href
7. 属性多值匹配 通过contains()方法， //li[contains(@class, "li")]/a/text()
8. 多属性匹配 匹配多个属性，使用运算符and来链接。//li[contains(@class, "li") and @name="item"]/a/text()
9. 按序选择 利用中括号传入索引的方式获取特定次序的节点 
    //li[1]/a/text  第一个节点
    //li[last()]/a/text() 最后一个节点  
    //li[position()<3]/a/text() 选取位置小于3的li节点，也就是1和2的节点
    //li[last()-2]/a/text() 选取倒数第三个节点
10. 节点轴选择  
    ancestor获取所有祖先节点，//li[1]/ancestor::\*获取所有的祖先节点，后面跟两个冒号::，然后是节点的选择器.  
    attribute 可以获取所有属性值 //li[1]/attrbute::\*  
    child 获取所有直接子节点 //li[i]/child::a[@href="link1.html"],选href属性为link1.html的a节点  
    descendant 获取所有的子节点 //li[1]/descendant::span  
    following 获取当前节点后的所有节点 //li[1]/following::*[1]  
    following-sibling 获取当前节点之后的所有同级节点 //li[1]/following-sibling::\*

### 嵌套选择器

选择器方法( .xpath() or .css() )返回相同类型的选择器列表，因此你也可以对这些选择器调用选择器方法

### 结合正则表达式使用选择器

Selector 也有一个 .re() 方法，用来通过正则表达式来提取数据 不同于使用 .xpath() 或者 .css() 方法, .re() 方法返回unicode字符串的列表

## 使用相对XPaths

记住如果你使用嵌套的选择器，并使用起始为 / 的XPath，那么该XPath将对文档使用绝对路径，而且对于你调用的 Selector 不是相对路径。

比如，假设你想提取在 <div> 元素中的所有 <p> 元素。首先，你将先得到所有的 <div> 元素:

```sh
>>> divs = response.xpath('//div')
```

开始时，你可能会尝试使用下面的错误的方法，因为它其实是从整篇文档中，而不仅仅是从那些 <div> 元素内部提取所有的 <p> 元素:

```sh
>>> for p in divs.xpath('//p'):  # this is wrong - gets all <p> from the whole document
...     print p.extract()
```

下面是比较合适的处理方法(注意 .//p XPath的点前缀):

```sh
>>> for p in divs.xpath('.//p'):  # extracts all <p> inside
...     print p.extract()
```

另一种常见的情况将是提取所有直系 <p> 的结果:

```sh
>>> for p in divs.xpath('p'):
...     print p.extract()
```

### 正则表达式

例如在XPath的 starts-with() 或 contains() 无法满足需求时， test() 函数可以非常有用。

例如在列表中选择有”class”元素且结尾为一个数字的链接:

sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract()

### Item Loaders

Item Loader在每个(Item)字段中都包含了一个输入处理器和一个输出处理器｡ 输入处理器收到数据时立刻提取数据 (通过 add_xpath(), add_css() 或者 add_value() 方法) 之后输入处理器的结果被收集起来并且保存在ItemLoader内. 收集到所有的数据后, 调用 ItemLoader.load_item() 方法来填充,并得到填充后的 Item 对象. 这是当输出处理器被和之前收集到的数据(和用输入处理器处理的)被调用.输出处理器的结果是被分配到Item的最终值｡

在 Spider 中典型的Item Loader的用法, 使用 Items chapter 中声明的 Product item:

```python
from scrapy.contrib.loader import ItemLoader
from myproject.items import Product

def parse(self, response):
    l = ItemLoader(item=Product(), response=response)
    l.add_xpath('name', '//div[@class="product_name"]')
    l.add_xpath('name', '//div[@class="product_title"]')
    l.add_xpath('price', '//p[@id="price"]')
    l.add_css('stock', 'p#stock]')
    l.add_value('last_updated', 'today') # you can also use literal values
    return l.load_item()
```

如前一节所见，输入和输出处理器可以在Item Loader定义中声明，并且以这种方式声明输入处理器是非常常见的。但是，还有一个地方可以指定要使用的输入和输出处理器:在Item Field元数据中。下面是一个例子:

```python
import scrapy

from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

def filter_price(value):
    if value.isdigit():
        return value

class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_price),
        output_processor=TakeFirst(),
    )
```

```sh
>>> from scrapy.contrib.loader import ItemLoader
>>> il = ItemLoader(item=Product())
>>> il.add_value('name', [u'Welcome to my', u'<strong>website</strong>'])
>>> il.add_value('price', [u'&euro;', u'<span>1000</span>'])
>>> il.load_item()
{'name': u'Welcome to my website', 'price': u'1000'}
```

## scrapy shell 命令

启动终端 

```sh
scrapy shell <url>
```

可用的Scrapy对象
Scrapy终端根据下载的页面会自动创建一些方便使用的对象，例如 Response 对象及 Selector 对象(对HTML及XML内容)。

这些对象有:

crawler - 当前 Crawler 对象.  
spider - 处理URL的spider。 对当前URL没有处理的Spider时则为一个 Spider 对象。  
request - 最近获取到的页面的 Request 对象。 您可以使用 replace() 修改该request。或者 使用 fetch 快捷方式来获取新的request。  
response - 包含最近获取到的页面的 Response 对象。  
sel - 根据最近获取到的response构建的 Selector 对象。   
settings - 当前的 Scrapy settings

### 在spider中启动shell来查看response

在spider的某个位置中查看被处理的response， 以确认您期望的response到达特定位置。

这可以通过 scrapy.shell.inspect_response 函数来实现

```python
import scrapy

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net",
    ]

    def parse(self, response):
        # We want to inspect one specific response.
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        # Rest of parsing code.
```

## Item Pipeline

当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。

每个item pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的Python类。他们接收到Item并通过它执行一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。

以下是item pipeline的一些典型应用：

清理HTML数据  
验证爬取的数据(检查item包含某些字段)  
查重(并丢弃)  
将爬取结果保存到数据库中  

### 编写你自己的item pipeline

编写你自己的item pipeline很简单，每个item pipiline组件是一个独立的Python类，同时必须实现以下方法:

process_item(item, spider)
每个item pipeline组件都需要调用该方法，这个方法必须返回一个 Item (或任何继承类)对象， 或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理。

参数:	
item (Item 对象) – 被爬取的item
spider (Spider 对象) – 爬取该item的spider
此外,他们也可以实现以下方法:

open_spider(spider)
当spider被开启时，这个方法被调用。

参数:	spider (Spider 对象) – 被开启的spider
close_spider(spider)
当spider被关闭时，这个方法被调用

参数:	spider (Spider 对象) – 被关闭的spider

pipeline，它为那些不含税(price_excludes_vat 属性)的item调整了 price 属性，同时丢弃了那些没有价格的item:

```python 
from scrapy.exceptions import DropItem

class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
```

pipeline将所有(从所有spider中)爬取到的item，存储到一个独立地 items.jl 文件，每行包含一个序列化为JSON格式的item:

```python 
import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
```

一个用于去重的过滤器，丢弃那些已经被处理过的item。让我们假设我们的item有一个唯一的id，但是我们spider返回的多个item中包含有相同的id:

```python
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
```

### 启用一个Item Pipeline组件

为了启用一个Item Pipeline组件，你必须将它的类添加到 ITEM_PIPELINES 配置，就像下面这个例子:

```text
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
```
分配给每个类的整型值，确定了他们运行的顺序，item按数字从低到高的顺序，通过pipeline，通常将这些数字定义在0-1000范围内。


## Feed exports

实现爬虫时最经常提到的需求就是能合适的保存爬取到的数据，或者说，生成一个带有爬取数据的”输出文件”(通常叫做”输出feed”)，来供其他系统使用。

Scrapy自带了Feed输出，并且支持多种序列化格式(serialization format)及存储方式(storage backends)。

## Link Extractors

Scrapy默认提供2种可用的 Link Extractor, 但你通过实现一个简单的接口创建自己定制的Link Extractor来满足需求｡

每个LinkExtractor有唯一的公共方法是 extract_links ,它接收一个 Response 对象,并返回一个 scrapy.link.Link 对象｡Link Extractors,要实例化一次并且 extract_links 方法会根据不同的response调用多次提取链接｡

Link Extractors在 CrawlSpider 类(在Scrapy可用)中使用, 通过一套规则,但你也可以用它在你的Spider中,即使你不是从 CrawlSpider 继承的子类, 因为它的目的很简单: 提取链接｡

内置Link Extractor 参考

LxmlLinkExtractor 默认link extractor
```python
from scrapy.contrib.linkextractors import LinkExtractor
```

## Logging

Scrapy提供了log功能。您可以通过 scrapy.log 模块使用。当前底层实现使用了 Twisted logging ，不过可能在之后会有所变化。

log服务必须通过显示调用 scrapy.log.start() 来开启。

Log levels
Scrapy提供5层logging级别:

CRITICAL - 严重错误(critical)  
ERROR - 一般错误(regular errors)  
WARNING - 警告信息(warning messages)  
INFO - 一般信息(informational messages)  
DEBUG - 调试信息(debugging messages)  

### 如何设置log级别

您可以通过终端选项(command line option) –loglevel/-L 或 LOG_LEVEL 来设置log级别。

### 如何记录信息(log messages)

下面给出如何使用 WARNING 级别来记录信息的例子:

```python
from scrapy import log
log.msg("This is a warning", level=log.WARNING)
```

### scrapy.log模块
___

```python
scrapy.log.start(logfile=None, loglevel=None, logstdout=None)
```

启动log功能。该方法必须在记录(log)任何信息前被调用。否则调用前的信息将会丢失。

参数:  
logfile (str) – 用于保存log输出的文件路径。如果被忽略， LOG_FILE 设置会被使用。 如果两个参数都是 None ，log将会被输出到标准错误流(standard error)。  
loglevel – 记录的最低的log级别. 可用的值有: CRITICAL, ERROR, WARNING, INFO and DEBUG.  
logstdout (boolean) – 如果为 True ， 所有您的应用的标准输出(包括错误)将会被记录(logged instead)。 例如，如果您调用 “print ‘hello’” ，则’hello’ 会在Scrapy的log中被显示。 如果被忽略，则 LOG_STDOUT 设置会被使用。  
___

```python
scrapy.log.msg(message, level=INFO, spider=None)
```

记录信息(Log a message)

参数:	
message (str) – log的信息  
level – 该信息的log级别. 参考 Log levels.  
spider (Spider 对象) – 记录该信息的spider. 当记录的信息和特定的spider有关联时，该参数必须被使用。  
scrapy.log.CRITICAL
严重错误的Log级别

scrapy.log.ERROR
错误的Log级别 Log level for errors

scrapy.log.WARNING
警告的Log级别 Log level for warnings

scrapy.log.INFO
记录信息的Log级别(生产部署时推荐的Log级别)

scrapy.log.DEBUG
调试信息的Log级别(开发时推荐的Log级别)

___
Logging设置
以下设置可以被用来配置logging:

LOG_ENABLED
LOG_ENCODING
LOG_FILE
LOG_LEVEL
LOG_STDOUT

## 数据收集

## Telnet终端

Scrapy提供了内置的telnet终端，以供检查，控制Scrapy运行的进程。 telnet仅仅是一个运行在Scrapy进程中的普通python终端。因此您可以在其中做任何事。

telnet终端是一个 自带的Scrapy扩展 。 该扩展默认为启用，不过您也可以关闭

### 访问telnet终端

elnet终端监听设置中定义的 TELNETCONSOLE_PORT ，默认为 6023 。 访问telnet请输入:

```sh
telnet localhost 6023
>>>
```

Windows及大多数Linux发行版都自带了所需的telnet程序。

### telnet终端中可用的变量

telnet仅仅是一个运行在Scrapy进程中的普通python终端。因此您可以做任何事情，甚至是导入新终端。

telnet为了方便提供了一些默认定义的变量:


快捷名称 |	描述 |
-|-|
crawler | Scrapy Crawler (scrapy.crawler.Crawler 对象)
engine |Crawler.engine属性
spider | 当前激活的爬虫(spider)
slot | the engine slot
extensions	| 扩展管理器(manager) (Crawler.extensions属性)
stats	| 状态收集器 (Crawler.stats属性)
settings	| Scrapy设置(setting)对象 (Crawler.settings属性)
est	| 打印引擎状态的报告
prefs	| 针对内存调试 (参考 调试内存溢出)
p	| pprint.pprint 函数的简写
hpy	| 针对内存调试 (参考 调试内存溢出)


## 反爬

### UA伪装