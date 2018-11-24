# WebServer with BSON

Este codigo tem como objetivo, exemplificar um caso de uso BSON, criado pela Google.
Trata-se de uma representação de um servidor web que executa em linha de comando.

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
Módulos BSON - pip3 install bson

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
$ python3 client.py -i <IP_Server> -p <Porta_Server>
```

<br>

Após isso, os códigos irão começar a execução e através do código de cliente será possível realizar as requisições para que então, o código de servidor analise a requisição e a execute.

## Desenvolvedores

* Felipe Homrich Melchior - UNIPAMPA - [Perfil GitHub](https://github.com/homdreen) <br>
* Guilherme Neri Bustamante Sá - UNIPAMPA - [Perfil GitHub](https://github.com/161150744) <br>
* Lucas Antunes - UNIPAMPA - [Perfil GitHub](https://github.com/LucasAntunesdeAlmeida) <br>
* Wesley Ferreira - UNIPAMPA - [Perfil GitHub](https://github.com/wesferr) <br>
