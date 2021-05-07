import requests
from bs4 import BeautifulSoup
from csv import writer

response = requests.get('https://baseballmonster.com/boxscores.aspx')

soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all(class_='w3-hoverable')
for post in posts:
    name = post.find_all('tr')
    for n in name:
        print(n.get_text())


# html_doc = """
# <!doctype html>
# <html>
# <head>
#     <title>My First Webpage</title>
#     <meta charset="utf-8" />
#     <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1" />
# </head>
# <body>
# <div id='section-1'>
#     <h1>This is a huge header</h1>
#     <h2>This one's a little smaller</h2>
#     <h3>And smaller still...</h3>
#     <h4>And so on</h4>
#     <h5>And on</h5>
#     <h6>Do you really want to go smaller than this??</h6>
#     <p>My first line goes here.<br/>Extra text!!</p>
#     <hr/>
#     <p>A second line goes here.</p>
#     <p><strong>This is a bold piece of text.</strong>  This word will be in <em>italics</em>. I want this <u>word</u> to be underlined.  <strike>This line is wrong.</strike></p>
#     <h2>My favorite foods</h2>
#     <ul>
#       <li>Pizza</li>
#       <li>Chocolate</li>
#       <li>Curry</li>
#     </ul>
#     <h2>My favorite times of day</h2>
#     <ol>
#       <li>Morning</li>
#       <li>Bed time</li>
#       <li>Dinner time</li>
#     </ol>
#     <img src="img/kate.jpg"/ width="100px" height="146px">
#     <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Leonard_Cohen_2008.jpg/100px-Leonard_Cohen_2008.jpg">
#     <table>
#       <tr><th>Names</th><th>Age</th><th>Gender</th></tr>
#       <tr><td>Rob</td><td>33</td><td>Male</td></tr>
#       <tr><td>Kirsten</td><td>34</td><td>Female</td></tr>
#       <tr><td>Tom</td><td>3</td><td>Male</td></tr>
#     </table>
# </div>
# <div>2</div>
# </body>
# </html>
# """
#
# soup = BeautifulSoup(html_doc, 'html.parser')

# Direct
# print(soup.body)
# print(soup.head)
# print(soup.head.title)

# find()
# el = soup.find('div')

# find_all() or findAll()
# el = soup.find_all('div')
# el = soup.find_all('div')[1]

# el =soup.find(id='section-1')
# el =soup.find(class_='items')

# el = soup.find(attrs={"data-hello": "hi"})

# select
# el = soup.select('#section-1')
# el = soup.select('#section-1')[0]
# el = soup.select('.item')[0]

# get_text()
# el = soup.find(class_='item').get_text()

# for item in soup.select('.item'):
#     print(item.get_text())

# Navigation
# el = soup.body.contents[1].contents[1].next_sibling.next_sibling
# el = soup.body.contents[1].contents[1].find_next_sibling()
# el = soup.find(id='section-2').find_previous_sibling()
# el = soup.find(class_='item').find_parent()
# el = soup.find('h3').find_next_sibling('p')
#
# print(el)



import pandas as pd
import utils
import io

BASE_URL = 'http://rotoguru1.com/cgi-bin/fyday.pl?game=dk&csv=1&week=WEEK&year=YEAR'
WEEKS=list(map(str,range(1,18)))
YEARS=list(map(str,range(2014,2017)))

all_games=pd.DataFrame()
for yr in YEARS:
    for wk in WEEKS:
        soup=utils.soup(BASE_URL.replace("WEEK", wk).replace("YEAR",yr))
        all_games=pd.concat([all_games,pd.read_csv(io.STRINGIO(soup.find('pre').text),sep=';')])
all_games