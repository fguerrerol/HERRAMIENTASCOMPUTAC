## Herrameintas computacionales 
#Desarrollado por Amaya Elard y Guerrero Francisco

#Load Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")

#Cambiar directorio
#Importante cambiar directorio para apuntar a la carpeta donde se va a trabajar
#setwd("/Users/apple/Documents/MEcon/Trim2/Herramientas/Semana-05/Trabajo")

#Check working directory
getwd()


#Leemos los csv
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

#Recabamos datos básicos de los respectivos CSV
str(df)
str(df2)
str(df3)


#A continuacion las líneas siguiente de código elaboraran los gráficos
# Estos gráficos están en el mismo orden que lso gráficos representados en el LaTEX/ PDF

#Gráfico 1
## Gráfico antiguo
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point()

p + facet_wrap(~Country)

## Gráfico nuevo
dfs <- subset(df,Country %in% c("Germany","India","China","United States"))
var1<-"Electricity_consumption_per_capita"
var2<-"gdp_per_capita"
p <- ggplot(dfs, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita))+geom_point(color="Red") 
  
p +stat_smooth(method=loess,color="blue")+facet_wrap(~Country,scales="free")+xlab('GDP per capita (US Dollars)')+ylab('Electricity consumption per cápita (KWh)')+
  theme(panel.background = element_rect(fill = "white",
                                        colour = "white",
                                        size = 0.5, linetype = "solid"),
        panel.grid=element_blank(),
        plot.title.position = "plot",
        plot.title = element_text(color = "white", size = 12, face = "bold"),
        plot.subtitle = element_text(color="cyan", size = 9, face="bold"),
        axis.title.x = element_text(colour = "white"),
        axis.text.x = element_text(colour = "white"),
        axis.title.y = element_text(colour = "white"),
        axis.text.y = element_text(colour = "white"),
        plot.background = element_rect(fill = "darkblue"),
        legend.position="bottom",
        legend.title = element_text(colour = "white"),
        legend.text = element_text(colour = "white"),
        legend.background = element_rect(fill = "dodgerblue3") )


#Gráfico 2

## Gráfico antiguo


dfn <- subset(HollywoodMovies, Genre %in% c("Action","Adventure","Comedy","Drama","Romance")
              & LeadStudio %in% c("Fox","Sony","Columbia","Paramount","Disney"))
p1 <- ggplot(dfn,aes(Genre,WorldGross)) 
p2 <- p1+geom_bar(stat="Identity",aes(fill=LeadStudio),position="dodge")
p2



## Gráfico nuevo
p4 <- p2+ggtitle(label="Cummulated movie's networth",
                 subtitle = "By Genre and LeadStudio")+scale_y_continuous(breaks=seq(0,3000,500))+
  theme(panel.background = element_rect(fill = "dodgerblue4",
                                        colour = "lightblue",
                                        size = 0.5, linetype = "solid"),
        panel.grid=element_blank(),
        plot.title.position = "plot",
        plot.title = element_text(color = "white", size = 12, face = "bold"),
        plot.subtitle = element_text(color="cyan", size = 9, face="bold"),
        axis.title.x = element_text(colour = "white"),
        axis.text.x = element_text(colour = "white"),
        axis.title.y = element_text(colour = "white"),
        axis.text.y = element_text(colour = "white"),
        plot.background = element_rect(fill = "dodgerblue4"),
        legend.position="bottom",
        legend.title = element_text(colour = "grey60"),
        legend.text = element_text(colour = "white"),
        legend.background = element_rect(fill = "dodgerblue4") )
p4 + scale_fill_brewer(palette="Spectral")

#Gráfico 3

## Gráfico antiguo
pd1 <- ggplot(df,aes(x=BMI_male,y=BMI_female))

pd3 <- pd1+geom_point(aes(colour=Country),size=1)+
  scale_colour_brewer(palette="Paired")
pd4 <- pd3+theme(axis.title=element_text(size=15,color="cadetblue4",
                                         face="bold"),
                 plot.title=element_text(color="cadetblue4",size=18,
                                         face="bold.italic"),
                 panel.background = element_rect(fill="azure",color="black"),
                 panel.grid=element_blank(),
                 legend.position="bottom",
                 legend.justification="left",
                 legend.title = element_blank(),
                 legend.key = element_rect(color=3,fill="gray97")
)+
  xlab("BMI Male")+
  ylab("BMI female")+
  ggtitle("BMI female vs BMI Male")
pd4

## Gráfico nuevo

pd4 <- pd3+theme(axis.title=element_text(size=15,color="cadetblue4",
                                         face="bold"),
                 plot.title=element_text(color="cadetblue4",size=18,
                                         face="bold.italic"),
                 panel.background = element_rect(fill="seashell1"),
                 panel.grid=element_blank(),
                 legend.position=c(.75,.2),
                 legend.justification="left",
                 legend.title = element_blank(),
                 plot.background = element_rect(fill='paleturquoise2'),
                 legend.key = element_rect(color=3,fill="gray97")
)+
  xlab("BMI Male")+
  ylab("BMI female")+
  ggtitle("BMI female vs BMI Male")
pd4

#End


