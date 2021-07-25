##########################################################################################
#                                     HERRAMIENTAS COMPUTACIONALES                       #
#                                     SEMANA 06- PyQGis                                  #
#                                     Modelo 02                                          #
##########################################################################################

##########
# Modelos desarrollados en clase y comentarios sobre los mismos
# Docente: Gibbons Amelia
# Alumnos : Amaya Elard, Guerrero Francisco
# Fecha : 25 Jul 2021
##########


"""
Model exported as python.
Name : modelo-2
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Model2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Reproyeccion
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/suit/suit/hdr.adf',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        outputs['Reproyeccion'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['Reproyeccion']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Extraccion
        alg_params = {
            'INPUT': outputs['Reproyeccion']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['Extract_Projection'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo-2'

    def displayName(self):
        return 'modelo-2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
