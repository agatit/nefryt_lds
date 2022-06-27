import logging
import struct
import time
import sys
from typing import List

from sqlalchemy import select, insert, and_

from trends_writer.db import session
from database import lds

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from . import TrendQuick, TrendBase, TrendMean, TrendDeriv, TrendDiff

class TrendBaseMeta(type):
    _objects = {}

    def __call__(cls, key, *args, **kwargs):
        if key in cls._objects:
            return cls._objects[key]
        else:
            obj = super().__call__(key, *args, **kwargs)
            cls._objects[key] = obj
            return obj


class TrendBase(metaclass=TrendBaseMeta):

    def __init__(self, id: int, parent_id: int = None):
        self.id = id
        self.children: List[TrendBase] = []
        self.params = {}
        self.output_size = 100
        
        self._read_params()
        self._read_children()
        logging.info(f"Trend {self.__class__.__name__} ({self.id}) initialized: params={self.params}")    


    def update(self, data: List[int], timestamp: int, parent_id: int = None):

        # TODO: threaded implementation

        logging.debug(f"Trend {self.__class__.__name__} ({self.id}) processing...")
        
        self._save(data, timestamp) 

        # process children
        for child in self.children:
            try:          
                child.update(data, timestamp, self.id)            
            except Exception as e:
                logging.exception(f"Trend {self.__class__.__name__} ({self.id}) child {child.__class__.__name__} ({child.id}) update error: {e}", exc_info=True)               


    def _read_params(self):
        stmt = select([lds.TrendParamDef, lds.TrendParam]) \
            .select_from(lds.Trend) \
            .join(lds.TrendDef, lds.Trend.TrendDefID == lds.TrendDef.ID) \
            .join(lds.TrendParamDef, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID) \
            .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.Trend.ID == lds.TrendParam.TrendID)) \
            .where(lds.Trend.ID == self.id)

        self.params = {}
        for tpd, tp in session.execute(stmt):
            self.params[tpd.ID.strip()] = tp.Value    


    def _read_children(self):

        trend_classes = {
            'QUICK': 'TrendQuick',
            'MEAN': 'TrendMean',
            'DERIV': 'TrendDeriv',
            'DIFF': 'TrendDiff'
        }

        stmt = select([lds.Trend, lds.TrendDef]) \
            .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) \
            .join(lds.TrendParam, lds.TrendParam.TrendID == lds.Trend.ID) \
            .join(lds.TrendParamDef, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID)) \
            .where(and_(lds.TrendParamDef.DataType == 'TREND', lds.TrendParam.Value == self.id))

        for trend, trend_def in session.execute(stmt):
            trend_class = getattr(sys.modules["trends_writer.trends"], trend_classes[trend_def.ID.strip()])
            trend = trend_class(trend.ID, self.id)
            self.children.append(trend)


    def _save(self, data, timestamp):
        
        try:
            if timestamp is None:
                timestamp = int(time.time())
            packed_data = struct.pack('<100h', *data)

            insert_stmt = insert(lds.TrendData).values(
                TrendID=self.id,
                Time=timestamp,
                Data=packed_data
            )
            session.execute(insert_stmt)
            session.commit()

            logging.debug(f"Trend {self.__class__.__name__} ({self.id}) saved for {timestamp}") 
        except Exception as e:            
            session.rollback()
            raise(e)




