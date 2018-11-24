#!/bin/bash

[ $1 ] && [ $2 ] && [ $3 ] || { echo "Usage: $0 <quantos_arquivos> <ate_quantos_bytes_por_arquivo> <local>"; echo "Example: $0 1000 20000 ./"; exit; }

MAXBYTES=$2

for i in `seq 1 $1`; 
do 
    RANDBYTES=$((RANDOM%MAXBYTES))
    dd if=/dev/zero of=$3/file-$i.dd bs=$RANDBYTES count=1
done

ls files/
