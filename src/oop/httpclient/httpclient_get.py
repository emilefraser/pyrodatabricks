from urllib import request,  parse

url = 'http://httpbin.org/get'

params = {
    'name1': 'value1',
    'name2': 'value2'
}

querystring = parse.urlencode(params)

# get request
u = request.urlopen(f'{url}?{querystring}')
response = u.read()

print(response)
