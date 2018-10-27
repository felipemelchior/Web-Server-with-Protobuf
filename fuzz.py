#!/usr/bin/python

import os

buffer = ["A"]
contador = 100
while len(buffer) <= 30:
    buffer.append("A"*contador)
    contador+=200

for string in buffer:
    print("GET")
    print(string)