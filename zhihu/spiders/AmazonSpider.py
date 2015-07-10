from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
class AmazonSpider(CrawlSpider):
    name = 'AmazonSpider'
    allowed_domains = ['amazon.cn']
    #start_urls = ['http://associates.amazon.cn/gp/associates/network/main.html']
    start_urls = ['https://associates.amazon.cn/gp/associates/network/reports/report.html']
    def __init__(self, username, password, *a,  **kwargs):
        super(AmazonSpider, self).__init__(*a, **kwargs)
        self.http_user = username
        self.http_pass = password
        #login form
        self.formdata = {'create':'0', \
                         'email':self.http_user, \
                         'password':self.http_pass, \
                         }
        self.headers = {'ccept-Charset':'GBK,utf-8;q=0.7,*;q=0.3', \
                        'Accept-Encoding':'gzip,deflate,sdch', \
                        'Accept-Language':'zh-CN,zh;q=0.8', \
                        'Cache-Control':'max-age=0', \
                        'Connection':'keep-alive', \
                        }
        self.id = 0

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              #formdata = self.formdata,\
                              headers = self.headers, \
                              callback = self.login)#jump to login page

    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))
    def login(self, response):
        self._log_page(response, 'amazon_login.html')
        return [FormRequest.from_response(response, \
                                          formdata = self.formdata, \
                                          headers = self.headers, \
                                          meta = {'cookiejar':response.meta['cookiejar']}, \
                                          callback = self.parse_item)]#success login

    def parse_item(self, response):
        self._log_page(response, 'after_login.html')
        hxs = HtmlXPathSelector(response)
        report_urls = hxs.select('//div[@id="menuh"]/ul/li[4]/div//a/@href').extract()
        for report_url in report_urls:
            #print "list:"+report_url
            yield Request(self._ab_path(response, report_url), \
                          headers = self.headers, \
                          meta = {'cookiejar':response.meta['cookiejar'], \
                                  }, \
                          callback = self.parse_report)

    def parse_report(self, response):
        self.id +=1
        self._log_page(response, "%d.html" %self.id)