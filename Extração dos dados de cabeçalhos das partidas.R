#Arquivo para gerar os cabe?alhos de cada partida cujos dados foram extra?dos
#pelo scraper

#Diret?rio onde ? feito tudo relacionado ao scraper
setwd('C:\\Users\\arviz\\Dropbox\\Andr?\\Valorant\\VLR Scraper')

#Checagem dos diret?rios presentes
todos_os_diretorios=list.dirs(path = "Informa??es dos jogos\\valorant", full.names = TRUE, recursive = TRUE)

#Como essa lista de diret?rios inclui subdiret?rios como overview, economy e
#assim por diante, o melhor ? encontrar os nomes dos diret?rios com apenas
#um nome ap?s "Informa??es dos jogos\\valorant/"
todos_os_diretorios_nomes_quebrados=strsplit(x=todos_os_diretorios,split='/')
ids_das_partidas=rownames(table(do.call(what=rbind,args=todos_os_diretorios_nomes_quebrados)[,2]))

#Agora ser?o definidos os diret?rios a serem usados
diretorios_a_serem_usados=paste0("Informa??es dos jogos\\valorant\\",ids_das_partidas)

#O Primeiro passo para tratamento de dados em si ? o de lidar com os
#cabe?alhos das partidas. Os arquivos de cabe?alhos t?m nome
#"header data.txt" e as informa??es que cont?m s?o do tipo: id, stage, etc.

#Os arquivos a serem lidos s?o definidos a seguir
arquivos_a_serem_lidos=paste0(diretorios_a_serem_usados,'\\','header data.txt')

#Mas, n?o ? poss?vel automaticamente l?-los todos. Algumas partidas do
#vlr.gg possuem id mas n?o dados. Nesses casos, n?o h? arquivos dentro de
#suas pastas. Ent?o, ? preciso descobrir quais arquivos n?o existem antes
#de tentar l?-los
arquivos_existem=unlist(lapply(X=as.list(arquivos_a_serem_lidos),FUN=file.exists))

#Para ler todos os arquivos ? utilizada a fun??o read.delim, que l? cada
#linha do txt. Essa escolha de fun??o n?o ? perfeita, porque h? vari?veis
#separadas por v?rgulas dentro das linhas dos arquivos de texto. Elas
#precisar?o ser separadas depois
informacoes_contidas_nos_arquivos=lapply(X=as.list(arquivos_a_serem_lidos[which(arquivos_existem==1)]),FUN=read.delim)

#O pr?ximo passo ? verificar se todas as listas t?m o mesmo formato. Se sim,
#cada arquivo tera 10 linhas, e nas linhas 8 e 9 h? 3 vari?veis cada.
#Primeiro, chequemos se h? 10 elementos em cada lista. Para isso, ?
#necess?rio criar uma fun??o que fa?a essa verifica??o
funcao_para_verificar_quantos_elementos_existem=function(x){
  return(length(x[[1]]))
}
numero_de_elementos_por_lista=unlist(lapply(X=informacoes_contidas_nos_arquivos,FUN=funcao_para_verificar_quantos_elementos_existem))

#Algumas das listas n?o t?m 10 elementos, e ? necess?rio verificar porque.
#Primeiro, chequemos o que aconteceu nesses casos
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==16)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==23)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==24)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==33)]
informacoes_contidas_nos_arquivos[which(numero_de_elementos_por_lista==36)]

#Em todos os casos, vemos que os problemas s?o causados por quebras de
#linha dentro de frases. Para resolver o problema, temos duas etapas. A
#primeira ? apagar todas as linhas vazias. A segunda ? juntar a primeira
#linha antes da sequ?ncia de linhas vazias e a primeira depois. Vamos criar
#uma fun??o que fa?a isso
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
informacoes_contidas_nos_arquivos_corretas=lapply(X=informacoes_contidas_nos_arquivos,FUN=funcao_que_ajeita_os_dados)

#Agora que os dados foram ajustados, o pr?ximo passo ? verificar se os
#n?meros de elementos est?o corretos (iguais a 10)
numero_de_elementos_por_lista_informacoes_corretas=unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))
table(numero_de_elementos_por_lista_informacoes_corretas)

#Pode-se ver que uma das listas tem 19 componentes. Vamos verificar o que a
#torna especial antes de seguir em frente
informacoes_contidas_nos_arquivos_corretas[[which(unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))!=10)]]

#V?-se que o que ? necess?rio fazer ? unir as strings a mais que tornam essa
#lista diferente das outras
informacoes_contidas_nos_arquivos_corretas[[which(unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))!=10)]][5]=paste(informacoes_contidas_nos_arquivos_corretas[[which(unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))!=10)]][5:14],collapse=' - ')
informacoes_contidas_nos_arquivos_corretas[[which(unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))!=10)]]=informacoes_contidas_nos_arquivos_corretas[[which(unlist(lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=length))!=10)]][-c(6:14)]

