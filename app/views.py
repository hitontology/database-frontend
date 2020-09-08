from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from wtforms import StringField, FieldList

from . import appbuilder, db
from .models import Softwareproduct, Catalogue, Classified, Citation#, interoperabilitystandard

class SoftwareproductView(ModelView):
    datamodel = SQLAInterface(Softwareproduct)
    edit_columns = ['suffix','label', 'comment', 'coderepository', 'homepage']
    label_columns = {'label':'Name', 'comment':'Comment', "uri": "URI"}
    list_columns = ['suffix',"uri", 'label', 'comment', 'coderepository', 'homepage']

class ClassifiedView(ModelView):
    datamodel = SQLAInterface(Classified)
    edit_columns= ["suffix","synonyms"]
    label_columns = {'label':'Name', }
    list_columns = ['label', 'suffix', 'catalogue_suffix']
    search_exclude_columns = ['synonyms']
    add_form_extra_fields = {'synonyms': FieldList(StringField('Synonyms'), min_entries=0)}
    edit_form_extra_fields = {'synonyms': FieldList(StringField('Synonyms'), min_entries=0)}

class CatalogueView(ModelView):
    datamodel = SQLAInterface(Catalogue)
    edit_columns= ["suffix"]
    label_columns = {'label':'Name', }
    list_columns = ['suffix', 'label', 'type']
    related_views = [ClassifiedView]

class CitationView(ModelView):
    datamodel = SQLAInterface(Citation)
    edit_columns= ["suffix"]
    label_columns = {'label':'Citation', 'suffix': 'id'}
    list_columns = ['suffix', "swp_suffix", 'label']#, 'classified_suffix']
#    related_views = [SoftwareproductView,ClassifiedView]

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

#appbuilder.add_view(
#    InteroperabilitystandardView,
#    "Interoperability Standard",
#    icon = "fa-folder-open-o",
#    category = "Software Product",
#    category_icon = "fa-envelope"
#)
