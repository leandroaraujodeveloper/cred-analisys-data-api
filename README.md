# CREDIT ANALISYS API

##### Table of Contents  
[Introdução](#intro)  
[Fontes de dados](#fontes)
[Serviços e Componentes](#servicos)
[Implementação](#implementacao)
[Utilizando o código fonte](#codigofonte)
[Observações](#observacoes)

<a name="intro"/>
### Introdução

A seguir é apresentada uma das possíveis soluções para o problema de analise de credito de forma a gerar algumas discussões quais, precedem a implementação do MVP desta solução, para que sejam identificados possíveis problemas já na sua concepção.

![docs/img/Componentes_Cred_Analisys.png](docs/img/Componentes_Cred_Analisys.png)

Diagrama de Componentes de uma proposta de API de analise de crédito
<a name="fontes"/>
### Fontes de dados

Assim como na descrição formal do problema temos três fontes de dados... São representadas no diagrama nesta primeira implementação de forma que possamos ter uma ideia de que fonte de dados estamos tratando atribuindo a nomenclatura referente aos objetivos de cada fonte de dados para facilitar na concepção dos serviços de consulta á essas fontes assim como a definição das ferramentas que irão gerir as mesmas. Sendo assim:

**A_CONSUMER**

Dados dos consumidores quais requerem segurança e acesso que não necessitará de muito desempenho. Essa base de dados pode ter um banco de dados relacional como Postgresql com os mecanismos de segurança devidamente verificados e testados na sua implementação.

**B_RATING**

Dados que necessitam de segurança porém um pouco mais de velocidade no acesso para realizar cálculos de forma performática gerando outros dados durante as consultas. Nesse caso podemos utilizar MongoDB ou ElasticSearch por conta do armazenamento distribuído que bem implementado pode-se acrescentar mais segurança dos dados ao criar redundâncias explorando o melhor da ferramenta escolhida.

**C_TRANSACTIONS**

Uma base de dados extremamente rápida necessita de um pouco mais de atenção quanto as decisões técnicas. Por exemplo ao escolher uma ferramenta como um banco de dados relacional ele irá dizer "Ei não posso ir tão rápido preciso verificar algumas tabelas", ou seja precisaremos de algo mais versátil... Então recorreremos á um banco de dados não relacional que atenderá nossas requisições de forma bem performática com certeza, porém quando nossas requisições escalarem ele poderá nos dizer "Ei posso ser bem rápido, mas que tal pedir um pouco menos?", nesse caso ainda ficamos com uma espécie de gargalo, pois não existe bala de prata nesses casos. Contudo podemos pensar em uma forma de "pedir" menos dados e isso pode-se fazer guardando algumas respostas para entregar em consultas futuras.

<a name="servicos"/>
### Serviços e Componentes

Para consultar as fontes de dados foram planejados alguns serviços que devem ser implementados para resolver questões como: Fazer múltiplas conexões nos bancos de dados, tratar os dados recebidos,  implementar módulos de aprendizado de máquina para auxiliar nas analises, entre outros serviços que surgirem como requisito durante o planejamento / desenvolvimento.  Os serviços serão listados a seguir:

**`manage_connections`**

Serviço que será responsável por gerenciar as conexões dos banco de dados, manipulando diferentes fontes de dados e tratando de forma a serem lidos por outros serviços.

**`data_wrapper`**

Componente que manipula os dados de forma a disponibilizar os mesmos em estruturas de dados adequadas para o contexto da aplicação.

**`Consumer`**

Entidade para os dados pessoais do consumidor que serão provenientes de um banco de dados relacional.

- **`rating_analisys`** Modulo de geração de dados provenientes de algoritmos de aprendizado de máquina

    **`rating_data_generator`**

    Serviço qual irá gerar dados utilizando modelos de aprendizado de máquina com base em alguns dados do consumidor

    **`rating_data_provider`**

    Serviço que irá disponibilizar os dados gerados anteriormente para serem consumidos por outros serviços

**`C_TRANSACTIONS_foward`**

Este será um serviço que irá inserir os dados que necessitam de alta velocidade em um banco de dados *memcached* como a ideia inicial é utilizar um banco de dados NoSQL para os dados que necessitam de consultas rápidas e inserir alguns desses dados neste banco que será o Redis. 

**`cred_analilys_data_api`**

Os serviços citados anteriormente serão disponibilizados através de uma API(*Application Programming Interface*) que fornecerá recursos de consulta que necessitarão de ser gerenciados conforme aumentar-mos a complexidade dos serviços.

<a name="implementacao"/>
### Implementação

Foram escolhidas algumas ferramentas de para fazer toda essa arquitetura rodar de a principio atendendo os requisitos iniciais da API, podendo ser atualizada conforme a necessidade. As ferramentas e serviços estarão listados a seguir.
#### Flask 
Foi utilizado o framework flask da liguagem python que é utilizado para desenvolver aplicações web de forma simples porém performatica. Aqui utilizaremos o Flask Restful que faz parte do flask para criar os recursos da nossa api.
![docs/img/flask.png](docs/img/flask.png)
#### Nameko 
Vamos começar pelo mais importate que faz acontecer a 'mágica' das chamadas remotas de para os micro-serviços criados na aplicação. De forma simples as chamadas remotas RPC(Remote Procedure Call) vão prover a comunicação para requisições de diferentes espaços de endereçamento dentro de uma rede compartilhada, ou seja, podemos ter acesso aos serviços criados dentro da nossa aplicação de forma distribuida, o que ė de extrema importancia para aplicações que precisam ser escaláveis e nos da liberdade para criar diversos tipos de recurso para manter nossa api de pé e performática. Logo o nameko será a ferramenta qual proverá a criação das chamadas remotas dos micro-serviços.
![docs/img/nameko.png](docs/img/nameko.png)

#### RabbitMQ
É o serviço de mensaokgeria que irá tornar possível o streaming dos dados gerados pelos serviços criados anteriormente utilizando o nameko. Vale ressaltar a importancia do streamming de dados quando se trabalha com diferentes fontes e serviços que irão prover dados para a aplicação.
<img src="docs/img/rabbitmq.png" alt="drawing" width="300"/>
#### MongoDB
Banco de dados NoSql que irá armazenar os dados de uma ou duas das fontes de dados primarias, a estrutura de documentos e a performance do mongoDB o torna uma opção apropriada para consultas performaticas.
![docs/img/mb  	ongodb.jpg](docs/img/mongodb.jpg)
#### Docker
Para colocar-mosveri tudo isso para funcionar em produção seja qual for o serviço de hospedagem ou ambiente de cloud nós iremos utilizar um container docker para colocar as dependencias e scripts necessários para o correto duncionamento da aplicação e para facilitar a integração de mais ferramentas e serviços no futuro.
![docs/img/docker.png](docs/img/docker.png)
#### Postgresql
Utilizaremos um banco de dados relacional para armazenar os dados mais criticos para que possam ser implementados os mecanismos de segurança adequados para esses dados. O postgresql possibilita a implementação de diversos plugins que o deixam ainda mais robusto.
<img src="docs/img/postgres.png" alt="drawing" width="400"/>
#### Elasticsearch
O elasticsearch podeerá provero armezenamento das bases de dados que necessitarão de consultas extremamente rapidas e também para as bases quais os dados serão utilizados em modelos de aprendizado de maquina para gerar dados a partir destes.O elasticsearch é utilizado em grandes projetos de alta disponibilidade.
<img src="docs/img/elasticsearch.png" alt="drawing" width="400"/>
#### Redis 
Alguns dados necessitarão estar extremantente disponiveis em consultas frequentes estes poderão ser armazenados em um banco de dados memcached aqui escolhido o Redis para que os dados estejam disponiveis em memoria armazenando consultas em cache reduzindo as requisições da api consequentemente diminuindo a carga de requisições e melhorando a performance na disponibilidade dos dados para o cliente.
<img src="docs/img/redis.png" alt="drawing" width="400"/>

<a name="codigofonte"/>
### Utilizando o código fonte 
As dependencias da aplicação foram colocadas em um container do docker para possibilitar a inicialização dos serviços necessários. A seguir a sequencia de passos para se seguir para subir a API.

#### Criando ambiente virtual python e instalando bibliotecas
Caso não tenha instalado recomendo que instale o gerenciador de ambientes vituais do python com o comando `pip3 install virtualenv` para executar os passos a seguir.

	$ cd cred-analisys-data-api
    $ virtualenv env
    $ source env/bin/activate
Agora que criamos nosso ambiente local do python deixamos as coisas um pouco mais organizadoas para instala.
	
    $ pip3 install -r requirements.txt 
	

#### Inicialização do container
Inicialize o container com o comando abaixo.

	$ docker-compose up -d

#### Inicializado nameko
Em seguida vamos inicializar o nameko  para prover a comunicação do serviço criado.	
	
    $ cd services
    $ nameko run manage_connections:DataSourceService

#### Inicializando a API
Por fim iniciaremos a API que disponiblilizará os recursos dos serviços criados.

	$ python api.py
    
<a name="observacoes"/>
### Observações
Algumas funcionalidades ainda precisam ser complementadas portanto vamos elencar alguns dos próximos passos.
 - Configuração dos bancos de dados no container docker;
 - Integração do Redis para a armazenar alguns dados da API;
 - Implementar mecanismo de autenticação;
 - Criar rotinas de deploy (CI/CD);
 - Criar serviço para implementar modelos de aprendizado de maquina para a realização de analises baseadas em eventos de atividades do consmidor.
