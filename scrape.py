from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


URL = 'http://www.mysuwanneeriver.org/realtime/river-levels.php'

print('++++++++++++++++++++')

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def get_headers(soup):
    """ Get table headers; accepts soup obj returns list of headers. """
    table_headers = []
    for header in soup.find_all('th'):
        table_headers.append(header.get_text())
    return table_headers

print('Accessing website...')
print(URL)

raw_html = simple_get(URL)

data = []
soup = BeautifulSoup(raw_html, 'html.parser')

table = soup.find('table')
for row in table.findAll("tr"):
    cells = row.findAll("td")
    cells = [ele.text.strip() for ele in cells]
    data.append([ele for ele in cells if ele])

print('--------- DATA ---------')
print('# of entries found: ', len(data))
print('Table headers: ', get_headers(soup))

print('///////// Branford /////////')
for entry in data:
    if len(entry):
        if entry[0] == 'Branford':
            print(entry)
