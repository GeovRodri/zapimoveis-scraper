#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2016, Geovany Rodrigues
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

from zapimoveis_scraper.enums import ZapAcao, ZapTipo
from zapimoveis_scraper.item import ZapItem
from collections import defaultdict

__all__ = [
    # Main search function.
    'search',
]


# URL templates to make urls searches.
url_home = "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/?pagina=%(page)s"

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    return response


def __get_text(element, content=False):
    text = ''
    if element is not None:
        if content is False:
            text = element.getText()
        else:
            text = element.get("content")

    text.replace('\\n', '')
    return text.strip()

def convert_dict(data):
    '''
    Simple function to convert the data from objects to a dictionary

    dicts: Empty default dictionary
    Keys: List with the keys for the dictionary
    '''
    #start dictonary 
    dicts = defaultdict(list)
    #create a list with the keys
    keys = ['price','bedrooms','bathrooms','vacancies','total_area_m2','address','description', 'link']
    
    #simple for loops to create the dictionary
    for i in keys:
        for j in range(len(data)):
            to_dict = data[j].__dict__
            dicts[i].append(to_dict['%s' % i])
            
    return dicts


def get_listings(soup):
    page_data_string = soup.find(lambda tag:tag.name=="script" and isinstance(tag.string, str) and tag.string.startswith("window"))

    json_string = page_data_string.string.replace("window.__INITIAL_STATE__=","").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());","")

    return json.loads(json_string)['results']['listings']


def get_ZapItem(listing):
    item = ZapItem()
    item.link = listing['link']['href']
    item.price = listing['listing']['pricingInfos'][0]['price']
    item.bedrooms = listing['listing']['bedrooms'][0] if len(listing['listing']['bedrooms']) > 0 else 0
    item.bathrooms = listing['listing']['bathrooms'][0] if len(listing['listing']['bathrooms']) > 0 else 0
    item.vacancies =  listing['listing']['parkingSpaces'][0] if len(listing['listing']['parkingSpaces']) > 0 else 0
    item.total_area_m2 = listing['listing']['usableAreas'][0] if len(listing['listing']['usableAreas']) > 0 else 0
    item.address = (listing['link']['data']['street'] + ", " + listing['link']['data']['neighborhood']).strip(',').strip()
    item.description = listing['listing']['title']

    return item


def search(localization='go+goiania++setor-marista', num_pages=1, acao=ZapAcao.aluguel.value, tipo=ZapTipo.casas.value, dictionary_out = False):
    page = 1
    items = []

    while page <= num_pages:
        html = get_page(url_home % vars())
        soup = BeautifulSoup(html, 'html.parser')

        listings = get_listings(soup)

        for listing in listings:
            if 'type' not in listing or listing['type'] != 'nearby':
                items.append(get_ZapItem(listing))

        page += 1

    if dictionary_out:
        return convert_dict(items)

    return items
