
from random import randint


myGrammer='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SHORT_URL_SIZE = 7
id=100000000000
def encode_id():
    result = ''
    global id 
    decimal = id 
    while int(decimal):
        remainder = int(decimal) % 62
        result = myGrammer[remainder]+result
        decimal = decimal / 62
        id +=1
        
    return result
def encode_random():
    result = ''
    while True:
        
        for i in range(SHORT_URL_SIZE):
            randNumber = randint(0,61)
            result = myGrammer[randNumber] + result
        return result
        

