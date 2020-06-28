from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'http://127.0.0.1:5000/'
response = requests.get(main_link)

soup = bs(response.text,'lxml')

# link = soup.find_all('a')

# link = soup.find('a')
# pprint(link)

# div = link.parent.parent
#
#
# children = div.findChildren(recursive=False)
# pprint(children)

# div2 = soup.find(attrs={'id':'clickable'})
# pprint(div2)

# p = soup.find_all('p',{'class':'red paragraph'})
# pprint(p)

# p = soup.find_all('p',limit=3)
# pprint(p)
#
# text = soup.find(text='Шестой параграф')
# print(text.parent)

p = soup.find_all('p')
pprint(p[-3:])

# link = soup.find('a')
# pprint(link.getText())
# pprint(link['href'])




