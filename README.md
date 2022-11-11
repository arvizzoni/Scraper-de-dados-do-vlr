# Scraper-de-dados-do-vlr

Nesse repositório, estou armazenando alguns scripts conjuntos de dados e análises. Tudo se relaciona diretamente com projetos para raspagem de dados do vlr.gg, um site que armazena estatísticas de partidas competitivas de VALORANT. O carro chefe desse repositório é o script valorant_final.py. Com ele, é possível excluir informações de todas as partidas presentes no banco de dados do vlr.gg, desde coisas simples como quem ganhou a partida x até quantos abates de Operator o Sacy tem contra o shion.

## Scraper de todas as partidas

Com o nome valorant_final.py, é um script de Python feito com o objetivo de permitir a extração de dados de partidas competitivas de VALORANT que estejam no vlr.gg.

### Como usar o script

Para utilizá-lo, basta ter instalado o Python (na minha máquina, instalei a versão 3.10, mas, acredito que algumas mais antigas funcionarão também). Em seguida, coloco o script na pasta em que meu Python está instalado, no meu caso: AppData\Local\Programs\Python\Python310.

#### Pré-requisitos

No arquivo requirements.txt estão os pacotes necessários para que o script funcione corretamente. Depois de instalá-los, o código está pronto para ser usado.

##### valorant match links.txt

Mas, para que ele funcione corretamente, ele precisa do arquivo valorant match links.txt. Nesse txt ficam todas as partidas que já foram extraídas.

Toda vez que o script roda, ele gera um novo arquivo com esse nome, com as novas partidas extraídas. O que eu faço é sempre salvar o txt com outro nome também, antes de usar o script.

Depois, pego o novo valorant match links.txt e adiciono as partidas do arquivo original, que salvei com outro nome. Por isso, é possível encontrar outros arquivos txt com valorant match links no nome, nesse repositório.

### Estrutura dos dados

Caso tudo tenha sido feito corretamente e o script tenha sido executado, os dados das partidas começarão a ser extraídos. Isso pode demorar dias, na primeira execução, porque são milhares de partidas.

Todas as informações serão extraídas para uma pasta com o nome valorant, que estará na mesma pasta onde o script foi colocado.

Dentro da pasta "valorant" será criada uma pasta para cada partida que se quer extrair, com o nome sendo o id da partida dentro da base do vlr.gg. E os dados da partida estarão lá.

#### Exemplo

No link https://www.vlr.gg/133419 é possível ver as informações de uma partida entre Alter Ego Celeste e W Streak. 133419 é o id da partida dentro da base, então, será criada uma pasta com o nome 133419, para esse conjunto de dados.

Quando se abre a pasta 133419, vê-se dois arquivos (header data.txt e Team score.xlsx) e três pastas (economy, overview e performance).

Nos arquivos, há dados básicos sobre a partida: qual foi o campeonato jogado, em que dia a partida ocorreu, qual foi o placar, etc.

Já nas pastas, encontra-se informações mais específicas. Nelas, há pastas para cada mapa da partida, e dentro dessas pastas há planilhas do Excel com os dados exibidos no vlr.gg.

Os nomes de cada planilha indicam qual tabela está sendo armazenada e são bem intuitivos, pois seguem o padrão visual e de nomes do vlr.gg. Por exemplo, caso se queira os dados da tabela "Overview" do mapa Haven, basta entrar nas pastas overview e Haven.

Ou seja, caso se esteja interessado em analisar quantos pistols a Alter Ego Celeste ganhou no mapa Breeze, é só seguir este caminho: valorant\133419\economy\Breeze\economy bottom table.xlsx. No arquivo, vê-se que a Alter Ego ganhou um pistol e perdeu o outro.

### 📄 Licença

Este projeto foi criado com o intuito de ser difundido de forma gratuita, pois o objetivo é impulsionar o cenário de VALORANT. Sendo assim, qualquer pessoa pode utilizar o scraper.

O único pedido é que ninguém além de mim se diga autor ou proprietário desse projeto, caso queira divulgá-lo. Afinal, esse projeto é fruto do meu investimento e do trabalho do Vikas Sutariya.

## Scraper de dados de carreira

Com o nome Extração dos dados de carreiras de jogadores escolhidos.R, é um script de R feito para extrair todos os dados de carreira de jogadores escolhidos. Todas as informações são extraídas do vlr.gg.

### Como usar o script

Para utilizá-lo, basta ter instalado o R (na minha máquina, instalei a versão 4.1.1, mas, acredito que algumas mais antigas funcionarão também).

#### Pré-requisitos

Os pacotes XML, tidyverse, rvest e robotstxt são usados no script.

No arquivo Jogadores cujos dados serão extraídos.txt estão os nomes dos jogadores cujos dados se quer. É necessário que o nome esteja escrito igualmente ao que se utiliza na base do vlr.gg. Por exemplo, caso se queira extrair dados da carreira do Sacy, o nome deve ser escrito assim, e não "sacy". Caso o nome seja escrito errado, o scraper não trará os dados corretos.

### Estrutura dos dados

Caso tudo tenha sido feito corretamente e o script tenha sido executado, os dados dos jogadores serão extraídos. Caso se queira informações de milhares de jogadores, isso pode demorar algumas horas.

Todas as informações serão extraídas para um arquivo com o nome X - Dados brutos.csv, sendo X a data do dia em que o script for executado.

#### Exemplo

Caso se queira todos os dados de carreira dos jogadores da LOUD campeões do mundo em 2022, basta colocar os nomes deles no arquivo Jogadores cujos dados serão extraídos.txt, no seguinte formato:

aspas
Less
pancada
saadhak
Sacy

Em seguida, basta executar o script, e um arquivo csv será gerado com os dados dos cinco jogadores.

### 📄 Licença

Este projeto foi criado com o intuito de ser difundido de forma gratuita, pois o objetivo é impulsionar o cenário de VALORANT. Sendo assim, qualquer pessoa pode utilizar o scraper.

O único pedido é que ninguém além de mim se diga autor ou proprietário desse projeto, caso queira divulgá-lo. Afinal, esse projeto é fruto do trabalho.
