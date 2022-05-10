
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, CHAR


class Trend(Base_lds):
    __tablename__ = 'Trend'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=False, nullable=False)
    Name = Column("Name", String(30))
    TrendGroupID = Column("TrendGroupID", Integer)
    TrendDefID = Column("TrendDefID", CHAR(length=30))

    def __repr__(self):
        return '<Trend> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
