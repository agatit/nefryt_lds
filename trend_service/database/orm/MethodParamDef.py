
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class MethodParamDef(Base_lds):
    __tablename__ = 'MethodParamDef'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=False, nullable=False)
    MethodDefID = Column("MethodDefID", Integer)
    Name = Column("Name", String(30))
    DataType = Column("DataType", String(6))

    def __repr__(self):
        return '<MethodParamDef> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
# # schemas/orm/MethodParamDef.yaml
# type: object
# x-tablename: MethodParamDef
# x-schema-name: lds
# required:
#   - ID
# properties:
#   ID:
#     x-primary-key: true
#     x-autoincrement: false
#     type: integer
#     nullable: false
#     description: none
#     example: 0
#   MethodDefID:
#     type: integer
#     description: none
#   Name:
#     type: string
#     # any char with length 0-30 only
#     pattern: ^.{0,30}
#     description: none
#   DataType:
#     type: string
#     # any char with length 0-6 only
#     pattern: ^.{0,6}
#     description: none
