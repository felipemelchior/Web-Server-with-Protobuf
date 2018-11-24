# WebServer with JSON

## Métodos Disponíveis
### GET
Utilizado para receber um arquivo que está hospedado no servidor
### POST
Utilizado para criar um arquivo no serivdor
### DELETE
Utilizado para deletar um arquivo hospedado no serivdor, um cliente não pode excluir um arquivo que não é de sua autoria. (TODO Script de distribuição de ID)

## Uso
Dependências: <br>
```
$ python3
```

```

Módulos de criptografia - pip3 install pycrypto
```

<br>

Inicialmente, inicie o código do servidor: <br>
```
# python3 server.py -i <IP_Server> -p <Porta_Server>
```

<br>

Em seguida, execute o código do cliente: <br>
```
# python3 client.py -i <IP_Server> -p <Porta_Server>
```

<br>

Após isso, os códigos irão começar a execução e através do código de cliente será possível realizar as requisições para que então, o código de servidor analise a requisição e a execute.

## Desenvolvedores

* Felipe Homrich Melchior - UNIPAMPA - [Perfil GitHub](https://github.com/homdreen) <br>
* Wesley Ferreira - UNIPAMPA - [Perfil GitHub](https://github.com/wesferr) <br>
