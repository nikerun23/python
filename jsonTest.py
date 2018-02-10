import json

dict_object = {
    'name' : 'hyunkeun',
    'age' : 34,
    'email' : 'lee@gmail.com'
}

json.dump(dict_object, open('sample.json', 'a+'))

dict_object2 = json.load(open('sample.json'))

print(dict_object2)