#!/usr/local/bin/python3
import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
from bs4 import BeautifulSoup


FLASK_HOST = '0.0.0.0'
FLASK_PORT = 80

URL_HASHICORP_RELEASES = 'https://releases.hashicorp.com'
ENTERPRISE_PRODUCTS = ['consul', 'nomad', 'nomad-autoscaler', 'vault']


def getProducts(url, product=None, version=None, latest=False, ent=False):
    items = []
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    for item in soup.find_all('a', href=True):
        text = item.get_text()
        if text != 'Fastly' and text != '../':
            if product and not version:
                text = text.replace('{}_'.format(product), '')
            items.append(text)

    if version:
        array = []
        for item in items:
            array.append({'name': item, 'url': '{}/{}/{}/{}'.format(URL_HASHICORP_RELEASES, product, version, item)})
        items = array

    if latest and product in ENTERPRISE_PRODUCTS:
        if not ent:
            items = [x for x in items if 'ent' not in x and 'beta' not in x and 'rc' not in x][0]
        if ent:
            items = [x for x in items if 'ent' in x and 'beta' not in x and 'rc' not in x][0]
    elif latest and not product in ENTERPRISE_PRODUCTS:
        items = items[0]

    if len(items) == 0:
        return({'message': 'Product \'{}\' has not been found. Check \'{}\' page.'.format(product, URL_HASHICORP_RELEASES)}), 404

    return jsonify(items), 200


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'message': f'path \'{path}\' not found'}), 404


@app.route('/')
def allProducts():
    return getProducts(URL_HASHICORP_RELEASES)


@app.route('/<product>/')
@app.route('/<product>/<version>/')
@app.route('/<product>/latest/')
@app.route('/<product>/latest/ent')
def productDetails(product, version=None, latest=False, ent=False):
    url = URL_HASHICORP_RELEASES + '/' + product
    if version:
        url += '/' + version
    if '{}/latest'.format(product) in request.url:
        latest = True
    if '{}/latest/ent'.format(product) in request.url:
        ent = True
    return getProducts(url, product, version, latest, ent)


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
