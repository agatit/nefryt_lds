
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Event(Base_lds):
    # def __init__(self, **kwargs):
    #     super(Event, self).__init__(**kwargs)
    __tablename__ = 'Event'
    __table_args__ = {'schema': 'obj'}
    EventID = Column("EventID", Integer, primary_key=True,
                     autoincrement=True, nullable=False)
    EventDefID = Column("EventDefID", Integer, nullable=False)
    DeviceID = Column("DeviceID", Integer, nullable=False)
    BeginDate = Column("BeginDate", DateTime, nullable=False)
    AckDate = Column("AckDate", DateTime)
    EndDate = Column("EndDate", DateTime)
    UserAppID = Column("UserAppID", Integer, nullable=False)
    AppName = Column("AppName", String(128))
    DBUser = Column("DBUser", String(128))
    HostName = Column("HostName", String(128))
    ChangeDate = Column("ChangeDate", DateTime)
    SentSMS = Column("SentSMS", Boolean)
    SentEmail = Column("SentEmail", Boolean)
    AdditionalInfo = Column("AdditionalInfo", String(100))

    def __repr__(self):
        return '<Event> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
