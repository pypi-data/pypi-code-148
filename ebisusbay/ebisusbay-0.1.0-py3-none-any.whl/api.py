#!/usr/bin/python
# coding: utf8

import requests

class Api:
    def __init__(self):
        self.url = 'https://api.ebisusbay.com'

    def get(self, request_url, params = {}):
        res = requests.get(self.url + request_url, params).json()
        if res['status'] != 200:
            raise Exception(f"Error {res['status']} : {res['error']}")

        return res

    #####################################
    #                                   #
    #             Request               #
    #                                   #
    #####################################
    def get_all_collections(self, params: dict = {}) -> list:
        res = self.get('/collections', params)
        collections = res['collections']
        
        if res['page'] < res['totalPages']:
            params['page'] = res['page'] + 1
            collections += self.get_all_collections(params)

        return collections
    
    def get_collections(self, params: dict = {}) -> list:
        return self.get('/collections', params)['collections']

    def get_full_collection(self, collection_address: str, params: dict = {}) -> dict:
        params['address'] = collection_address

        return self.get('/fullcollections', params)['nfts']
        

    def get_listings(self, params: dict = {}) -> list:
        return self.get('/listings', params)['listings']

    def get_nft(self, collection_address: str, token_id: str) -> dict:
        params = {
            'collection': collection_address,
            'tokenId'  : token_id
        }
        res = self.get('/nft', params)
        res.pop('status')
        res.pop('error')

        return res

    def get_wallet(self, wallet_address: str, params:dict = {}) -> dict:
        params['wallet'] = wallet_address

        return self.get('/wallets', params)['data']
