##########################################################################################
#                                     HERRAMIENTAS COMPUTACIONALES                       #
#                                     SEMANA 06- PyQGis                                  #
#                                     Modelo 01                                          #
##########################################################################################

##########
# Modelos desarrollados en clase y comentarios sobre los mismos
# Docente: Gibbons Amelia
# Alumnos : Amaya Elard, Guerrero Francisco
# Fecha : 25 Jul 2021
##########
"""
Model exported as python.
Name : modelo-1
Group : 
With QGIS : 31608
"""
# En esta sección se importa/convoca a los modulos necesarios para hacer las operaciones
# con Qgis, básicamente tenemos la familia de procesamiento y el sistema de coordinadas 
# de referencia, utilizamos la funcion from para solo invocar los módulos especificos 
# de una librería


from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Creamos el algoritmo y damos inicio al Modelo 1
class Model1(QgsProcessingAlgorithm):
    # Definimos la función "initAlgorithm" con la variable "self"
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_less_than_11', 'OUTPUT_L_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    # Definimos otra función que usará a self para obtener seis layers
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # Primero corregimos las geometrías defectuosas, utilizamos el archivo langa.shp y el comando 'Fix_geo'
        alg_params = {
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['Fix-geometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['Fix-geometries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Añadimos un ID que comienza desde el 1 
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['Fix-geometries']['OUTPUT'],
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['Add_autoinc_field'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['Add_autoinc_field']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Generamos una variable que se llama 'length' cuyos valores son iguales a la cantidad de caracteres que tiene la variable NAME_PROP utilizando "fieldcalculator"
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': outputs['Add_autoinc_field']['OUTPUT'],
            'OUTPUT': parameters['Length']
        }
        outputs['Field_Calculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['Field_Calculator']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Creamos y ejecutamos el filtro para descartar las observaciones cuyo Length(NAME_PROP) es mayor a 10 empleando el "filter"
        alg_params = {
            'INPUT': outputs['Field_Calculator']['OUTPUT'],
            'OUTPUT_L_11': parameters['Output_less_than_11']
        }
        outputs['Entity_filter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_less_than_11'] = outputs['Entity_filter']['OUTPUT_L_11']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Clonamos "NAME_PROP" y la nombramos 'Inm' usando fieldcalculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Inm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': '\"NAME_PROP\"',
            'INPUT': outputs['Entity_filter']['OUTPUT_L_11'],
            'OUTPUT': parameters['Field_calc']
        }
        outputs['Field_Calculator_Clone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['Field_Calculator_Clone']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Quitamos las columnas no pertinentes usando deletecolumn
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': outputs['Field_Calculator_Clone']['OUTPUT'],
            'OUTPUT': parameters['Wldsout']
        }
        outputs['Remove_Fields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['Remove_Fields']['OUTPUT']
        return results

    def name(self):
        return 'modelo-1'

    def displayName(self):
        return 'modelo-1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
