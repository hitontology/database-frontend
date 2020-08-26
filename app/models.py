import enum
from flask_appbuilder import Model, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, ARRAY
from sqlalchemy.orm import relationship
import config
from sqlalchemy import create_engine

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

class Interoperabilitystandard(Base):
	__table__ = Table('interoperabilitystandard', Base.metadata,autoload=True,autoload_with=engine)
	def __repr__(self):
		return self.label

association_table = Table('swp_has_interoperabilitystandard', Base.metadata,
	Column('swp_suffix', String(200), ForeignKey('softwareproduct.suffix')),
	Column('io_suffix', String(200), ForeignKey('interoperabilitystandard.suffix'))
	)

#class SwpHasInteroperabilitystandard(Model):
#	swp_suffix = Column('swp_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)
#	io_suffix = Column('io_suffix', String(200), ForeignKey('interoperabilitystandard.suffix'),primary_key=True)

class SwpHasChild(Model):
	parent_suffix = Column('parent_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)
	child_suffix = Column('child_suffix', String(200), ForeignKey('softwareproduct.suffix'),primary_key=True)

class Softwareproduct(Model):
    suffix = Column(String(200), primary_key=True)
    label =  Column(String(200), nullable=False)
    comment = Column(String, nullable=True)
    coderepository = Column(String(200), nullable=True)
    homepage = Column(String(200), nullable=True)
    swp_has_child = relationship('SwpHasChild', backref='softwareproduct', foreign_keys="SwpHasChild.child_suffix")
    swp_has_interoperabilitystandard = relationship('Interoperabilitystandard', secondary = association_table)

    def __repr__(self):
        return self.label

class Catalogue(Model):
    suffix = Column(String(200), primary_key=True)
    label =  Column(String(200), nullable=False)
    type =  Column(String(200), nullable=False)

    def __repr__(self):
        return self.label

class Classified(Model):
    suffix = Column(String(200), primary_key=True)
    catalogue_suffix = Column(String(200), ForeignKey("catalogue.suffix"))
    catalogue = relationship("Catalogue")
    label =  Column(String(200), nullable=False)
    comment = Column(String, nullable=True)
    dct_source = Column(String(200), nullable=True)
    # synonyms = Column()

    def __repr__(self):
        return self.label

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
