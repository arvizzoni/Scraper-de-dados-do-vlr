#Arquivo para gerar os cabeçalhos de cada partida cujos dados foram extraídos
#pelo scraper

#Diretório onde é feito tudo relacionado ao scraper
setwd('C:\\Users\\arviz\\Dropbox\\André\\Valorant\\VLR Scraper')

#Checagem dos diretórios presentes
todos_os_diretorios=list.dirs(path = "Informações dos jogos\\valorant", full.names = TRUE, recursive = TRUE)

#Como essa lista de diretórios inclui subdiretórios como overview, economy e
#assim por diante, o melhor é encontrar os nomes dos diretórios com apenas
#um nome após "Informações dos jogos\\valorant/"
todos_os_diretorios_nomes_quebrados=strsplit(x=todos_os_diretorios,split='/')
ids_das_partidas=rownames(table(do.call(what=rbind,args=todos_os_diretorios_nomes_quebrados)[,2]))

#Agora serão definidos os diretórios a serem usados
diretorios_a_serem_usados=paste0("Informações dos jogos\\valorant\\",ids_das_partidas)

#O Primeiro passo para tratamento de dados em si é o de lidar com os
#cabeçalhos das partidas. Os arquivos de cabeçalhos têm nome
#"header data.txt" e as informações que contêm são do tipo: id, stage, etc.

#Os arquivos a serem lidos são definidos a seguir
arquivos_a_serem_lidos=paste0(diretorios_a_serem_usados,'\\','header data.txt')

#Mas, não é possível automaticamente lê-los todos. Algumas partidas do
#vlr.gg possuem id mas não dados. Nesses casos, não há arquivos dentro de
#suas pastas. Então, é preciso descobrir quais arquivos não existem antes
#de tentar lê-los
arquivos_existem=unlist(lapply(X=as.list(arquivos_a_serem_lidos),FUN=file.exists))

#Para ler todos os arquivos é utilizada a função read.delim, que lê cada
#linha do txt. Essa escolha de função não é perfeita, porque há variáveis
#separadas por vírgulas dentro das linhas dos arquivos de texto. Elas
#precisarão ser separadas depois
informacoes_contidas_nos_arquivos=lapply(X=as.list(arquivos_a_serem_lidos[which(arquivos_existem==1)]),FUN=read.delim)

#O próximo passo é verificar se todas as listas têm o mesmo formato. Se sim,
#cada arquivo tera 10 linhas, e nas linhas 8 e 9 há 3 variáveis cada.
#Primeiro, chequemos se há 10 elementos em cada lista. Para isso, é
#necessário criar uma função que faça essa verificação
funcao_para_verificar_quantos_elementos_existem=function(x){
  return(length(x[[1]]))
}
numero_de_elementos_por_lista=unlist(lapply(X=informacoes_contidas_nos_arquivos,FUN=funcao_para_verificar_quantos_elementos_existem))

#Algumas das listas não têm 10 elementos, e é necessário verificar porque.
#Primeiro, chequemos o que aconteceu nesses casos
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==16)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==23)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==24)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==33)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==36)]

#Em todos os casos, vemos que os problemas são causados por quebras de
#linha dentro de frases. Para resolver o problema, temos duas etapas. A
#primeira é apagar todas as linhas vazias. A segunda é juntar a primeira
#linha antes da sequência de linhas vazias e a primeira depois. Vamos criar
#uma função que faça isso
funcao_que_ajeita_os_dados=function(x){
  lista=x[[1]]
  if(length(lista)>10){
    while(length(lista[which(lista!='')])!=10 & length(lista[which(lista=='')])>0){
      primeiro_valor_vazio=which(lista=='')[1]
      valores_preenchidos=which(lista!='')
      primeiro_valor_depois_do_primeiro_valor_vazio=valores_preenchidos[which(valores_preenchidos>primeiro_valor_vazio)[1]]
      valores_antes_do_primeiro_valor_vazio=lista[c(1:(primeiro_valor_vazio-1))]
      ultimo_valor_antes_do_primeiro_valor_vazio=paste(valores_antes_do_primeiro_valor_vazio[primeiro_valor_vazio-1],lista[primeiro_valor_depois_do_primeiro_valor_vazio],sep=' ')
      valores_antes_do_primeiro_valor_vazio[primeiro_valor_vazio-1]=ultimo_valor_antes_do_primeiro_valor_vazio
      lista=c(valores_antes_do_primeiro_valor_vazio,lista[c((primeiro_valor_depois_do_primeiro_valor_vazio+1):length(lista))])
    }
  }
  return(lista)
}
informacoes_contidas_nos_arquivos_corretas=lapply(X=informacoes_contidas_nos_arquivos[c(1:1000)],FUN=funcao_que_ajeita_os_dados)

#Agora que os dados foram ajustados, o próximo passo é verificar se os
#números de elementos estão corretos (iguais a 10)
numero_de_elementos_por_lista_informacoes_corretas=unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))

#Parece que todos os dados estão corretamente organizados. O próximo passo
#é criar um data frame com a quantidade correta de colunas (14) e os nomes
#corretos para as variáveis. Mas, é necessário verificar se todas as linhas
#das listas possuem as informações corretas. Para isso, será criada uma
#função que verifica se as listas estão corretas, se cada linha contém
#apenas as variáveis que deveria conter, e mais nada