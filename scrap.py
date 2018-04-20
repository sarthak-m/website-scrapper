# import libraries
import urllib.request as request
from bs4 import BeautifulSoup as bs
import ssl
import csv
from datetime import datetime

# for SSL Certificate work around
context = ssl._create_unverified_context()

# headers
hdr = {'User-Agent':'Mozilla/5.0'}

with open('links.csv', newline='') as csvfile:
	links = csv.reader(csvfile, delimiter='\n')

	for link in links:
		
		# specify the url
		# product_pages = ['test_url_for_one_product']

		# request variable
		req = request.Request(link[0],headers=hdr)

		# load URL
		page = request.urlopen(req, context=context)

		# parse the content as HTML format
		soup = bs(page, 'lxml')

		name = soup.find('h1', attrs={'id': 'name'}).text.strip()
        # pricing = soup.find('section', attrs={'id': 'product-price'})
		# retail_price = soup.find('section', attrs={'id':'product-msrp'})

		price = "n/a"
		if soup.find('div', attrs={'id': 'price'}):
			price = soup.find('div', attrs={'id': 'price'}).text.strip()
		product_spec_list = soup.find('ul', attrs={'id': 'product-specs-list'}).findAll('li')

		expiration_date = "n/a"
		if soup.find('div', attrs={'id': 'expiration-message-link'}):
			for tag in soup.find('div', attrs = {'id': 'expiration-message-link'}).next_siblings:
				if soup.find("div") == True:
					exit()
				else:
					expiration_date += str(tag)
					break

		expiration_date = expiration_date.strip()
		upc_code = soup.find('span', attrs={'itemprop': 'gtin12'}).text.strip()
		description = "n/a"
		if soup.find('div', attrs={'itemprop': 'description'}):
			description = soup.find('div', attrs={'itemprop': 'description'}).text.strip()

		rating = "n/a"
		if soup.find('span', attrs={'class': 'rating-average'}):
			rating = soup.find('span', attrs={'class': 'rating-average'}).text.strip()
		
		# open a csv file with append, so old data will not be erased
		with open('data.csv', 'a') as csv_file:
		 writer = csv.writer(csv_file)
		 writer.writerow([name, price, rating, upc_code, description, expiration_date, datetime.now()])

print('data saved')
