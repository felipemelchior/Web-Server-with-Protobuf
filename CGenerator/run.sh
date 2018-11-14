echo "SERVIDOR ONLINE"
sudo python3 ../Servidor/server.py -i localhost -p 80&

echo "TESTES COM OS CLIENTES"

echo "TESTE RANDOMICO"
sudo python3 ../Cliente/client.py -i localhost -p 80 << rcmds
