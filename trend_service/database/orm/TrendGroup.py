
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary


class TrendGroup(Base_lds):
    __tablename__ = 'TrendGroup'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=True, nullable=False)
    Name = Column("Name", String(100))  # , nullable=False)
    AnalisisOnly = Column("AnalisisOnly", Boolean)

    def __repr__(self):
        return '<TrendGroup> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_

# schemas/orm/TrendGroup.yaml
# type: object
# x-tablename: TrendGroup
# x-schema-name: lds
# required:
#   - ID
#   - Name
#   - AnalisisOnly
# properties:
#   ID:
#     x-primary-key: true
#     x-autoincrement: true
#     type: integer
#     description: none
#     example: 0
#   Name:
#     type: string
#     pattern: ^.{0,100}
#     description: none
#   AnalisisOnly:
#     type: boolean
#     description: none
