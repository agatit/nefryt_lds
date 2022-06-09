import struct
import time
from typing import List

from sqlalchemy import alias, select, delete
from trends_writer import session
from database.models import lds


def insert(trend_id, raw_data):
    
    try:
        
        pack = struct.pack('<100h', *raw_data)
        
        now = int(time.time() * 1000)
        
        insert_stmt = insert(lds.TrendData).values(
            TrendID = trend_id,
            Time = now,
            Data = pack
        )
        
        session.execute(insert_stmt)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
