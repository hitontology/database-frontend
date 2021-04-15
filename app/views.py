from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from wtforms import StringField, FieldList

from . import appbuilder, db
from .models import Softwareproduct, Catalogue, Classified, Citation, FeatureSupportsFunction#, interoperabilitystandard

class ClassifiedView(ModelView):
    datamodel = SQLAInterface(Classified)
    label_columns = {'label':'Name', }
    list_columns= ["suffix","label", "comment", "dct_source", "catalogue", "synonyms", "citation","parents","children"]
    show_columns= ["suffix","label", "comment", "dct_source", "catalogue", "synonyms", "citation","parents","children"]
    edit_columns= ["suffix","label", "comment", "dct_source", "catalogue", "synonyms", "citation","parents","children"]
    add_columns= ["suffix","label", "comment", "dct_source", "catalogue", "synonyms", "citation","parents","children"]
    search_exclude_columns = ['synonyms']
    add_form_extra_fields = {'synonyms': FieldList(StringField('Synonyms'), min_entries=5)}
    edit_form_extra_fields = {'synonyms': FieldList(StringField('Synonyms'), min_entries=5)}

class CatalogueView(ModelView):
    datamodel = SQLAInterface(Catalogue)
    edit_columns= ["suffix","label","type"]
    label_columns = {'label':'Name', 'suffix': 'ID'}
    list_columns = ['suffix', 'label', 'type']
    related_views = [ClassifiedView]

class CitationView(ModelView):
    datamodel = SQLAInterface(Citation)
    label_columns = {'label':'Citation', 'suffix': 'ID'}
    add_columns = ['softwareproduct', "label", "suffix", "classified","type"]
    edit_columns = ['softwareproduct', "label", "suffix","classified","type"]
    show_columns = ['softwareproduct', "label", "suffix","classified","type"]
    list_columns = ['softwareproduct', "label", "suffix","classified","type"]
    related_views = [ClassifiedView]

class FeatureSupportsFunctionView(ModelView):
    datamodel = SQLAInterface(FeatureSupportsFunction)
    label_columns = {'feature':'Feature', 'function': 'Function'}
    add_columns = ['feature', 'function', 'source']
    edit_columns = ['feature', 'function', 'source']
    show_columns = ['feature', 'function', 'source']
    list_columns = ['feature', 'function', 'source']
    related_views = [ClassifiedView]

class SoftwareproductView(ModelView):
    datamodel = SQLAInterface(Softwareproduct)
    #label_columns = {'label':'Name', 'comment':'Comment', "uri": "URI", 'suffix': 'ID'}
    label_columns = {'label':'Name', 'comment':'Comment', 'suffix': 'ID', "swp_has_client": "Clients", "swp_has_databasesystem": "Databases"}
    #list_columns = ['label', 'comment', 'coderepository', 'homepage', 'suffix', 'uri']
    list_columns = ['label', 'comment', 'coderepository', 'homepage', 'suffix','swp_has_client',"swp_has_databasesystem"]
    #show_columns = ['suffix','label','comment','coderepository','homepage','swp_has_client','swp_has_language','swp_has_license','swp_has_operatingsystem', 'swp_has_programminglanguage', 'swp_has_interoperabilitystandard', 'parents','children']
    edit_columns = ['suffix','label','comment','coderepository','homepage','classified','swp_has_language','swp_has_license','swp_has_operatingsystem', 'swp_has_programminglanguage', 'swp_has_interoperabilitystandard', 'swp_has_client', 'swp_has_databasesystem', 'parents','children']
    add_columns = ['suffix','label','comment','coderepository','homepage','classified','swp_has_language','swp_has_license','swp_has_operatingsystem', 'swp_has_programminglanguage', 'swp_has_interoperabilitystandard', 'swp_has_client', 'swp_has_databasesystem', 'parents','children']
    show_columns = ['suffix','label','comment','coderepository','homepage','classified','swp_has_language', 'swp_has_license','swp_has_operatingsystem', 'swp_has_programminglanguage', 'swp_has_interoperabilitystandard', 'swp_has_client', 'swp_has_databasesystem', 'parents','children']
    #add_form_extra_fields = {'swp_has_client': FieldList(EnumField('Client'), min_entries=5)}
    #edit_form_extra_fields = {'swp_has_client': FieldList(EnumField('Client'), min_entries=5)}
    related_views = [CitationView]

setattr(ClassifiedView,"related_views",[CitationView]) # not defined yet when added in the class definition

#class InteroperabilitystandardView(ModelView):
#    datamodel = SQLAInterface(interoperabilitystandard)
#    label_columns = {'label':'Name'}
#    list_columns = ['suffix', 'label', 'comment']#, 'sourceuris']
#    related_views = [SoftwareproductView]

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


#db.create_all()

appbuilder.add_view(
    SoftwareproductView,
    "Software Product",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    CatalogueView,
    "Catalogue",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    CitationView,
    "Citation",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    ClassifiedView,
    "Classified",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    FeatureSupportsFunctionView,
    "FeatureSupportsFunction",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)

#appbuilder.add_view(
#    InteroperabilitystandardView,
#    "Interoperability Standard",
#    icon = "fa-folder-open-o",
#    category = "Software Product",
#    category_icon = "fa-envelope"
#)
