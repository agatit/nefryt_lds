import struct
import time
from typing import List

import sqlalchemy as sql

from ..database import Session, engine, orm


def insert(trend_id, raw_data):
    
    try:
        
        pack = struct.pack('<100h', *raw_data)
        
        now = int(time.time() * 1000)
        
        insert_stmt = sql.insert(orm.TrendData).values(
            TrendID = trend_id,
            Time = now,
            Data = pack
        )
        
        Session.execute(insert_stmt)
        Session.commit()
    except Exception as e:
        print(e)
        Session.rollback()
        raise
