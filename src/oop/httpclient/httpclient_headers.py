from urllib import request,  parse

url = 'http://httpbin.org/post'

params = {
    'name1': 'value1',
    'name2': 'value2'
}

querystring = parse.urlencode(params)

# Extra headers
headers = {
    'User-agent' : 'none/ofyourbusiness',
    'Spam' : 'Eggs'
}

req = request.Request(url, querystring.encode('ascii'), headers=headers)
u = request.urlopen(req)
response = u.read()

print(response)
