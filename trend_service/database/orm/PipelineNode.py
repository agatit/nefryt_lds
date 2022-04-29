
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class PipelineNode(Base_lds):
    __tablename__ = 'PipelineNode'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=False, nullable=False)
    NodeID = Column("NodeID", Integer)
    First = Column("First", Boolean)

    def __repr__(self):
        return '<PipelineNode> ' + str(self.columns_to_dict())
    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
# # schemas/orm/PipelineNode.yaml
# type: object
# x-tablename: PipelineNode
# x-schema-name: lds
# required:
#   - ID
#   - NodeID
# properties:
#   ID:
#     x-primary-key: true
#     x-autoincrement: false
#     type: integer
#     nullable: false
#     description: none
#     example: 0
#   NodeID:
#     x-primary-key: true
#     type: integer
#     description: none
#   First:
#     type: boolean
#     description: none
