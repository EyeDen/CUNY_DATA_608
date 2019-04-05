#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:19:18 2019

@author: idenwatanabe
"""

from flask import Flask, jsonify
import json, requests

app = Flask(__name__)


# Much like last assignment, this GET fetches boro data
# regarding tree type, count, health, and whether it has a steward

@app.route('/tree/<string:boro>')
def return_tree_data(boro):
    url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
           '$select=spc_common,count(tree_id),health,steward,boroname' +\
           '&$where=boroname=\'' + boro + '\'' +\
           '&$group=spc_common,health,steward,boroname').replace(' ', '%20')
    response = requests.get(url)
    return jsonify(response.json())
    
if __name__ == '__main__':
    app.run(debug = True)