from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Pipeline(Base_lds):
    __tablename__ = 'Pipeline'
    __table_args__ = {'schema': 'lds'}
    ID = Column("ID", Integer, primary_key=True,
                autoincrement=True, nullable=False)
    Name = Column("Name", String(30))
    BeginPos = Column("BeginPos", Integer)

    def __repr__(self):
        return '<Pipeline> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
