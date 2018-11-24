#!/bin/bash

[ $1 ] || { echo "Usage: $0 <quantos_arquivos>"; echo "Example: $0 1000"; exit; }

for i in `seq 1 $1`; 
do 
    echo "POST"
    echo "files/file-$i.dd"
done

for i in `seq 1 $1`; 
do 
    CMD=$((RANDOM%15))
    if [ $CMD -le 5 ]
    then
        echo "POST"
        echo "files/file-$i.dd"
    elif [ $CMD -le 10 ]
    then
        echo "GET"
        echo "files/file-$i.dd"
    else
        echo "DELETE"
        echo "files/file-$i.dd"
    fi
done
echo "SAIR"
