import os, re
import logging
import argparse
import datetime
import configparser
import requests
import urllib
import random
import string
import json
import csv

from bs4 import BeautifulSoup

__author__ = 'mac'
__version__ = '1.0.0'
NAME = 'kingdork'
_GLOBAL_NAME = 'google_search'
_DATETIME = datetime.datetime.now().strftime("%Y%m%d")
configfile = 'conf/config.ini'
_JSON='json'
_CSV='csv'
_SCREEN = 'screen'
google_base = 'https://www.google.com'
google_search = '/search?q='
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


# -----------------------------------------------------------------------------------------------------------------------
class data_found:
    def __init__(self, name=None):
        if not name is None:
            self.NAME = name
        else:
            self.NAME = _GLOBAL_NAME
        self.current = 0
        self.data = {
            'number': 0,
            0: {
                'link': '',
                'title': '',
                'description': '',
                'date': ''
            }
        }
        self.next_page = None

    def _plus(self):
        self.current += 1

    def add_data(self, _link=None, _title=None, _description=None, _date=None):
        self.data[self.current] = {
            'link': _link,
            'title': _title,
            'description': _description,
            'date': _date
        }
        self._plus()

    def show(self, number=False):
        if number is False:
            number = self.last()
        if not number is False:
            return self.data[number]
        else:
            return None

    def last(self):
        if self.current == 0:
            return False
        else:
            return self.current - 1

    def print(self):
        for i in range(0, self.current):
            aux = self.show(i)
            print("Data [{0}]\n\tTitle: {1}\n\tlink: {2}\n\tdescription: {3}\n\tdate: {4}".format(
                i, aux['title'], aux['link'], aux['description'], aux['date']
            ))
        #print("Next page: {0}".format(self.next_page))

    def div_DATA(self, _div):
        link = ''
        title = ''
        description = ''
        date = ''
        content = _div.find_all('div', attrs={'class': 'kCrYT'})
        try:
            # ---- Parte superior
            link = re.sub('^/url\?q=', '', content[0].find('a', href=True)['href']).split('&')[0]
            title = content[0].find('div', attrs={'class': 'BNeawe'}).get_text()
            # ---- Parte inferior
            description = content[1].find('div', attrs={'class': 'BNeawe'}).get_text()
            if content[1].find('span', 'r0bn4c rQMQod'):
                res2 = content[1].find_all('span', 'r0bn4c rQMQod')
                date = res2[0].text
            if link != '' or title != '' or description != '':
                self.add_data(link, title, description, date)
        except:
            pass

    def div_SECTION (self, result):
        return result.find_all('div', attrs={'class': 'ZINbbc'})

    def select_next_page(self, result):
        try :
            self.next_page = result.find('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi BmP5tf'}).a['href']
        except:
            self.next_page = None

    def keys (self):
        return ['link','title', 'description','date']

    def data_found (self):
        _data= []
        for i in range(0, self.current):
            _data.append(self.show(i))
        return _data
# -----------------------------------------------------------------------------------------------------------------------
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))
def string2search(words):
    query = urllib.parse.quote_plus(words)
def config(file=None):
    _configdata = {}
    if file is None:
        file = configfile
    if os.path.exists(file):
        logger.info("Getting data from configuration file {0}".format(file))
        Config = configparser.ConfigParser()
        Config.read(file)
        for i in Config.sections():
            _configdata[i] = dict(Config.items(i))
    else:
        logger.error('File {0} not found'.format(file))
    return _configdata
def options():
    parser = argparse.ArgumentParser(
        prog=NAME,
        usage="python %(prog)s [options]",
        description='Another dorking tool. This is only a proof of concept to develop an a right tool. Just a hobby',
        epilog='never mind the bollock, if you don\'t like this, forget this.\n comments>/dev/null'
    )
    # group_action = parser.add_mutually_exclusive_group()
    # group_credentials = parser.add_argument_group()
    parser.add_argument('--verbose', "-v", action='store_true', help='Verbose')
    #parser.add_argument('--logging', '-log', action='store_true', help='logging activity')
    parser.add_argument('--config', "-c", type=str, help='Config file')
    parser.add_argument('--numpages', "-n", type=int, help='number of pages to manage', default=1)
    parser.add_argument('--dorkfile', "-d", type=str, help='file with expressions')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--json', '-json', action='store_true', help='Save data in json format')
    group.add_argument('--csv', '-csv', action='store_true', help='Save data in CSV format')
    args = parser.parse_args()

    if args.config:
        print ("[{0}]".format(args.config))
        _config = config(args.config)
    else:
        _config = config()
    if args.numpages :
        _config['numpages'] = args.numpages
    else:
        _config['numpages'] = 1
    if args.verbose:
        _config['VERBOSE'] = args.verbose
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        _config['VERBOSE'] = False
    _config['search_string'] = 'test'

    if args.json :
        _config['OUTPUT'] = _JSON
    elif args.csv :
        _config['OUTPUT'] = _CSV
    else:
        _config['OUTPUT'] = _SCREEN


    _url = google_base + google_search + _config['search_string']


    if args.dorkfile and os.path.exists(args.dorkfile):
        _config['dorkfile'] = args.dorkfile
        _url = google_base + google_search
    elif args.dorkfile:
        logger.error('File {0} not found'.format(args.dorkfile))
        exit (0)

    return _config, _url
