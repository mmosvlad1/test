import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
money = []


with open('addresses.txt', 'r') as file_loc:
    addresses = file_loc.readlines()



for addres in addresses:
    url = f"https://etherscan.io/address/{addres[:-1]}"

    driver_service = Service('chromedriver_mac_arm64/chromedriver')
    driver = webdriver.Chrome(service=driver_service)
    driver.get(url)

    driver.implicitly_wait(50)
    time.sleep(0.4)
    response_after_search = driver.page_source

    driver.quit()

    soup_after_search = BeautifulSoup(response_after_search, 'html.parser')
    info_div = soup_after_search.find_all('h4', {'class': 'text-cap mb-1'})
    value = info_div[1].parent
    value = str(value)

    numb = 50
    money_count = []
    while value[numb:]:
        if (value[numb] == '.'):
            break

        money_count.append(value[numb])
        numb += 1

    money.append("".join(money_count))
    driver.quit()

with open('money.txt', 'w') as file_loc:
    file_loc.writelines("\n".join(money))
