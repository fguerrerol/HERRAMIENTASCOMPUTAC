##########################################################################################
#                                     HERRAMIENTAS COMPUTACIONALES                       #
#                                     SEMANA 06- PyQGis                                  #
#                                     Modelo 04-C                                         #
##########################################################################################

##########
# Modelos desarrollados en clase y comentarios sobre los mismos
# Docente: Gibbons Amelia
# Alumnos : Amaya Elard, Guerrero Francisco
# Fecha : 25 Jul 2021
##########

"""
Model exported as python.
Name : modelo-4c
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Model4c(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Quitar campo(s) - countries_drop_fields
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9','ADMIN_2','ISO_A3_2'],
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Countries_drop_fields']
        }
        outputs['Drop_fields_countries'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_drop_fields'] = outputs['Drop_fields_countries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'INPUT': outputs['Drop_fields_countries']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'),
            'OUTPUT': parameters['Countries_reprojected']
        }
        outputs['Countries_reprojected'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['Countries_reprojected']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'INPUT': outputs['Countries_reprojected']['OUTPUT'],
            'OUTPUT': parameters['Countries_fixgeo']
        }
        outputs['Countries_fixedgeo'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['Countries_fixedgeo']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry)/1000000',
            'INPUT': outputs['Countries_fixedgeo']['OUTPUT'],
            'OUTPUT': parameters['Areas_out']
        }
        outputs['Field-Calc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['Field-Calc']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['Field-Calc']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06//areas.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExportFeatures'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo-4c'

    def displayName(self):
        return 'modelo-4c'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4c()
