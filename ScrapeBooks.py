import requests
from bs4 import BeautifulSoup
import pandas as pd

def extractBookParticulars(bookurl):
    response = requests.get(bookurl)
    if response.status_code==200:
        soupObject = BeautifulSoup(response.text, 'html.parser')
        productname = soupObject.find('li',{'class':'active'}).text
        productdescription = soupObject.find('meta',{'name':'description'}).get("content")
        productinformation = soupObject.find('table',{'class': 'table-striped'})
        productupc = productinformation.find(string="UPC").find_next('td').string
        producttype = productinformation.find(string="Product Type").find_next('td').string
        productprice = productinformation.find(string="Price (incl. tax)").find_next('td').string
        productavailability = productinformation.find(string="Availability").find_next('td').string
        productreviews = productinformation.find(string="Number of reviews").find_next('td').string
        thebook = {'Name':productname, 'Price':productprice, 'UPC':productupc, 'Description':productdescription, 'Availability':productavailability, 'Reviews':productreviews}   
        return(thebook)
        
url = 'https://books.toscrape.com/catalogue/page-' #1.html'
df  =  pd.DataFrame(columns=['Name', 'Price', 'UPC', 'Description', 'Availability', 'Reviews'])
for i in range (1, 5):
    urlmod = url + str(i) + '.html'
    response = requests.get(urlmod)
    print(f'Page {i} response code {response.status_code}')
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all('li',{'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    print(f'Total books in the page {len(books)}')
    partial_url = 'https://books.toscrape.com/catalogue/'
    for book in books:
        book_name = book.h3.a['title']
        book_url = book.h3.a['href']
        full_book_url = partial_url + book_url
        bookdictionary = extractBookParticulars(full_book_url)            
        df.loc[len(df)] = bookdictionary
print(df.head(5))
df.to_csv("BookBrochure.csv")
        
