from flask_appbuilder import Model, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, ARRAY
from sqlalchemy.orm import relationship, validates
import config
from sqlalchemy import create_engine

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

associativeData = [
    ["language","lang"],
    ["license","license"],
    ["operatingsystem","os"],
    ["programminglanguage","plang"],
    ["programminglibrary","lib"],
    ["interoperabilitystandard","io"],
    ]

def repr(self):
        return self.label

clazzes = []
for data in associativeData:
   clazzes.append(type(data[0], (Base, ),
   {
	"__table__": Table(data[0], Base.metadata,autoload=True,autoload_with=engine),
        "__repr__": repr
   }))

associativeTables = list(map(lambda d: Table('swp_has_'+d[0], Base.metadata,
	Column('swp_suffix', String(200), ForeignKey('softwareproduct.suffix')),
	Column(d[1]+'_suffix', String(200), ForeignKey(d[0]+'.suffix'))
	),
        associativeData))

class SwpHasChild(Model):
    parent_suffix = Column('parent_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)
    child_suffix = Column('child_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)
#    def __repr__(self):
#        return .label

class Softwareproduct(Model):
    suffix = Column(String(200), primary_key=True)
    label =  Column(String(200), nullable=False)
    comment = Column(String, nullable=True)
    coderepository = Column(String(200), nullable=True)
    homepage = Column(String(200), nullable=True)
    #databasesystems =  Column(ArrayOfEnum(Enum("MySql","PostgreSql")))
    #databasesystems = Column(Enum("MySql","PostgreSql"))
#    databasesystems =  Column(ArrayOfEnum(Enum("MySql","PostgreSql")))
#    clients =  Column(ARRAY(Enum("Mobile","WebBased","Native")), nullable=False)
    swp_has_child = relationship('SwpHasChild', backref='softwareproduct', foreign_keys="SwpHasChild.child_suffix")

    @validates('comment', 'coderepository', 'homepage')
    def empty_string_to_null(self, key, value):
        return None if value=="" else value

    def __repr__(self):
        return self.label

for i in range(len(associativeData)):
    rel = relationship(associativeData[i][0], secondary = associativeTables[i])
    setattr(Softwareproduct,"swp_has_"+associativeData[i][0],rel)

class Catalogue(Model):
    suffix = Column(String(200), primary_key=True)
    label =  Column(String(200), nullable=False)
    type =  Column(Enum("UserGroup","ApplicationSystem","Feature","EnterpriseFunction","OrganizationalUnit"), nullable=False)

    def __repr__(self):
        return self.label

class Classified(Model):
    suffix = Column(String(200), primary_key=True)
    catalogue_suffix = Column(String(200), ForeignKey("catalogue.suffix"))
    catalogue = relationship("Catalogue")
    label =  Column(String(200), nullable=False)
    comment = Column(String, nullable=True)
    dct_source = Column(String(200), nullable=True)
    synonyms = Column(ARRAY(String(200)))

    def __repr__(self):
        return self.label

class Citation(Model):
    suffix = Column(String(200), primary_key=True)
    swp_suffix = Column(String(200), ForeignKey("softwareproduct.suffix"),nullable=False)
    softwareproduct = relationship("Softwareproduct")
    #classified_suffix = Column(String(200), ForeignKey("classified.suffix"))
    #classified = relationship("Classified" )
    label =  Column(String(200), nullable=False)

    def __repr__(self):
        return self.label

