
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary, CHAR


class TrendParamDef(Base_lds):
    __tablename__ = 'TrendParamDef'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", CHAR(length=30), primary_key=True,
                autoincrement=True, nullable=False)
    TrendDefID = Column("TrendDefID", CHAR(30), primary_key=True, nullable=False)
    Name = Column("Name", String(30))  # , nullable=False)
    DataType = Column("DataType", String(6))

    def __repr__(self):
        return '<TrendParamDef> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