def dork(_config, _url):

    logger.info('Getting data from URL: {0}'.format(_url))

    ua = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    response = requests.get(_url, ua)
    name = _config['path']['tmp'] + "/{0}_{1}_{2}.html".format(_DATETIME, _config['search_string'], randomString())
    logger.info('Writting data in: {0}'.format(name))
    open(name, 'wb').write(response.content)
    html = BeautifulSoup(response.content, "html.parser")
    cd = data_found()
    cd.select_next_page(html)
    _url = cd.next_page
    if _config['VERBOSE']:
        logger.debug('obtained URL: {0}'.format(_url))
        logger.debug('data saved in file: {0}'.format(name))
    return _url, name
def files2open(filename, _encoding='ISO-8859-1'):
    logger.info('Openning file  {0}'.format(filename))
    f = open(filename, 'r', encoding=_encoding)
    doc = f.read()
    f.close()
    return doc
def showfiles(files):
    cd = data_found()
    for i in files:
        doc =  files2open(i)
        html = BeautifulSoup(doc, "html.parser")
        resultado = cd.div_SECTION(html)
        for i in resultado:
            cd.div_DATA(i)
    manageoutput(_config, cd)
def loop(_config, _url, loop=1):
    cont = 0
    files = []
    if not os.path.exists(_config['path']['tmp']):
        os.mkdir(_config['path']['tmp'])
    while cont < loop:
        logger.info('count : {0}'.format(cont))
        cont += 1
        _aux, _file = dork(_config, _url)
        if _aux is None:
            logger.info('Next page not found.')
        else:
            _url = google_base + _aux
            if _config['VERBOSE']:
                logger.debug('URL returned: {0}'.format(_url))
                logger.debug('filename returned: {0}'.format(_file))
        files.append(_file)
    return files
def deletefiles (files):
    for i in files:
        os.remove(i)
        logger.info('{0} deleted !!!'.format(i))
def manageoutput (_config, _data):
    def filename (_config) :
        _TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return _TIMESTAMP+"_"+_GLOBAL_NAME
    if not 'OUTPUT' in _config:
        if _config['VERBOSE']:
            logger.debug('screen output')
        _data.print()
    else:
        if not os.path.exists(_config['path']['data']):
            os.mkdir(_config['path']['data'])
            logger.info('Outout directory created :{0}'.format(config['path']['data']))
        name = _config['path']['data']+"/"+filename(_config)
        if _config['OUTPUT'] == _JSON:
            name+=".json"
            if _config['VERBOSE']:
                logger.debug('screen output')
            logger.info('Writing data in {0}'.format(name))
            with open(name, 'w', encoding='utf8') as json_file:
                json.dump(_data.data, json_file, ensure_ascii=False)
        elif _config['OUTPUT'] == _CSV:
            name+=".csv"
            logger.info('Writing data in {0}'.format(name))
            if _config['VERBOSE']:
                logger.debug('Keys found:{0}'.format(_data.keys()))
            csv_file = csv.writer(open(name, 'w'))
            csv_file.writerow(_data.keys())
            for row in _data.data_found():
                _csv_data = []
                for key in _data.keys():
                    print ("{}".format(row[key]))
                    _csv_data.append(row[key])
                csv_file.writerow(_csv_data)

if __name__ == "__main__":
    dt = datetime.datetime.now()
    _config, _url = options()
    logger.info('Starting {0} at {1}...'.format(NAME, dt))
    if _config['VERBOSE']:
        logger.debug('config: {0}'.format(_config))
    if 'dorkfile' in  _config:
        doc = files2open (_config['dorkfile'],'utf-8')
        linecount=0
        name=_config['dorkfile'].split("/")[len(_config['dorkfile'].split("/"))-1]
        for i in doc.split('\n'):
            str = i
            _aux = _url + i
            logger.info('URL to check: {0}'.format(_aux))
            _config['search_string']="{0}_line_{1}".format( name,linecount)
            linecount+=1
            files = loop(_config, _aux, _config['numpages'])
        showfiles(files)
        deletefiles(files)
    else:

        files = loop(_config, _url, _config['numpages'])
        showfiles(files)
        deletefiles(files)
    dt = datetime.datetime.now() - dt
    logger.info('Finished. Elapsed time {0}'.format(dt))
