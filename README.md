<h1 align='center'>Projeto 2 - Protocolo de enlace</h1>
<p align="center">Projeto de desenvolvimento de um <a href="https://pt.wikipedia.org/wiki/Point-to-Point_Protocol">protocolo de enlace ponto-a-ponto</a></p>

Tabela de conteúdos
=================
<!--ts-->
   * [Protocolo de Enlace](#Protocolo-de-Enlace)
   * [Objetivos](#Objetivos)
   * [Arquitetura do Projeto](#arquitetura-do-projeto)
   * [Pré-requisitos](#Pré-requisitos)
   * [Instruções para Uso](#Instruções-para-Uso)
   * [Autores](#Autores)

## Protocolo de Enlace

O Projeto desenvolvido neste repositório foi baseado no protocolo de enlace ponto-a-ponto (PPP), um protocolo de enlace de dados usado para estabelecer conexão direta ente dois nós. Este protocolo é utilizado na camada física do tipo UART, possuí um encapsulamento de mensagens com até 1024 bytes, garantia de entrega, criptografia de transmissão, controle de acesso ao meio, e estabelecimento de sessão (Este não foi implementado durante o semestre por conta de tempo hábil).

O PPP é usado sobre muitos tipos de redes físicas incluindo cabo serial, linha telefônica, linha tronco, telefone celular, enlaces de rádio especializados e enlaces de fibra ótica como SONET. O PPP também é usado sobre conexões de acesso à Internet. Provedores de serviços de Internet têm usado o PPP para acesso discado à Internet pelos clientes, uma vez que pacotes IP não podem ser transmitidos sobre uma linha de modem por si próprios, sem algum protocolo de enlace de dados.

Existem dois derivdados do PPP, o Point-to-Point Protocol over Ethernet (PPPoE), em português protocolo ponto a ponto sobre Ethernet, e Point-to-Point Protocol over ATM (PPPoA), em português Protocolo ponto a ponto sobre ATM, que são usados mais comumente por Provedores de Serviços de Internet para estabelecer uma conexão de serviços de Internet de Linha Digital de Assinante (ou DSL) com seus clientes.

![](images/projeto-ppp.png)

## Objetivos

Os objetivos deste repositorio foram desenvolver uma aplicação integrada ao protocolo implementado que possibilite o envio e recepção de mensagens via um terminal de texto. Mas que também possa ser utilizado em outras aplicações, assim se apresentando na forma de uma API. Podendo se comunicar biderecionalmente com a implementação de referência.

## Arquitetura do Projeto

O Protocolo desenvolvido pela equipe se comunica atráves de um link utilizando portas seriais, estas sendo emuladas com o [Serialemu](https://github.com/IFSCEngtelecomPTC/Serialemu). O Protocolo é divido em subcamadas: enquadramento, arquitetura, aplicação (também referencia em sala como adaptação). A seguir será explicado a funcionalidade de cada componente do projeto.

### Protocolo

A classe protocolo nada mais é que uma interface da biblioteca do protocolo, podendo instanciar um objeto do tipo Protocolo que faz conexão das subcamadas ao informar a porta serial e o timeout, utilizado para o tratamento de Callbacks.

### Subcamada

A classe subcamada auxilia na conexão das subcamadas mencionadas anteriormente, entre superior e inferior.

### Enquadramento

Este é responsável por delimitar o quadro, utilizando a técnica do tipo sentinela com uma flag de valor `7E` como delimitador do quadro, um byte de escape(esc) `7D` para o prenchimento da mensagem. O transmissor faz o escape dos bytes `7E` e `7D` modificando-os por meio de um XOR `20`

![](images/enq-mef.png)

### Arquitetura

Este é conjunto de mecanismos que têm como finalidade garantir a entrega de mensagens, preservando a ordem do envio e buscando eficiência no uso do canal. Possibilitando que o transmissor se certifique de que uma mensagem foi entregue ou não ao destino. Enquanto uma mensagem não tiver sua entrega assegurada, ela permanece na fila de saída mantida no transmissor pelo protocolo. Estes mecanismos são baseados em:
- Dois tipos de mensagens: DATA e ACK
- Mensagens de confirmação ACK sendo 0 ou 1.
- Mensagens são numeradas de acordo com uma sequência
- Retransmissão de mensagens perdidas ou recusadas

![](images/arq-mef.png)

### Aplicação

A aplicação é responsável por lê sequências de caracteres do terminal e passar o quadro  para a arquitetura. Bem como, receber os dados desencapsulados que são recebidos da arquitetura e apresenta-los no terminal.

Foi desenvolvido dois métodos iniciar (start) e parar (stop) visando facilitar a execução/encerramento do projeto.
## Pré-requisitos

Para executar o projeto basta seguir os passos abaixo:

- Clone o repositório do projeto e acesse o diretório que contém o codigo:

```bash
$ git clone https://github.com/mmsobral-croom/projeto-2-um-protocolo-de-enlace-arthur-alana-jefferson

$ cd protocolo-enlace
```

- Obtenha o código-fonte do serialemu neste <a href="https://github.com/IFSCEngtelecomPTC/Serialemu">repositório</a> no github. Em seguida compile manualmente:

```bash
$ g++ -o serialemu *.cpp -lpthread -lutil -std=c++11
```

- Instale o pyserial, junto ao código fonte na pasta `protocolo-enlace` para rodar o projeto:

```bash
$ pip3 install pyserial
```

## Instruções para Uso

Primeiramente é necessário ter duas portais seriais para que possa ser utilizado a biblioteca do PPP. Por isso será utilizado o serialemu para gerar um par de porta seriais como visto a seguir:

```bash
$ ./serialemu -h
BER: taxa de erro de bit, que deve estar no intervalo  [0,1]
atraso: atraso de propagação, em milissegundos.
taxa_bits: taxa de bits em bits/segundo
-f: executa em primeiro plano (nao faz fork)

$ ./serialemu [-b BER][-a atraso][-f][-B taxa_bits]
```

Após executar de forma deseja o emulador de porta serias, anote os dois caminhos informados pelo serialemu: eles são as duas portas seriais que correspondem às pontas do link serial emulado. Então podera rodar o projeto com uma das portas seriais dada pelo serialemu como parâmetro no terminal 1:

```bash
$ python3 test.py [porta_serial_1]
```

O mesmo procedimento para a execução do projeto será feito em um segundo terminal, mas utilizando a outra porta do par de portas seriais obtidas pelo serialemu:

```bash
$ python3 test.py [porta_serial_2]
```

Caso deseje também há um binario de implementação de referencia ao protocolo, desenvolvido pelo professor da disciplima, para ser executado, caso dejese como um dos terminais envolivdos na comunicação (Obs: Neste caso deve se utilizar obrigatoriamente a flag de `--noSession`):

```bash
$ ./proto -h
Uso: ./proto_noarq --serialPath /dev/XXX [opções] | -h

Opções:
 --debug: ativa debug em todas as subcamadas
-h: mostra esta ajuda

Opções relacionadas a Sessão:
--idSession ID: define o número do id de sessão entre 0 e 255. default: 0
--master: define como iniciador de sessao
--noSession: desativa o controle de sessão
--idError T: frequência de erros de id de sessão (1 a cada T mensagens com id sessão errado)
--debugSession: ativa mensagdens de debug de sessão

Opções relacionadas a ARQ:
--noArq: desativa o ARQ
--ackError T: frequência de erros de Ack (1 a cada T ACK recebidos são descartados)
--dataError T: frequência de erros de DATA (1 a cada T DATA recebidos são descartados)
--maxRetries N: limite de retransmissões do ARQ (default: 3)
--ackTimeout T: timeout de espera por ACK no ARQ, em milissegundos (default: 1000)
--debugArq: ativa mensagdens de debug de Arq

Opções relacionadas a Enquadramento:
--noFcs: desativa a detecção de erros
--fcsError T: frequência de erros de FCS (1 a cada T quadros transmitidos com erro proposital)
--flagError T: frequência de erros de Flag (1 a cada T flags omitidas propositalmente)
--mtu N: valor da MTU (default: 1024)
--debugEnq: ativa mensagens de debug de Enquadramento
```

## Autores

<a href="https://github.com/ArthurAnastopulos">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/51097061?v=4" width="100px;" alt=""/><br />
    <sub><b>Arthur Anastopulos dos Santos</b></sub></a><br />

<a href="https://github.com/alanamandim">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/58298192?v=4" width="100px;" alt=""/><br />
    <sub><b>Alana Mandim</b></sub></a><br />

<a href="https://github.com/jeffersonbcr">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/58866006?v=4" width="100px;" alt=""/><br />
    <sub><b>Jefferson Botitano</b></sub></a>