from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from .models import Softwareproduct, Catalogue, Classified



class SoftwareproductView(ModelView):
    datamodel = SQLAInterface(Softwareproduct)
    label_columns = {'label':'Name', 'comment':'Comment'}
    list_columns = ['label', 'comment', 'coderepository', 'homepage']

class ClassifiedView(ModelView):
    datamodel = SQLAInterface(Classified)
    label_columns = {'label':'Name', }
    list_columns = ['label', 'suffix', 'catalogue_suffix']

class CatalogueView(ModelView):
    datamodel = SQLAInterface(Catalogue)
    label_columns = {'label':'Name', }
    list_columns = ['suffix', 'label', 'type']
    related_views = [ClassifiedView]

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
    ClassifiedView,
    "Classified",
    icon = "fa-folder-open-o",
    category = "Software Product",
    category_icon = "fa-envelope"
)
