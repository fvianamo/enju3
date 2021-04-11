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
		raise NotImplemented('TODO')


if __name__ == '__main__':
	logging.basicConfig( format='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	scrapper = AdvfnScrapper('https://br.advfn.com')
	news_url = scrapper.fetch_news('ENJU3')
	print(news_url)