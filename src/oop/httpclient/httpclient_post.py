from urllib import request,  parse

url = 'http://httpbin.org/post'

params = {
    'name1': 'value1',
    'name2': 'value2'
}

querystring = parse.urlencode(params)

# post request
u = request.urlopen(url, querystring.encode('ascii'))
response = u.read()

print(response)
