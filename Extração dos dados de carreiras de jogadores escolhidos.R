#Preâmbulo
library(XML)
library(tidyverse)
library(rvest)
library(robotstxt)

#Diretório onde os dados serão colocados
setwd('C:\\Users\\arviz\\Dropbox\\André\\Valorant\\VLR Scraper')

#Checagem de se o vlr.gg permite que seus dados sejam extraídos
paths_allowed(
  paths = c('https://www.vlr.gg/stats')
)
#Como o resultado foi positivo, continua-se com o scrapping

#Radical para as URLs
radical='https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=0&'
sufixo='&map_id=all&timespan=all'

#Possíveis valores para agentes jogados
agentes=c("Astra","Breach","Brimstone","Chamber","Cypher","Fade","Jett","Kay/O","Killjoy","Neon","Omen","Phoenix","Raze","Reyna","Sage","Skye","Sova","Viper","Yoru")
agentes_codigos_url=c("astra","breach","brimstone","chamber","cypher","fade","jett","kayo","killjoy","neon","omen","phoenix","raze","reyna","sage","skye","sova","viper","yoru")

#Jogadores cujos dados serão extraídos
jogadores=read.table('Jogadores cujos dados serão extraídos.txt')[[1]]

#Tabelas com os dados apenas dos jogadores extraídos para cada agente
tabelas_com_os_dados_de_agentes=list()
for(agente in c(1:19)){
  url_dos_dados=paste0(radical,'agent=',agentes_codigos_url[agente],sufixo)
  tabela_da_url=url_dos_dados %>%
    read_html() %>% 
    html_nodes('table') %>% 
    html_table(fill=T)
  tabela_da_url_como.data.frame=as.data.frame(tabela_da_url)
  nomes_dos_jogadores_na_tabela=do.call(what=rbind,args=strsplit(x=tabela_da_url_como.data.frame[,1],split="[\n]"))[,1]
  tabela_da_url_como.data.frame[,1]=nomes_dos_jogadores_na_tabela
  linhas_da_tabela_com_os_jogadores_escolhidos=match(x=jogadores,table=tabela_da_url_como.data.frame[,1])
  numero_de_colunas_na_tabela=dim(tabela_da_url_como.data.frame)[2]
  tabela_com_os_dados_com_o_agente=as.data.frame(matrix(0,nrow=length(jogadores),ncol=numero_de_colunas_na_tabela))
  colnames(tabela_com_os_dados_com_o_agente)=colnames(tabela_da_url_como.data.frame)
  tabela_com_os_dados_com_o_agente[,1]=jogadores
  tabela_com_os_dados_com_o_agente[,2]=agentes[agente]
  tabela_com_os_dados_com_o_agente[which(is.na(linhas_da_tabela_com_os_jogadores_escolhidos)==0),c(3:numero_de_colunas_na_tabela)]=tabela_da_url_como.data.frame[linhas_da_tabela_com_os_jogadores_escolhidos[which(is.na(linhas_da_tabela_com_os_jogadores_escolhidos)==0)],c(3:numero_de_colunas_na_tabela)]
  tabelas_com_os_dados_de_agentes[[agente]]=tabela_com_os_dados_com_o_agente
}

#Função para organizar os dados das tabelas
funcao_para_organizacao_das_tabelas=function(x){
  tabela=x[,c(1:4,6,7,12:14,16:20)]
  tabela_sem_NAs=tabela
  tabela_sem_NAs[is.na(tabela_sem_NAs)==1]="0"
  tabela_sem_NAs[tabela_sem_NAs==""]="0"
  tabela_sem_NAs[which(is.na(tabela_sem_NAs)==1)]="0"
  tabela_sem_NAs[which(tabela_sem_NAs=="")]="0"
  tabela_com_nomes_de_linha=tabela_sem_NAs
  rownames(tabela_com_nomes_de_linha)=tabela[,1]
  tabela_com_nomes_de_linha=tabela_com_nomes_de_linha[,-1]
  if(sum(tabela_com_nomes_de_linha[,3])>0){
    tabela_organizada=cbind(tabela_com_nomes_de_linha[,-c(7,8)],do.call(rbind,strsplit(tabela_com_nomes_de_linha[,8],split='/')),tabela_com_nomes_de_linha[,12]/tabela_com_nomes_de_linha[,9],tabela_com_nomes_de_linha[,11]/tabela_com_nomes_de_linha[,9],as.numeric(do.call(rbind,strsplit(tabela_com_nomes_de_linha[,8],split='/'))[,2])/tabela_com_nomes_de_linha[,2],as.numeric(do.call(rbind,strsplit(tabela_com_nomes_de_linha[,8],split='/'))[,1])/as.numeric(do.call(rbind,strsplit(tabela_com_nomes_de_linha[,8],split='/'))[,2]))
  }
  else{
    tabela_organizada=cbind(tabela_com_nomes_de_linha[,1:2],as.data.frame(matrix(0,length(jogadores),15)))
  }
  colnames(tabela_organizada)=c('Agent','Rounds played','Average Combat Score','KAST pct','Average damage per round','HS pct','Kills','Deaths','Assists','First Kills','First Deaths','Clutches Won','Clutch Situations','Assists per Kill','First Kills per Kill','Clutch Situations per Round','Clutch Success pct')
  tabela_organizada$`KAST pct`=as.numeric(gsub(x=tabela_organizada$`KAST pct`,pattern='%',replacement=''))/100
  tabela_organizada$`HS pct`=as.numeric(gsub(x=tabela_organizada$`HS pct`,pattern='%',replacement=''))/100
  return(tabela_organizada)
}

#Aplicação da função na lista de tabelas
tabela_final=do.call(cbind,lapply(X=tabelas_com_os_dados_de_agentes,FUN=funcao_para_organizacao_das_tabelas))

#Salvamento do arquivo
tabela_final[is.na(tabela_final)==1]="0"
write.csv2(tabela_final,file=paste0(Sys.Date(),' - Dados brutos.csv'))