Parte 2 del trabajo.\
  Contenidos.-
  
  -Código R 
  
  Cambios en el archivo con respecto al archivo .R original, se adicionó la línea 123 \
  lnd@data$Crimep1000 = (lnd@data$CrimeCount/strtoi(lnd@data$Pop_2001))*1000 \
   la cual genera el vector Crime 1000 dentro del objeto data,  (Aquí encontramos el criemn y lo dividimos sobre la población total(La cual es pasada a números enteros dado que estaba como cadena ) y lo multiplicamos por 1000, luego reemplazamos en las instancias correspondiente para gráficar tant con gg plot como con tmap, usando la distribución por cuantiles donde se es posible. (Línea 127 uso de fill.style =quantile en qtm)
  
  -Código STATA \
  Cambios en el archivo con respecto al archivo .do original, se incluyó en la línea 89 la adición de la variable Cper1000, la cual dividía a un crimen específico por la población total y se multiplicaba por 1000, luego esta variable reemplazo a la varaible anterior que era solo cantidad de crimen, para generar el gráfico
  
  

