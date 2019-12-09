import os
import argparse
import csv
import requests

NAME='download_att'
DONWLOAD='output/pdf'

def files2open(filename, _encoding='ISO-8859-1'):
    type=filename.split('.')[len(filename.split('.'))-1]
    if type in ['csv']:
        doc=  csv.DictReader(open(filename, mode='r'))
    else :
        f = open(filename, 'r', encoding=_encoding)
        doc = f.read()
        f.close()
    return doc, type


parser = argparse.ArgumentParser(
        prog=NAME,
        usage="python %(prog)s [options]",
        description='Another dorking tool. This is only a proof of concept to develop an a right tool. Just a hobby',
        epilog='never mind the bollocks, if you don\'t like this, forget this. comments>/dev/null'
    )


parser.add_argument('--verbose', "-v", action='store_true', help='Verbose')
parser.add_argument('--file', '-f', type=str, help='File with data')


args = parser.parse_args()
type = ''
if args.file:
    if os.path.exists(args.file):
        doc, type = files2open(args.file)
    else:
        print ('File {0} not found'.format(args.file))
        exit(-1)
    if type == 'csv':
        for i in doc:
            print ("URL:{0}".format(i['link']))
            filename=i['link'].split('/')[len(i['link'].split('/'))-1]
            try:
                type=filename.split('.')[len(filename.split('.'))-1]
            except:
                type=filename
            print("[{0}]->({1})".format(filename,type))
            if type in ['pdf']:
                if not os.path.exists(DONWLOAD):
                    os.mkdir(DONWLOAD)
                aux=DONWLOAD+"/"+filename
                if not os.path.exists(AUX):
                    ua = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
                    response = requests.get(i['link'], headers=ua)
                    open(aux, 'wb').write(response.content)
