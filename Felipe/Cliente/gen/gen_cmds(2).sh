#!/bin/bash

[ $1 ] && [ $2 ] || { echo "Usage: $0 <quantos_arquivos> <local_dos_arquivos>"; echo "Example: $0 1000 ./contents"; exit; }

for i in `seq 1 $1`; 
do 
    echo "POST"
    echo "$2/file-$i.dd"
done

for i in `seq 1 $1`; 
do 
    CMD=$((RANDOM%15))
    if [ $CMD -le 5 ]
    then
        echo "POST"
        echo "$2/file-$i.dd"
    elif [ $CMD -le 10 ]
    then
        echo "GET"
        echo "$2/file-$i.dd"
    else
        echo "DELETE"
        echo "$2/file-$i.dd"
    fi
done
echo "SAIR"
