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
agentes=c("Astra","Breach","Brimstone","Chamber","Cypher","Fade",'Harbor',"Jett","Kay/O","Killjoy","Neon","Omen","Phoenix","Raze","Reyna","Sage","Skye","Sova","Viper","Yoru")
agentes_codigos_url=c("astra","breach","brimstone","chamber","cypher","fade",'harbor',"jett","kayo","killjoy","neon","omen","phoenix","raze","reyna","sage","skye","sova","viper","yoru")

#Tabelas com os dados para todos os jogadores que jogaram com cada agente
tabelas_com_os_dados_de_agentes=list()
for(agente in c(1:length(agentes))){
  url_dos_dados=paste0(radical,'agent=',agentes_codigos_url[agente],sufixo)
  tabela_da_url=url_dos_dados %>%
    read_html() %>% 
    html_nodes('table') %>% 
    html_table(fill=T)
  tabela_da_url_como.data.frame=as.data.frame(tabela_da_url)
  tabelas_com_os_dados_de_agentes[[agente]]=tabela_da_url_como.data.frame
}

#Função para calcular as medidas de resumo para cada agente
funcao_para_medidas_de_resumo=function(x){
  rodadas_jogadas=sum(x[,3])
  rating_medio=weighted.mean(x=x[which(is.na(x[,4])==F),4],w=x[which(is.na(x[,4])==F),3])
  ACS_media=weighted.mean(x=x[which(is.na(x[,5])==F),5],w=x[which(is.na(x[,5])==F),3])
  KD_medio=sum(x[,17])/sum(x[,18])
  KAST_da_amostra=as.numeric(do.call(rbind,strsplit(x[which(is.na(x[,7])==F),7],split="%")))
  KAST_media=weighted.mean(x=KAST_da_amostra,w=x[which(x[,7]!=rownames(table(tabelas_com_os_dados_de_agentes[[1]][which(is.na(tabelas_com_os_dados_de_agentes[[1]][,7])==F),7]))[1]),3])
  ADR_media=weighted.mean(x=x[which(is.na(x[,8])==F),8],w=x[which(is.na(x[,8])==F),3])
  KPR_media=weighted.mean(x=x[which(is.na(x[,9])==F),9],w=x[which(is.na(x[,9])==F),3])
  APR_media=weighted.mean(x=x[which(is.na(x[,10])==F),10],w=x[which(is.na(x[,10])==F),3])
  AK_medio=sum(x[,19])/sum(x[,17])
  FKPR_media=weighted.mean(x=x[which(is.na(x[,11])==F),11],w=x[which(is.na(x[,11])==F),3])
  FDPR_media=weighted.mean(x=x[which(is.na(x[,12])==F),12],w=x[which(is.na(x[,12])==F),3])
  FKK_medio=sum(x[,20])/sum(x[,17])
  FKFD_medio=sum(x[,20])/sum(x[,21])
  HS_da_amostra=as.numeric(do.call(rbind,strsplit(x[which(is.na(x[,13])==F),13],split="%")))
  HS_media=weighted.mean(x=HS_da_amostra,w=x[which(x[,13]!=rownames(table(tabelas_com_os_dados_de_agentes[[1]][which(is.na(tabelas_com_os_dados_de_agentes[[1]][,13])==F),13]))[1]),3])
  informacoes_de_clutch_da_amostra=cbind(as.numeric(do.call(rbind,strsplit(x[which(is.na(x[,15])==F),15],split="/"))[,1]),as.numeric(do.call(rbind,strsplit(x[which(is.na(x[,15])==F),15],split="/"))[,2]))
  clutches_jogados=sum(informacoes_de_clutch_da_amostra[,2])
  clutches_ganhos=sum(informacoes_de_clutch_da_amostra[,1])
  clutches_jogados_por_rodada=clutches_jogados/rodadas_jogadas
  sucesso_em_clutches=clutches_ganhos/clutches_jogados
  kmax_da_amostra=max(x[which(is.na(x[,16])==F),16])
  medidas_de_resumo=cbind(rodadas_jogadas,
         rating_medio,
         ACS_media,
         KD_medio,
         KAST_media,
         ADR_media,
         KPR_media,
         APR_media,
         AK_medio,
         FKPR_media,
         FDPR_media,
         FKK_medio,
         FKFD_medio,
         HS_media,
         clutches_jogados_por_rodada,
         sucesso_em_clutches,
         kmax_da_amostra)
  colnames(medidas_de_resumo)=c('Rodadas','Rating','ACS','K/D','KAST%','ADR','K','A','A/K','FK','FD','FK/K','FK/FD','HS%','Situações de clutches','CL%','KMAX')
  return(medidas_de_resumo)
}

#Organização das medidas de resumo dos agentes
medidas_de_resumo_dos_agentes=lapply(tabelas_com_os_dados_de_agentes,FUN=funcao_para_medidas_de_resumo)
medidas_de_resumo_dos_agentes=do.call(rbind,medidas_de_resumo_dos_agentes)
medidas_de_resumo_dos_agentes=cbind(agentes,data.frame(medidas_de_resumo_dos_agentes))
colnames(medidas_de_resumo_dos_agentes)[1]='Agente'

#Arquivo com os dados de agentes para amostras de todas as partidas já jogadas
write.csv2(medidas_de_resumo_dos_agentes,file=paste0(Sys.Date(),' - Medidas de resumo dos agentes - Todas as partidas.csv'))