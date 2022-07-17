import requests
from bs4 import BeautifulSoup
import concurrent.futures


file = open("./items.txt", "w", encoding="utf-8")


maxPageCount = 25
itemCounter = 1

# Function used to get the title and the description from an item
# itemLinkHref represents the url that is taken from the item title in the listings page
def get_title_and_description(itemLink):
  itemLinkHref = itemLink["href"]
  if itemLinkHref:
    # The page is parsed using lxml and BeautifulSoup
    newPage = BeautifulSoup(requests.get(itemLinkHref).content, "lxml");
    # We get the title by finding the strong attribute, the result returned being <strong>title</strong>
    # We get rid of the opening and closing tags by slicing
    itemTitle = str(itemLink.find("strong"))[8:-9]
    # Get the item description using the css path ( Mozilla Firefox ). The item returned is [<div class="css-g5mtbi-Text">description</div>]
    # Sometimes, there are <br> tags in the description, thus we replace them with nothing
    itemDescription = str(newPage.select("html body div#root div.css-50cyfj div.css-1on7yx1 div.css-1d90tha div.css-dwud4b div.css-1wws9er div.css-1m8mzwg div.css-g5mtbi-Text")).replace('<br/>', '')[30:-7]
    # Get the item price from the listing using the css path ( Mozilla Firefox ). The item returned is [<h3 class="css-okktvh-Text eu5v0x0">price<!-- --> <!-- -->lei</h3>]
    # We get rid of the starting and ending tags, leaving us with the price. We also get rid of the space ( ex: 7 000 becomes 7000 )
    itemPrice = str(newPage.select("html body div#root div.css-50cyfj div.css-1on7yx1 div.css-1d90tha div.css-dwud4b div.css-1wws9er div.css-dcwlyx h3.css-okktvh-Text.eu5v0x0"))[37:-26].replace(' ', '')
    # The string that is written in the file. Will be used with regex
    stringToWrite =  itemTitle + '\n' + itemDescription + '\n' + itemPrice + " lei\n"
    return stringToWrite
  else:
    return 0

def get_page(page):
  global itemCounter
  # Get the page using BeautifulSoup and lxml parsing
  soup = BeautifulSoup(requests.get(page).content, "lxml")
  # On OLX, the title of all listings represents the link to the item itself. Thus, we get all the links to the items
  # using this method.
  itemsLink = soup.find_all("a", class_="marginright5 link linkWithHash detailsLink", href = True)
  # We create a pool of threads that will call the method with an item from itemsLink as parameter
  # All threads begin at the same time and the results are stored when all of them are finished
  results = concurrent.futures.ThreadPoolExecutor().map(get_title_and_description, itemsLink)
  for result in results:
    try:
      file.write(result)
      itemCounter += 1
    except:
      # If there is an exception, continue execution ( probably site parsing error )
      continue

# Using the same principle as before, we take all the pages and call the get_page function with a page as parameter
# As a result of all the multithreading, if we have 5 pages, all 5 pages will be verified at the same time and all the
# listings on all of those pages will get parsed at the same time, saving execution time
with concurrent.futures.ThreadPoolExecutor() as executor:
  pages = []
  for count in range(1, maxPageCount + 1):
    pages.append(f"https://www.olx.ro/mama-si-copilul/?page={count}")
    

  pageResults = executor.map(get_page, pages)