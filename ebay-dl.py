# importing things
import argparse 
import requests
from bs4 import BeautifulSoup
import json
import csv

# any functions wanted/needed
def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string

    >>> parse_itemssold('59 sold')
    59
    >>> parse_itemssold('Last one')
    0
    >>> parse_itemssold('25 watchers')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else: 
        return 0

def parse_price(text):
    '''
    >>> parse_price('$15.95')
    1595
    >>> parse_price('$4.79 to $8.99')
    479
    >>> parse_price('free shipping')
    0
    '''
    numbers = ''
    price_text = ''
    dollar_index = text.find('$')
    space_index = text.find(' ')
    if "$" not in text:
        return 0
    if space_index != -1:
        price_text = text[dollar_index : space_index]
    else: 
        price_text = text[dollar_index:]
    for char in price_text:
        if char in '1234567890':
            numbers += char
    return int(numbers)


# this if statement says only run the code below when the python file is run "normally"
if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term') #arguments need to have quotations to include spaces
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print('args.search_term=', args.search_term)


    items = [] #list of all items found in all ebay webpages

    #loop over the ebay webpages
    for page_number in range(1, int(args.num_pages)+1):

        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url', url)
        
        # download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text

        # process the html

        soup = BeautifulSoup(html, 'html.parser')

        #loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            # extract the name
            tags_name = tag_item.select('.s-item__title')
            name = None
            for tag in tags_name:
                name = tag.text

            # extract the free_returns
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            # extract the items_sold
            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            # extract price
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            # extract shipping
            shipping = 0
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_price(tag.text)

            # extract the status
            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text
            
            # create item dictionary for items list
            item = {
                'name' : name,
                'free_returns' : freereturns,
                'items_sold' : items_sold,
                'status' : status,
                'price' : price,
                'shipping' : shipping
                }

            items.append(item)

        print('len(tag_items)=', len(tags_items))
        print('len(items)', len(items))

    if not args.csv:
        # write the json to a file
        filename = args.search_term+'.json'
        with open(filename, 'w', encoding='ascii') as f:
            f.write(json.dumps(items))
    else:
        filename = args.search_term+'.csv'
        with open(filename, 'w', encoding= 'UTF-8') as f:
            for item in items:
                writer = csv.writer(f)
                name = item['name']
                freereturns = item['free_returns']
                items_sold = item['items_sold']
                status = item['status']
                price = item['price']
                shipping = item['shipping']
                writer.writerow([name, freereturns, items_sold, status, price, shipping])
        f.close()

