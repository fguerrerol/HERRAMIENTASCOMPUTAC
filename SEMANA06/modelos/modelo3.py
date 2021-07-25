"""
Model exported as python.
Name : modelo-3
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('HFTopo', 'topo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_field_3', 'drop_field_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
        results = {}
        outputs = {}

        alg_params = {
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_3']
        }
        outputs['Fix_Geometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_3'] = outputs['Fix_Geometries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': outputs['Fix_Geometries']['OUTPUT'],
            'OUTPUT': parameters['Drop_field_3']
        }
        outputs['Remove_fields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_field_3'] = outputs['Remove_fields']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN_PREFIX': 'landq_',
            'INPUT': outputs['Remove_fields']['OUTPUT'],
            'INPUT_RASTER': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/landquality.tif',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Landq']
        }
        outputs['Z1_Stats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['Z1_Stats']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN_PREFIX': '1800_',
            'INPUT': outputs['Z1_Stats']['OUTPUT'],
            'INPUT_RASTER': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/pop/popd_1800AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1800']
        }
        outputs['Z2_Stats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['Z2_Stats']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}


        alg_params = {
            'COLUMN_PREFIX': '1900_',
            'INPUT': outputs['Z2_Stats']['OUTPUT'],
            'INPUT_RASTER': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/pop/popd_1900AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1900']
        }
        outputs['Z3_Stats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['Z3_Stats']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN_PREFIX': '2000_',
            'INPUT': outputs['Z3_Stats']['OUTPUT'],
            'INPUT_RASTER': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/pop/popd_2000AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop2000']
        }
        outputs['Z4_Stats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['Z4_Stats']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}


        alg_params = {
            'COLUMN_PREFIX': 'topo_',
            'INPUT': outputs['Z4_Stats']['OUTPUT'],
            'INPUT_RASTER': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/topo30.grd',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['HFTopo']
        }
        outputs['Z5_Stats'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HFTopo'] = outputs['Z5_Stats']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['Z5_Stats']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/output/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Export_results'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo-3'

    def displayName(self):
        return 'modelo-3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()