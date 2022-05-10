
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Node(Base_lds):
    __tablename__ = 'Node'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=True, nullable=False)
    Type = Column("Type", String(6))
    TrendID = Column("TrendID", Integer, nullable=True)
    Name = Column("Name", String(50))

    def __repr__(self):
        return '<Node> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
