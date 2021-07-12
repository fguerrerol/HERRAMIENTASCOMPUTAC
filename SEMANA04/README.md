# Python scrapping

#### Pasos
1) Buscar zipcodes https://www.zipcodestogo.com/Maryland/ (copiar y pegar en Excel, después en Stata - líneas 3 a 11 del do file de Stata)

2) Bajar datos de crimen de https://odn.data.socrata.com/dataset/National-Police-Department-Crime-Rates-by-Month-Ye/tt5s-y5fc (hecho en clase llamado crime.csv). Quedarse con los datos de 2015 y el estado MD, guardar como MD_crime.dta (líneas 14 a 22 del do file de Stata).

3) Merge base zipcodes y crimen (necesito ubicar los zipcodes para bajar el weather después).

4) Bajar shapefile https://hub.arcgis.com/datasets/maryland::maryland-physical-boundaries-county-boundaries-detailed/explore?location=38.802591%2C-77.268250%2C8.35 y abrir con Excel el archivo .dbf para obtener el ID de cada county. Agregar el ID (sacado del shapefile) para después poder hacer el merge (líneas 31 a 55 Stata.).

5) linea 59 de Stata suma los crimenes por county, linea 61 me genera un zipcode por county (el zipcode mediano), línea 63 me quedo con una observación por county, por año, por mes, por tipo de crimen -> MD_crime_2015.dta.

6) en la línea 68 le pido a Stata los zipcodes para poner en python para que me baje los datos de weather (usar el Inicial.py) agregando los zips, corrigiendo año y frecuency *24*.

7) línea 71 a 92 genera nueva base para que cada columna sea un crimen.

8) línea 95 a 110 junta las bases de weather quedándose con el promedio de precipitaciones por mes (línea 104) y una observación por mes/county (linea 105).

9) Merge crimen,zipcodes+weather (línea 117).

#### Consignas

Gráficos a hacer:
1) Gráfico entre precipitaciones y algún crímen per cápita. Explicar.

  En este caso se utilizó el hurto dado que por investigaciones anteriores tenía una correlacion(Aunque muy débil) con las precipitaciones a diferencia de otros tipos de crímenes, la mayoría de investigaciones no considera a la lluvia como factor determinante sino mas bien al calor como causal de crímenes.


2) Usar la variable BLACK para generar algo (gráfico o mapa) interesante (potencialmente interesante, puede que con estos datos no de nada).

En este caso se usó la proporción de personas afroamericanas con respecto a los crímenes per cápita hallando que la creencia popular que a mayor personas afroamericanas más crímenes no tiene asidero.

3) Mapa que avance en el tiempo por mes de precipitaciones y de uno de los crímenes per cápita (Properties > Temporal después de haber hecho un coropletico o heatmap. Ver: https://www.qgistutorials.com/en/docs/3/animating_time_series.html. Generar variable de date con función make_date y las variables, year, month y day. Ojo que ya existe la variable date y salta error si le ponen el mismo nombre). En heatmap, poner como transparente cuando es 0 la variable. 

En este caso se utilizaron 2 mapas temporales cloropléticos los cuales se encuentran en la carpeta Temporal-Maps.

Se entregan 3 archivos en GitHub (Poner link en la entrega de la tarea):

LaTeX con consignas 1 y 2

GIF con consigna 3.

Archivo .py (Inicial.py) para bajar lo de weather para los zipcodes correspondientes. (Se encuentra en carpeta principal), La computadora donde se realizó el archivo tiene de nombre de Usuario "apple" por ende aparece como author en el file.
