from flask import Flask, request
import os
import requests
import logging

app = Flask(__name__)

def config(key):
    '''
    Stores the configuration variables in one hashmap
    '''
    config_store = {
        'nytimes_api_key': os.environ['NYTIMES_API_KEY'],
        'nytimes_base_url': 'https://api.nytimes.com/svc/books/v3',
        'proxies': {
            'http': 'http://localhost:8081',
            'https': 'http://localhost:8081',
        }
    }
    return config_store[key]

@app.route('/nytimes/books/bestsellers.json')
def list_bestseller():
    '''
    Retuns json containing nytimes bestsellers books
    '''    
    payload = {
        'api-key': config('nytimes_api_key')
        }
    url = "{}/lists/names.json".format(config('nytimes_base_url'))
    return requests.get(url=url, params=payload, proxies=config('proxies')).json()

@app.route('/nytimes/books/<path:path>', methods=['GET'])
def nytimes_wrapper(path):
    '''
    Wrapper on top of nytimes APIs.
    Most of API can be hit listed on https://developer.nytimes.com/docs/books-product/1/overview
    example: 
    `/nytimes/books/lists/current/hardcover-fiction.json` will call `/lists/current/hardcover-fiction.json` of nytimes API
    '''
    payload = {
        'api-key': config('nytimes_api_key')
        }
    payload.update(request.args.to_dict())
    url = "{}/{}".format(config('nytimes_base_url'), path)
    # Prints api_key also, security vulnerability (Can be easily fixed by replacing payload with args)
    app.logger.info("calling API '%s' with arguements: '%s'", url, payload)
    return requests.get(url=url, params=payload, proxies=config('proxies')).json()

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run()