#Parece que todos os dados est?o corretamente organizados. O pr?ximo passo
#? criar um data frame com a quantidade correta de colunas (14) e os nomes
#corretos para as vari?veis. Mas, ? necess?rio verificar se todas as linhas
#das listas possuem as informa??es corretas. Para isso, ser?o criadas fun??es
#que verificam se as listas est?o corretas, se cada linha cont?m apenas as
#vari?veis que deveria conter, e mais nada

#A primeira fun??o presume que todas as listas t?m os mesmos formatos, e
#tenta encontrar as 4 colunas adicionais necess?rias
funcao_para_gerar_o_numero_correto_de_colunas=function(x){
  if(grep(x[1],pattern='Match Name')==1 & grep(x[2],pattern='Match Stage')==1 & grep(x[3],pattern='Match Type')==1 & grep(x[4],pattern='Match Date')==1 & grep(x[5],pattern='Match Time')==1 & grep(x[6],pattern='Match Score Type')==1 & grep(x[7],pattern='Match Note')==1 & grep(x[8],pattern='Team1')==1 & grep(x[9],pattern='Team2')==1 & grep(x[10],pattern='Betting line')==1){
    variaveis_adicionais_do_time1=strsplit(x[8],split=', ')
    variaveis_adicionais_do_time2=strsplit(x[9],split=', ')
    y=c(x[1:7],unlist(variaveis_adicionais_do_time1),unlist(variaveis_adicionais_do_time2),x[10])
  }
  return(y)
}
dados_de_linhas_da_tabela_final_v1=lapply(X=informacoes_contidas_nos_arquivos_corretas,FUN=funcao_para_gerar_o_numero_correto_de_colunas)
numero_de_elementos_por_lista_dados_de_linhas_v1=unlist(lapply(X=dados_de_linhas_da_tabela_final_v1,FUN=length))
table(numero_de_elementos_por_lista_dados_de_linhas_v1)

#Pode-se ver que o resultado n?o foi perfeito. Mas, como apenas uma lista
#tem um tamanho diferente, n?o ? preciso criar mais uma fun??o
dados_de_linhas_da_tabela_final_v1[[which(numero_de_elementos_por_lista_dados_de_linhas_v1!=14)]]

#Mais uma vez, basta unir as strings
dados_de_linhas_da_tabela_final_v1[[which(numero_de_elementos_por_lista_dados_de_linhas_v1!=14)]][11]=paste(dados_de_linhas_da_tabela_final_v1[[which(numero_de_elementos_por_lista_dados_de_linhas_v1!=14)]][11:12],collapse=', ')
dados_de_linhas_da_tabela_final_v1[[which(numero_de_elementos_por_lista_dados_de_linhas_v1!=14)]]=dados_de_linhas_da_tabela_final_v1[[which(numero_de_elementos_por_lista_dados_de_linhas_v1!=14)]][-c(12)]

#Agora que se sabe que todas as listas t?m o n?mero correto de vari?veis e
#est?o organizadas corretamente, o que falta ? gerar o data frame final.

#Primeiro, ser? criada uma fun??o que transforma cada lista em um data
#frame de apenas uma linha
funcao_que_gera_dfs_de_uma_linha=function(x){
  x[1]=strsplit(x[1],split='Match Name: ')[[1]][2]
  x[2]=strsplit(x[2],split='Match Stage: ')[[1]][2]
  x[3]=strsplit(x[3],split='Match Type: ')[[1]][2]
  x[4]=strsplit(x[4],split='Match Date: ')[[1]][2]
  x[5]=strsplit(x[5],split='Match Time: ')[[1]][2]
  x[6]=strsplit(x[6],split='Match Score Type: ')[[1]][2]
  x[7]=strsplit(x[7],split='Match Note: ')[[1]][2]
  x[8]=strsplit(x[8],split='Team1: ')[[1]][2]
  x[9]=strsplit(x[9],split='Score: ')[[1]][2]
  x[10]=strsplit(x[10],split='Elo Number: ')[[1]][2]
  x[11]=strsplit(x[11],split='Team2: ')[[1]][2]
  x[12]=strsplit(x[12],split='Score: ')[[1]][2]
  x[13]=strsplit(x[13],split='Elo Number: ')[[1]][2]
  x[14]=strsplit(x[14],split='Betting line: ')[[1]][2]
  nomes_das_colunas=c('Match Name','Match Stage','Match Type','Match Date','Match Time','Match Score Type','Match Note','Team1','Score','Elo Number','Team2','Score','Elo Number','Betting line')
  df_de_uma_linha=as.data.frame(t(x))
  colnames(df_de_uma_linha)=nomes_das_colunas
  return(df_de_uma_linha)
}
lista_de_dfs_de_uma_linha=lapply(dados_de_linhas_da_tabela_final_v1,FUN=funcao_que_gera_dfs_de_uma_linha)

