import requests, time

from bs4 import BeautifulSoup

myHeader = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72'}

response = requests.get("https://www.bestbuy.com/site/sony-playstation-5-console/6523167.p?skuId=6523167", headers=myHeader)

Soup = BeautifulSoup(response.content, 'html.parser')

cart_button = Soup.find("button", class_="add-to-cart-button")

#print(Soup.find("button", class_="add-to-cart-button"))

print(cart_button.text) #Finds the text associated with the add-to-cart button

#Checks if the text on the button is "Sold Out".
while 2 > 1:

    if 'Sold Out' != cart_button.text:
        print("The PS5 is in stock!!!!!!!!!!!!!")
    else:
        print("The PS5 is NOT in stock")
    time.sleep(2) #Checks the page every 2 seconds
