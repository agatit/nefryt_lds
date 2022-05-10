
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary, CHAR


class TrendParam(Base_lds):
    __tablename__ = 'TrendParam'
    __table_args__ = {'schema': 'lds'}
    TrendParamDefID = Column("TrendParamDefID",
                             CHAR(length=30), primary_key=True, autoincrement=False, nullable=False)
    TrendID = Column("TrendID", Integer, primary_key=True, autoincrement=False, nullable=False)
    Value = Column("Value", String(30))

    def __repr__(self):
        return '<TrendParam> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
