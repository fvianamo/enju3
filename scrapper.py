import logging
import requests

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseScrapper(ABC):
	"""
	Classe base para a implementação de um scrapper
	"""

	def __init__(self, _url):
		"""
		Contrutor da classe
		Params:
			- url: endereço da portal onde o scrapper irá realizar o processo de scrapping

		"""
		logging.debug(f'Instanciating scrapper for url {_url}')
		response = requests.get(_url)
		if response.status_code == 200:
			logging.debug(f'Source checked, looking good')
			self.url = _url
		else:
			logging.error(f'This url could not be reached')
			raise Exception(f'Portal {_url} não consegue ser acessado')
		pass

	@abstractmethod
	def fetch_news(self, ticker):
		"""
		Realiza a busca por notícias na seção do portal
		retornando a lista de notícias a serem consultadas
		"""
		pass

	@abstractmethod
	def parse_news(self, news_url):
		"""
		Dado o endereço da notícia, realiza-se o parser da página retornando dict com as informações da notícia
		Params:
			- news_url: endereço da notícia
		"""
		pass


class AdvfnScrapper(BaseScrapper):
	"""
	Implementa o scrapper para a página https://br.advfn.com
	"""
	def __init__(self, _url):
		super().__init__(_url)


	def fetch_news(self, ticker):
		# redirecionando para a página da ação
		search_path = f'{self.url}/p.php?pid=qkquote&symbol=BOV%5E{ticker.upper()}'
		logging.info(f'searching for Ticker page on {search_path}')
		search_response = requests.get(search_path)
		
		assert search_response.status_code == 200
		
		# buscando urls na tabela de notícias
		ticker_page = BeautifulSoup(search_response.text, 'html.parser')
		news_table = ticker_page.find(id='id_news')
		news = news_table.find_all('a')
		news = [f"https:{new['href']}" for new in news]

		logging.info(f'found {len(news)} on {self.url} for ticker {ticker}')

		return news


	def parse_news(self, news_url):
		logging.info(f'requesting news on {news_url}')
		news_response = requests.get(news_url)
		news_page = BeautifulSoup(news_response.text, 'html.parser')
		
		news_title = news_page.h1.get_text()
		news_category = news_page.find('span', {'class': 'cat-title'}).get_text()
		news_source = news_page.find('span', {'class': 'posted-by'}).a.get_text()
		news_dt = news_page.find('span', {'class': 'posted-on'}).time['datetime']
		news_content_str = news_page.find('div', {'class': 'post-content post-dymamic'}).get_text()
		news_content_html = str(news_page.find('div', {'class': 'post-content post-dymamic'}))
		
		return dict(title = news_title,
					category = news_category,
					source = news_source,
					posted_on = news_dt,
					content_str = news_content_str,
					content_html = news_content_html)


if __name__ == '__main__':
	logging.basicConfig( format='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	scrapper = AdvfnScrapper('https://br.advfn.com')
	news_url = scrapper.fetch_news('ENJU3')
	
	news = scrapper.parse_news(news_url[0])

	print(news)