#!/usr/bin/python3

#   Authors: Wesley Ferreira de Ferreira and Willian Ferreira de Ferreira
#   Date: 6/9/2018
#   All Rights Reserved
#   V0.1

import hashlib, socket, sys, random, string
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random
from Crypto.Util.number import long_to_bytes
from treatment.key_pb2 import Prime_key, Public_key
from Crypto.Util.number import getPrime

#METODO QUE ENCRIPTA A MENSAGEM SEREALIZADA
def crypt(key, msg):
    crypt = AES.new(key.to_bytes(16, "big"), AES.MODE_CFB, b"REDESDECOMPUTADO")
    return crypt.encrypt(msg)

#METODO QUE DESENCRIPTA A MENSAGEM SEREALIZADA
def decrypt(key, msg):
    crypt = AES.new(key.to_bytes(16, "big"), AES.MODE_CFB, b"REDESDECOMPUTADO")
    return crypt.decrypt(msg)

def key_exchange(connection):

    key = Prime_key()
    key.ParseFromString(connection.recv(1024))

    private_key = getPrime(16)
    public_key = (key.base ** private_key) % key.public

    public_keyin, public_keyout = Public_key(), Public_key()
    public_keyout.key = (key.base ** private_key) % key.public

    public_keyin.ParseFromString(connection.recv(42))
    connection.send(public_keyout.SerializeToString())
    secrete_key = ( public_keyin.key ** private_key ) % key.public
    return secrete_key
