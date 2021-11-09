# HW03: ebay.dl/E-Bay Scraping
[HW03 for CSCI40 at CMC](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)

### What The ebay.dl File Does
The ebay.dl python file...
- Creates a url from whatever `search_term` argument you enter within the command line
- Downloads the first ten pages of results for your `search_term`
- Extracts individual items from these pages
- Creates a list of dictionaries, each dictionary containing information from the items

### How to Run the ebay.dl File
The generic form of the command to run the ebay.dl file looks like this:

    python3 ebay.dl 'search_term'
    
If you would like to only receive one webpage that your `search_term` argument has, you can modify that command using the `num_pages` argument. For page x, that would look something like this.

    python3 ebay.dl 'search_term' --num_pages=x
    
    
**The command lines to receive my specific json files look like this:**

For heelys.json:

    python3 ebay.dl 'heelys'
    
For converse.json:

    python3 ebay.dl 'converse'
    
For high heels.json:

    python3 ebay.dl 'high heels'
    
### Extra Bonus Round: Creating CSV files instead of json files
Use the same generic forms of command to run your ebay.dl file:

    python3 ebay.dl 'search_term'

But, to receive a CSV file instead of a json file, I have added an argument `csv`. Add `--csv` to the end of this command line, which looks like this:

    python3 ebay.dl 'search_term' --csv
    
**The command lines to receive my specific CSV files look like this:**

For heelys.csv:

    python3 ebay.dl 'heelys' --csv
    
For converse.csv:

    python3 ebay.dl 'converse' --csv
    
For high heels.csv:

    python3 ebay.dl 'high heels' --csv
    
    
