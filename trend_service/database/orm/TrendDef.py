
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary, CHAR


class TrendDef(Base_lds):
    __tablename__ = 'TrendDef'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", CHAR(length=30), primary_key=True,
                autoincrement=True, nullable=False)
    Name = Column("Name", String(30))
    TimeExponent = Column("TimeExponent", Integer)
    Format = Column("Format", String(30))
    UnitID = Column("UnitID", CHAR(8))

    def __repr__(self):
        return '<TrendDef> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
