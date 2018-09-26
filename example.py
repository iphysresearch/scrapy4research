import scrapy

class Example(scrapy.Spider):
	name = "arxiv"
	start_urls = {
		'https://arxiv.org/list/gr-qc/new'
	}

	def parse(self, response):

		for item in response.xpath('.//span[@class="list-identifier"]'):
			url = response.urljoin(item.xpath('a[@title="Abstract"]/@href').extract_first())

			yield scrapy.Request(url, callback = self.parse_info)
	def parse_info(self, response):
		id = response.xpath('.//div[@id="header"]/h1/text()').extract()
		PDF_url = response.urljoin(response.xpath('.//div[@class="full-text"]/ul/li[1]/a/@href').extract_first())
		title = response.xpath('.//h1[@class="title mathjax"]/text()').extract_first()
		authors = response.xpath('.//div[@class="authors"]/a/text()').extract()
		dateline = response.xpath('.//div[@class="dateline"]/text()').extract_first()
		abstract = response.xpath('.//blockquote[@class="abstract mathjax"]/text()').extract()

		yield{
			'id': id[1].split('>')[1].split(':')[1].strip(),
			'PDF_url': PDF_url,
			'title': title,
			'authors': authors,
			'dateline': dateline,
			'abstract': abstract[1]
		}