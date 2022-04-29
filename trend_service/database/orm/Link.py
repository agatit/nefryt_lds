
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Link(Base_lds):
    __tablename__ = 'Link'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=True, nullable=False)
    BeginNodeID = Column("BeginNodeID", Integer)
    EndNodeID = Column("EndNodeID", Integer)
    Length = Column("Length", Integer)

    def __repr__(self):
        return '<Link> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
# # schemas/orm/Link.yaml
# type: object
# x-tablename: Link
# x-schema-name: lds
# required:
#     - ID
# properties:
#     ID:
#         x-primary-key: true
#         x-autoincrement: true
#         type: integer
#         nullable: false
#         description: none
#         example: 0
#     BeginNodeID:
#         type: integer
#         description: none
#     EndNodeID:
#         type: integer
#         description: none
#     Length:
#         type: number
#         description: none
