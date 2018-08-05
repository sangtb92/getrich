import requests

api_gateway_host = 'localhost'
api_gateway_port = '8001'

services = [
    {
        'name': 'user-service',
        'protocol': 'http',
        'host': 'users',
        'port': 5000
    }
]


def add_service():
    url = 'http://' + api_gateway_host + ':' + api_gateway_port + '/services'
    try:
        for service in services:
            r = requests.post(url=url, json=service)
    except Exception as e:
        print(e)


def update_service(service_name, **kwargs):
    url = 'http://' + api_gateway_host + ':' + api_gateway_port + '/services/' + service_name
    try:
        r = requests.patch(url, data=kwargs)
    except Exception as e:
        print(e)


def get_max():
    a = "abc(cba)ab(bac)c"
    print(a.count("("))
    if a.count("(") < 0:
        return a
    elif a.count("(") == 1:
        open_index = a.index("(")
        close_index = a.index(")")
        str_get = a[open_index + 1:close_index]
        return a[:open_index] + str_get[::-1] + a[close_index + 1:]
    else:
        sub_open_index = a.rindex("(")
        sub_close_index = a.index(")")
        first_string = a[a.index("(") + 1:a.rindex("(")][::-1]
        second_string = a[a.index(")") + 1:a.rindex(")")][::-1]
        sub_string = a[sub_open_index + 1:sub_close_index]
        return a[:a.index("(")] + second_string + sub_string + first_string + a[a.rindex(")") + 1:]

    return a


if __name__ == '__main__':
    sequence = [1, 3, 2, 1, 3]
    print(get_max())
