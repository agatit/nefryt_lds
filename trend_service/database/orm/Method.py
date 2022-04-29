
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Method(Base_lds):
    __tablename__ = 'Method'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=False, nullable=False)
    MothedDefID = Column("MothedDefID", Integer, nullable=False)
    PipelineID = Column("PipelineID", Integer, nullable=False)
    Name = Column("Name", String(30))

    def __repr__(self):
        return '<Method> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
# # schemas/orm/Method.yaml
# type: object
# # OPEN ALCHEMY required
# x-tablename: Method
# x-schema-name: lds
# # x-foreign-key-column: MethodID <<<<
# required:
#   - ID
#   - MethodDefID
#   - PipelineID
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
#     nullable: false
#     example: 0
#   PipelineID:
#     type: integer
#     nullable: false
#     example: 0
#   Name:
#     type: string
#     example: Arthur Dent
#     pattern: ^.{0,30}
