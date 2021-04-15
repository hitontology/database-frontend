from flask_appbuilder import Model, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY, CheckConstraint
from sqlalchemy.orm import relationship, validates
import config
import enum
from sqlalchemy import create_engine
import sqlalchemy as sa

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

associativeData = [
    ["language","lang"],
    ["license","license"],
    ["operatingsystem","os"],
    ["programminglanguage","plang"],
    ["programminglibrary","lib"],
    ["interoperabilitystandard","io"],
    ["client","client"],
    ["databasesystem","db"]
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

#assoc_child = Table("swp_has_child", Model.metadata,
#    Column('parent_suffix', String(200), ForeignKey('softwareproduct.suffix')),
#    Column('child_suffix', String(200), ForeignKey('softwareproduct.suffix')),
#)

CitationHasClassified = Table("citation_has_classified",Model.metadata,
    Column('citation_suffix', String(200), ForeignKey('citation.suffix'),primary_key=True),
    Column('classified_suffix', String(200), ForeignKey('classified.suffix'),primary_key=True)
    )

SwpHasChild = Table("swp_has_child",Model.metadata,
    Column('parent_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True),
    Column('child_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)
    )

SwpHasClassified = Table("swp_has_classified",Model.metadata,
    Column('swp_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True),
    Column('classified_suffix', String(200), ForeignKey('classified.suffix'),primary_key=True)
    )

ClassifiedHasChild = Table("classified_has_child",Model.metadata,
    Column('parent_suffix', String(200), ForeignKey('classified.suffix'),primary_key=True),
    Column('child_suffix', String(200), ForeignKey('classified.suffix'),primary_key=True)
    )

class Softwareproduct(Model):
    suffix = Column(String(200), primary_key=True)
    #uri =  Column(String(229), nullable=False)
    label =  Column(String(200), nullable=False)
    comment = Column(String, nullable=True)
    coderepository = Column(String(200), nullable=True)
    homepage = Column(String(200), nullable=True)
    #databasesystems =  Column(ArrayOfEnum(Enum("MySql","PostgreSql")))
    #databasesystems = Column(Enum("MySql","PostgreSql"))
#    databasesystems =  Column(ArrayOfEnum(Enum("MySql","PostgreSql")))
    #swp_has_child_= relationship("Softwareproduct", secondary=assoc_child, backref="softwareproduct", foreign_keys="swp_has_child.child_suffix")
    #swp_has_child = relationship('SwpHasChild', backref='softwareproduct', foreign_keys="SwpHasChild.child_suffix")
    #swp_has_child = relationship('SwpHasChild', foreign_keys="swphaschildsoftwareproduct.suffix")#  backref='softwareproduct',
    classified = relationship("Classified", secondary=SwpHasClassified)
    parents = relationship("Softwareproduct", 
    secondary=SwpHasChild,
    foreign_keys = [SwpHasChild.c.parent_suffix,SwpHasChild.c.child_suffix],
    primaryjoin=suffix==SwpHasChild.c.parent_suffix,
    secondaryjoin=suffix==SwpHasChild.c.child_suffix,
    backref="children")

    @validates('comment', 'coderepository', 'homepage')
    def empty_string_to_null(self, key, value):
        return None if value=="" else value

    def __repr__(self):
        return self.label

for i in range(len(associativeData)):
    rel = relationship(associativeData[i][0], secondary = associativeTables[i])
    setattr(Softwareproduct,"swp_has_"+associativeData[i][0],rel)

class CatalogueType(enum.Enum):
    UserGroup = "UserGroup"
    ApplicationSystem = "ApplicationSystem"
    Feature = "Feature"
    EnterpriseFunction = "EnterpriseFunction"
    OrganizationalUnit = "OrganizationalUnit"

class Catalogue(Model):
    suffix = Column(String(200), primary_key=True)
    label =  Column(String(200), nullable=False)
    type = Column(sa.Enum(CatalogueType), nullable = False)

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
    citation = relationship("Citation", secondary=CitationHasClassified)
    parents = relationship("Classified", 
    secondary=ClassifiedHasChild,
    foreign_keys = [ClassifiedHasChild.c.parent_suffix,ClassifiedHasChild.c.child_suffix],
    primaryjoin=suffix==ClassifiedHasChild.c.parent_suffix,
    secondaryjoin=suffix==ClassifiedHasChild.c.child_suffix,
    backref="children")
    
    @validates('comment')
    def empty_string_to_null(self, key, value):
        return None if value=="" else value

    @validates('synonyms')
    def array_empty_string_to_null(self, key, values):
        return list(filter(lambda value: value != "", values))

    def __repr__(self):
        return self.label + " (" + self.catalogue_suffix + ")"

class Citation(Model):
    suffix = Column(String(200), primary_key=True)
    swp_suffix = Column(String(200), ForeignKey("softwareproduct.suffix"),nullable=False)
    softwareproduct = relationship("Softwareproduct")
    classified = relationship("Classified", secondary=CitationHasClassified)
    label =  Column(String(200), nullable=False)
    type = Column(sa.Enum(CatalogueType), nullable = False)

    @validates('comment')
    def empty_string_to_null(self, key, value):
        return None if value=="" else value

    def __repr__(self):
        return self.label

class FeatureSupportsFunction(Model):
    #feature_suffix = Column('feature_suffix', String(200), ForeignKey('classified_type.suffix'),CheckConstraint("type='Feature'"),primary_key=True)
    #function_suffix = Column('function_suffix', String(200), ForeignKey('classified_type.suffix'),CheckConstraint("type='EnterpriseFunction'"),primary_key=True)
    feature_suffix = Column('feature_suffix', String(200), ForeignKey('citation.suffix'),primary_key=True)
    feature = relationship('Citation', foreign_keys=[feature_suffix])
    function_suffix = Column('function_suffix', String(200), ForeignKey('citation.suffix'),primary_key=True)
    function = relationship('Citation', foreign_keys=[function_suffix])
    source = Column(String(200), nullable=True)
    
    @validates('source')
    def empty_string_to_null(self, key, value):
        return None if value=="" else value
    
