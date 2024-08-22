import requests


response = requests.post('http://127.0.0.1:7000/user',
                         json={'name': 'user_1',
                               "password": "4321"}
                         )
print(response.status_code)
print(response.text)


response = requests.get('http://127.0.0.1:7000/user/1',)
print(response.status_code)
print(response.text)


response = requests.patch('http://127.0.0.1:7000/user/1',
                         json={'name': 'user_q',
                               "password": "1234"}
                         )
print(response.status_code)
print(response.text)


response = requests.delete('http://127.0.0.1:7000/user/1',)
print(response.status_code)
print(response.text)


response = requests.post('http://127.0.0.1:7000/post', json={'heading': 'Post_1',
                                    'description': 'text_text_text_1',
                                    'user_id': 1})
print(response.status_code)
print(response.text)


response = requests.get('http://127.0.0.1:7000/post/1')
print(response.status_code)
print(response.text)


response = requests.patch('http://127.0.0.1:7000/post/2',
                    json={'heading': 'Post_22222',
                           'description': 'text_text_text_22222',
                            'user_id': 1
                            })
print(response.status_code)
print(response.text)


response = requests.delete("http://127.0.0.1:7000/post/1")
print(response.status_code)
print(response.text)