#Agora ? a hora de juntar os data frames de uma linha, para ter um data
#frame com todas as linhas
df_final_v1=do.call(rbind,lista_de_dfs_de_uma_linha)

#O pr?ximo passo ? limpar os dados, de forma a serem mais facilmente
#utiliz?veis. Primeiro, adicionando o match id ao data frame
df_final_v2=df_final_v1
df_final_v2$'Match Id'=as.numeric(ids_das_partidas[which(arquivos_existem==1)])

#Em seguida, o data frame ser? ordenado em rela??o ao match id, que se
#tornar? a primeira coluna
df_final_v3=df_final_v2[order(df_final_v2$'Match Id'),]
df_final_v3=df_final_v3[,c(15,1:14)]

#O pr?ximo passo ? organizar as datas de cada partida. Depois de ordenado
#com base no valor do match id, o data frame fica quase em ordem temporal,
#o que facilita o trabalho de inferir o ano em que cada partida foi jogada

#Primeiro, ? preciso organizar os dias da semana, os dias do m?s e os meses
#em que cada partida foi jogada em 3 vari?veis diferentes
datas_divididas=do.call(rbind,strsplit(df_final_v3$'Match Date',split=' '))
dias_da_semana=do.call(rbind,strsplit(datas_divididas[,1],split=','))[,1]
meses=datas_divididas[,2]
possiveis_dias_do_mes=rownames(table(datas_divididas[,3]))
dias_corretos_do_mes=c(10:19,1,20:29,2,30,31,3:9)
dias_dos_meses=datas_divididas[,3]
for(dia_do_mes in possiveis_dias_do_mes){
  dias_dos_meses=gsub(x=dias_dos_meses,pattern=dia_do_mes,replacement=dias_corretos_do_mes[which(possiveis_dias_do_mes==dia_do_mes)])
}
df_final_v4=df_final_v3
df_final_v4$'Match day of the week'=dias_da_semana
df_final_v4$'Match day of the month'=as.numeric(dias_dos_meses)
df_final_v4$'Match month'=meses
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='January')]=1
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='February')]=2
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='March')]=3
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='April')]=4
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='May')]=5
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='June')]=6
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='July')]=7
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='August')]=8
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='September')]=9
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='October')]=10
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='November')]=11
df_final_v4$'Match month'[which(df_final_v4$'Match month'=='December')]=12
df_final_v4=df_final_v4[,c(1,16:18,2:15)]
df_final_v4=df_final_v4[,-8]

#Agora, sim, ? poss?vel inferir o ano em que cada partida foi jogada
grep(x=df_final_v4$'Match month',pattern='January')
#com base nesses dados, podemos definir onde ocorrem as viradas de ano
primeiro_id_de_2021=3716
primeiro_id_de_2022=11432
anos=rep(2020,times=length(df_final_v4[,1]))
anos[which(df_final_v4$'Match Id'>=primeiro_id_de_2021)]=2021
anos[which(df_final_v4$'Match Id'<=(primeiro_id_de_2021*1.5) & df_final_v4$'Match month'>10)]=2020
anos[which(df_final_v4$'Match Id'>=primeiro_id_de_2022)]=2022
anos[which(df_final_v4$'Match Id'>=(primeiro_id_de_2021*1.5) & df_final_v4$'Match Id'<=(primeiro_id_de_2022*1.5) & df_final_v4$'Match month'>10)]=2021
df_final_v5=df_final_v4
df_final_v5$'Match year'=anos
df_final_v5=df_final_v5[,c(1:4,18,5:17)]

#O pr?ximo passo ? limpar os dados de Elo Rating e de apostas
df_final_v5$'Elo Number'=as.numeric(gsub(x=gsub(x=df_final_v5$'Elo Number',pattern='[[]',replacement=''),pattern='[]]',replacement=''))
df_final_v5$`Elo Number.1`=as.numeric(gsub(x=gsub(x=df_final_v5$'Elo Number',pattern='[[]',replacement=''),pattern='[]]',replacement=''))
df_final_v5$'Betting line'[which(df_final_v5$'Betting line'==df_final_v5$'Betting line'[1])]=NA

#Finalmente, os dados podem ser salvos num csv
write.csv2(df_final_v5,file=paste0('Cabe?alhos de partidas',' - ',Sys.Date(),'.csv'))