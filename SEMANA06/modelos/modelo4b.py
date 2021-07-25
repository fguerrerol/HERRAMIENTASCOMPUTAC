##########################################################################################
#                                     HERRAMIENTAS COMPUTACIONALES                       #
#                                     SEMANA 06- PyQGis                                  #
#                                     Modelo 04-B                                        #
##########################################################################################

##########
# Modelos desarrollados en clase y comentarios sobre los mismos
# Docente: Gibbons Amelia
# Alumnos : Amaya Elard, Guerrero Francisco
# Fecha : 25 Jul 2021
##########

"""
Model exported as python.
Name : modelo-4b
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Centroid-Country', 'pais_centroide', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'Extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ExtractVertices', 'extract vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_country', 'fixgeo_pais', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('CentroidsNearestCoastJoined', 'centroids nearest coast joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('NearestCatAdjustDropfields', 'nearest cat adjust dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('csv-export', 'csvout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroid-w-coord', 'centroid-w-coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}
        
        alg_params = {
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['Fix-Geo-Coast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['Fix-Geo-Coast']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'INPUT': '/Users/apple/Documents/MEcon/Trim2/Herramientas/SEMANA06/data/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_country']
        }
        outputs['Fix-Geo-Countries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_country'] = outputs['Fix-Geo-Countries']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) costas
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': outputs['Fix-Geo-Coast']['OUTPUT'],
            'OUTPUT': parameters['Coastout']
        }
        outputs['Drop-fields-coast'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['Drop-fields-coast']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['Fix-Geo-Countries']['OUTPUT'],
            'OUTPUT': parameters['Centroid-Country']
        }
        outputs['Centroids-Country'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroid-Country'] = outputs['Centroids-Country']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['Centroids-Country']['OUTPUT'],
            'OUTPUT': parameters['Centroid-w-coord']
        }
        outputs['Add-Geometry-Attribs'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroid-w-coord'] = outputs['Add-Geometry-Attribs']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': outputs['Add-Geometry-Attribs']['OUTPUT'],
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['RemoveFieldsCentroid'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['RemoveFieldsCentroid']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['RemoveFieldsCentroid']['OUTPUT'],
            'from_output': '././nearout',
            'from_type': [0,1,3],
            'output': './distout',
            'to': outputs['Drop-fields-coast']['OUTPUT'],
            'to_column': '',
            'to_type': [0,1,3],
            'upload': [0],
            'from_output': QgsProcessing.TEMPORARY_OUTPUT,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'attribute($currentfeature,\'cat\')-1',
            'INPUT': outputs['Vdistance']['from_output'],
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['Field-Calc-Adjust-Cat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['Field-Calc-Adjust-Cat']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) nearest cat
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['Field-Calc-Adjust-Cat']['OUTPUT'],
            'OUTPUT': parameters['NearestCatAdjustDropfields']
        }
        outputs['Drop-fields-nearest-cat'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['NearestCatAdjustDropfields'] = outputs['Drop-fields-nearest-cat']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': outputs['RemoveFieldsCentroid']['OUTPUT'],
            'INPUT_2': outputs['Drop-fields-nearest-cat']['OUTPUT'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['CentroidsNearestCoastJoined']
        }
        outputs['Join-Attribs-by-field-of-Y-centroid'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CentroidsNearestCoastJoined'] = outputs['Join-Attribs-by-field-of-Y-centroid']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9','ADMIN_2','ISO_A3_2'],
            'INPUT': outputs['Join-Attribs-by-field-of-Y-centroid']['OUTPUT'],
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['Drop-fields-cent-coast-joint'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['Drop-fields-cent-coast-joint']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': outputs['Vdistance']['output'],
            'INPUT_2': outputs['Drop-fields-cent-coast-joint']['OUTPUT'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['Join-Attrib-by-Field-Value'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['Join-Attrib-by-Field-Value']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'INPUT': outputs['Join-Attrib-by-Field-Value']['OUTPUT'],
            'OUTPUT': parameters['ExtractVertices']
        }
        outputs['Extract-Vertixes'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ExtractVertices'] = outputs['Extract-Vertixes']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD': 'distance',
            'INPUT': outputs['Extract-Vertixes']['OUTPUT'],
            'OPERATOR': 2,
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['Extract_by_attrib'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['Extract_by_attrib']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': outputs['Extract_by_attrib']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['Fielc-calc-cent-lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['Fielc-calc-cent-lat']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': outputs['Fielc-calc-cent-lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['Field-calc-cent-lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['Field-calc-cent-lon']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': outputs['Field-calc-cent-lon']['OUTPUT'],
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['Remove-Fields-Centroids-lat-lon'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['Remove-Fields-Centroids-lat-lon']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['Remove-Fields-Centroids-lat-lon']['OUTPUT'],
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['Add-attribs-of-geo-coast'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['Add-attribs-of-geo-coast']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': outputs['Add-attribs-of-geo-coast']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['Field_calculator-Coast-lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['Field_calculator-Coast-lat']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': outputs['Field_calculator-Coast-lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['Field-calc-coast-lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['Field-calc-coast-lon']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['Field-calc-coast-lon']['OUTPUT'],
            'OUTPUT': parameters['csv-export']
        }
        outputs['Remove_Fields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['csv-export'] = outputs['Remove_Fields']['OUTPUT']
        return results

    def name(self):
        return 'modelo-4b'

    def displayName(self):
        return 'modelo-4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
