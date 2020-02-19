import os
from flask import Flask, flash, redirect, render_template, request, json
import urllib.request
from jinja2 import ext
from datetime import datetime

 
app = Flask(__name__)

# ná í petrol á apis.is
with urllib.request.urlopen("https://apis.is/petrol") as url:
    gogn = json.loads(url.read().decode())

app.jinja_env.add_extension(ext.do)


# ná í tímatal síðasta uppfærsla
def format_time(gogn):
    return datetime.strptime(gogn, '%Y-%m-%dT%H%:M:%S.%f').strftime('%d. %m. %Y. Kl. %H:%M')

app.jinja_env.filters['format_time'] = format_time #filter skilgreindur



#besta verðið
def minPetrol():
    minPetrolPrice = 1000
    company = None
    address = None
    lsti = gogn['results']

    for i in lsti: #loop í gegnum alla datasettið
        if i['bensin95'] is not None:
            if i['bensin95'] < minPetrolPrice:
                minPetrolPrice = i['bensin95']
                company = i['company']
                address = i['name']
    return [ minPetrolPrice, company, address] #lægsta verð í lista


#öll fyrirtæki x1
@app.route('/')
def home():
    return render_template('index.html', gogn=gogn, MinP=minPetrol())

#eitt fyrirtæki - allar stöðvar
@app.route('/company/<company>')
def comp(company):
    return render_template('company.html', gogn=gogn, com=company)


#bensínstöð fyrirtækis
@app.route('/moreinfo/<key>')
def info(key):
    return render_template('moreinfo', gogn=gogn, k=key)

#villuskilaborð
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'), 404

if __name__== '__main__':
    app.run(debug=True)