import requests
from flask import Flask,request,jsonify
from requests.api import options
from requests.models import Response
import time
import json
from config import destination,origin



app = Flask(__name__)

def modifyHeaders(request):
    headers=dict(request.headers)
    if(request.get_json()==None ):
        headers.pop('Content-Type') if 'Content-Type' in headers else None
        headers.pop('Content-Length') if 'Content-Length' in headers else None
    
    return headers


def get(request):
    return requests.get('{0}{1}'.format(destination,request.full_path),headers=modifyHeaders(request))

def post(request):
    print(request.get_json())
    return requests.post('{0}{1}'.format(destination,request.full_path),headers=modifyHeaders(request),json=request.get_json())

def put(request):
    print(request.get_json())
    return requests.put('{0}{1}'.format(destination,request.full_path),headers=modifyHeaders(request),json=request.get_json())

def options(request):
    return requests.options('{0}{1}'.format(destination,request.full_path),headers=modifyHeaders(request))

def delete(request):
    print(request.get_json())
    return requests.delete('{0}{1}'.format(destination,request.full_path),headers=modifyHeaders(request),json=request.get_json())

@app.route('/', defaults={'path': ''},methods=['GET', 'POST','PUT','OPTIONS'])
@app.route('/<path:path>',methods=['GET', 'POST','PUT','OPTIONS'])
def proxy(path):
    print(request.full_path)
    if(request.method=='GET'):
        res= get(request)
        headers=dict(res.headers.items())
        headers['Access-Control-Allow-Origin']=origin
        return (res.text, res.status_code, headers.items())
    elif(request.method=='PUT'):
        res= put(request)
        headers=dict(res.headers.items())
        headers['Access-Control-Allow-Origin']=origin
        return (res.text, res.status_code, headers.items())
    elif(request.method=='DELETE'):
        res= delete(request)
        headers=dict(res.headers.items())
        headers['Access-Control-Allow-Origin']=origin
        return (res.text, res.status_code, headers.items())
    elif(request.method=='POST'):
        res= post(request)
        headers=dict(res.headers.items())
        headers['Access-Control-Allow-Origin']=origin
        return (res.text, res.status_code, headers.items())
    elif(request.method=='OPTIONS'):
        res= options(request)
        headers=dict(res.headers.items())
        headers['Access-Control-Allow-Origin']=origin
        return (res.text, res.status_code, headers.items())



app.add_url_rule("/", view_func=proxy,provide_automatic_options=False)

