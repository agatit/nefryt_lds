
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary


class TrendData(Base_lds):
    __tablename__ = 'TrendData'
    __table_args__ = {'schema': 'lds'}
    TrendID = Column("TrendID", Integer, primary_key=True,
                     autoincrement=False, nullable=False)
    Time = Column("Time", DateTime, primary_key=True,
                  nullable=False, autoincrement=False)
    Data = Column("Data", LargeBinary, nullable=False)

    def __repr__(self):
        return '<TrendData> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
# # schemas/orm/TrendData.yaml
# type: object
# x-tablename: TrendData
# x-schema-name: lds
# required:
#   - TrendID
#   - Time
#   - Data
# properties:
#   TrendID:
#     x-primary-key: true
#     x-autoincrement: false
#     type: integer
#     nullable: false
#     description: none
#     example: 0
#   Time:
#     x-primary-key: true
#     x-autoincrement: false
#     type: integer
#     format: int64
#     nullable: false
#     description: none
#   Data:
#     type: string
#     format: binary
#     nullable: false
#     maxLength: 200
#     # pattern: ^.{0,200}
