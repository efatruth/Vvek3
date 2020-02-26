
import os
from flask import Flask, render_template, json
import urllib.request
from jinja2 import ext
from datetime import datetime

app = Flask(__name__)

# bensínstöðvar
with urllib.request.urlopen("https://apis.is/petrol/") as url:
    gogn = json.loads(url.read().decode())

def format_time(gogn):
    return datetime.strptime(gogn, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d. %m. %Y Kl. %H:%M') # tímaform endurraðað 

app.jinja_env.add_extension(ext.do)

app.jinja_env.filters['format_time'] = format_time   # filter sem búinn er til í appinu fyrir index.tpl

""" Lægsta verðið """

def minPetrol():
    minPetrolPrice = 1000 # vonum að lítraverð fari ekki yfri 1000 kr, annars þarf að breyta þessum gaur.
    company = None
    address = None
    lst = gogn['results']
    for i in lst: # lúppum í gegnum allt datasettið
        if i['bensin95'] is not None: # Hreinsum í burt "null"
            if i['bensin95'] < minPetrolPrice:
                minPetrolPrice = i['bensin95']
                company = i['company']
                address = i['name']
    return [minPetrolPrice, company, address]  # skila lista af lægsta verði, fyrirtæki og heimilisfangi

def minDiesel():
    minDieselPrice = 1000 # vonum að lítraverð fari ekki yfri 1000 kr, annars þarf að breyta þessum gaur.
    company = None
    address = None
    lst = gogn['results']
    for i in lst: # lúppum í gegnum allt datasettið
        if i['diesel'] is not None: # Hreinsum í burt "null"
            if i['diesel'] < minDieselPrice:
                minDieselPrice = i['diesel']
                company = i['company']
                address = i['name']
    return [minDieselPrice, company, address] # skila lista af lægsta verði, fyrirtæki og heimilisfangi

""" forsíðan """
@app.route('/') 
def index():
    return render_template('index.html',gogn=gogn, minP=minPetrol(), minD=minDiesel()) # Sendum niður 2 lista með upplýsingum um ódýrasta bensín (minP) og díesel (minD)

@app.route('/company/<company>')
def comp(company):
    return render_template('company.html',gogn=gogn,com=company)

@app.route('/moreinfo/<key>')
def info(key):
    return render_template('moreinfo.html',gogn=gogn,k=key)

""" gengið """

with urllib.request.urlopen("http://apis.is/currency/") as url:
    data = json.loads(url.read().decode())

@app.route('/gengi')
def currency():
    return render_template('gengi.html', data=data)

# villuskilaboð 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pagenotfound.html'), 404

if __name__ == "__main__":
    app.run(debug=True)