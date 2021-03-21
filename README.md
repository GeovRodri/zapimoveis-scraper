# Zap Imoveis Scraper

zapimoveis-scraper is a Python package that works as a crawler and scraper using beautifulsoup4 to get data from [zap imóveis](https://zapimoveis.com.br).


### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install zapimoveis-scraper.
```bash
    pip install zapimoveis_scraper
```

### Usage 

```python
import zapimoveis_scraper as zap

# returns a list with objects containing scraped data
zap.search(localization="go+goiania++setor-oeste", num_pages=5) 
```

#### Available search parameters:
* localization (string): location in which the search will be performed
  * default: 'go+goiania++setor-marista'
  * The search string is available on the search url of zap imóveis. Eg: https://www.zapimoveis.com.br/aluguel/imoveis/rj+rio-de-janeiro+ilha-do-governador+cacuia/
* num\_pages (int): Number of pages to scrape
  * default: 1
* acao (string): type of contract. Possible values: 'venda', 'aluguel', 'lancamentos'
  * default: 'aluguel'
* tipo (string): type of property. Possible values: 'imoveis', 'apartamentos', 'casas'
  * default: 'casas'
* dictionaty\_out (boolean): Specifies the method output (list of objects or dictionary)
  * default: False

#### Scraped attributes:
The objects returned from `search` contain the following attributes:
* description: property description
* price: property price (monthly)
* bedrooms: number of bedrooms on property
* bathrooms: number of bathrooms on property
* total\_area\_m2: property area (square meters)
* vacancies: parking spots available on property
* address: property address
* link: link of the property