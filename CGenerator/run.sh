#!/bin/bash
echo "SERVIDOR ONLINE"
sudo python3 ../Servidor/server.py -i localhost -p 80&

echo "TESTES COM OS CLIENTES"

echo "TESTES RANDOMICO"
echo "RANDOMICO" >> tempos
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < rcmds; } 2>> tempos

echo "SEQUENCIAL" >> tempos
echo "TESTES SEQUENCIAL: POST GET DELETE"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < pgdcmds; } 2>> tempos

echo "TESTES DE DIVERSOS TAMANHOS"

echo "1k" >> tempos
echo "1k"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < cmds1k; } 2>> tempos

echo "100k" >> tempos
echo "100k"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < cmds100k; } 2>> tempos

echo "1m" >> tempos
echo "1m"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < cmds1m; } 2>> tempos

echo "100m" >> tempos
echo "100m"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < cmds100m; } 2>> tempos

echo "1g" >> tempos
echo "1g"
{ sudo time python3 ../Cliente/client.py -i localhost -p 80 < cmds1g; } 2>> tempos
