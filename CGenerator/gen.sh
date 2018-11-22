#!/bin/bash
echo "GERANDO ARQUIVOS DE TESTE"

dd if=/dev/urandom bs=1k count=10 | split -a 2 -b 1k - t.
dd if=/dev/urandom bs=100k count=10 | split -a 3 -b 100k - t.
dd if=/dev/urandom bs=1M count=10 iflag=fullblock | split -a 4 -b 1M - t.
dd if=/dev/urandom bs=100M count=10 iflag=fullblock | split -a 5 -b 100M - t.
dd if=/dev/urandom bs=1G count=3 iflag=fullblock | split -a 6 -b 1G - t.

name1k=("t.aa" "t.ab" "t.ac" "t.ad" "t.ae" "t.af" "t.ag" "t.ah" "t.ai" "t.aj")
name100k=("t.aaa" "t.aab" "t.aac" "t.aad" "t.aae" "t.aaf" "t.aag" "t.aah" "t.aai" "t.aaj")
name1m=("t.aaaa" "t.aaab" "t.aaac" "t.aaad" "t.aaae" "t.aaaf" "t.aaag" "t.aaah" "t.aaai" "t.aaaj")
name100m=("t.aaaaa" "t.aaaab" "t.aaaac" "t.aaaad" "t.aaaae" "t.aaaaf" "t.aaaag" "t.aaaah" "t.aaaai" "t.aaaaj")
name1g=("t.aaaaaa" "t.aaaaab" "t.aaaaac")

files=(${name1k[@]} ${name100k[@]} ${name1m[@]} ${name100m[@]} ${name1g[@]})

echo "GERANDO LISTAS DE COMANDOS"

commands=("GET" "POST" "DELETE")

echo "COMANDOS RANDOMICOS"

for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> rcmds
	echo ${files[$RANDOM % ${#files[@]}]} >> rcmds
done
echo "SAIR" >> rcmds

echo "COMANDOS SEQUENCIAIS: POST GET DELETE"

for i in {1..1000}
do
	echo "POST" >> pgdcmds
	echo ${files[$RANDOM % ${#files[@]}]} >> pgdcmds
done

for i in {1..1000}
do
	echo "GET" >> pgdcmds
	echo ${files[$RANDOM % ${#files[@]}]} >> pgdcmds
done

for i in {1..1000}
do
	echo "DELETE" >> pgdcmds
	echo ${files[$RANDOM % ${#files[@]}]} >> pgdcmds
done

echo "SAIR" >> pgdcmds

echo "COMANDOS TAMANHOS DIFERENTES"

echo "1K"
for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> cmds1k
	echo ${name1k[$RANDOM % ${#name1k[@]}]} >> cmds1k
done
echo "SAIR" >> cmds1k

echo "100K"
for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> cmds100k
	echo ${name100k[$RANDOM % ${#name100k[@]}]} >> cmds100k
done
echo "SAIR" >> cmds100k

echo "1M"
for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> cmds1m
	echo ${name1m[$RANDOM % ${#name1m[@]}]} >> cmds1m
done
echo "SAIR" >> cmds1m

echo "100M"
for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> cmds100m
	echo ${name100m[$RANDOM % ${#name100m[@]}]} >> cmds100m
done
echo "SAIR" >> cmds100m

echo "1G"
for i in {1..3000}
do
	echo ${commands[$RANDOM % ${#commands[@]} ]} >> cmds1g
	echo ${name1g[$RANDOM % ${#name1g[@]}]} >> cmds1g
done
echo "SAIR" >> cmds1g
