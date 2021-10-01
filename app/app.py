from flask import Flask
from flask_restful import reqparse, Resource, Api
import pyodbc
import struct
from datetime import datetime

app = Flask(__name__)
api = Api(app)


class Page(Resource):


    def __init__(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('id',     type=int, required=True, help='No id given.')
        parser.add_argument('begin',  type=float, required=True, help='No begin time given.')
        parser.add_argument('end',    type=float, required=True, help='No end time given.')
        parser.add_argument('number', type=int, required=True, help='No number given.')
        self.parser = parser
        self.db_cs = 'DRIVER={SQL Server};' + \
                     ';SERVER=SERVERDB,1447' +\
                     ';DATABASE=NefrytLDSDemo' + \
                     ';UID=sa' + \
                     ';PWD=Onyks$us'
        pass


    def get_scale(self, trend_id):
        con = pyodbc.connect(self.db_cs, unicode_results=True)

        cur = con.cursor()
        cur.execute("""select * from lds.TrendDefParam WHERE TrendDefID = ? and TrendDefParamDefID
                     in (16,17,18,19) ORDER BY TrendDefParamDefID DESC""", trend_id)
        
        args = list()
        r = cur.fetchone()

        if r is None :
            return 1
            
        while r:
            args.append(float(r[2]))
            r = cur.fetchone()

        con.close()

        return (args[0] - args[1]) / (10 * (args[2] - args[3]))


    def get(self):
        args = self.parser.parse_args()

        id = args['id']
        begin_time = args['begin'] 
        end_time = args['end']
        number = args['number']
        step = (end_time -  begin_time) / number

        if begin_time >= end_time or step == 0:
            return {
                    "Error": "Arguments are invalid."
            }
        

        contact = pyodbc.connect(self.db_cs, unicode_results = True, autocommit=True)
        cursor = contact.cursor()
        cursor.execute("SELECT * FROM lds.Trend WHERE TrendDefID = ? AND Time >= ? AND Time < ? ORDER BY Time ASC",
                        (id, int(begin_time), end_time))
        row = cursor.fetchone()
        
        values = []
        cur_time = begin_time
        scale = self.get_scale(id)
        last = 0
        labels = []

        while row and cur_time < end_time:
            if int(cur_time) == row[1]:
                time = round(cur_time, 2)
                pos = int ((cur_time - int(cur_time)) * 100)
                data = struct.unpack_from('<100H', row[2])
                last = data[pos]
                values.append(last * scale)
                labels.append(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
                cur_time = cur_time + step
                if int(time) < int(cur_time):
                    row = cursor.fetchone()
                continue

            elif int(cur_time) < row[1]:
                while int(cur_time) < row[1]:
                    time = round(cur_time, 2)
                    values.append(last * scale)
                    labels.append(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
                    cur_time = cur_time + step
                continue

            row = cursor.fetchone()        


        return {
                'data':         values,
                'labels':       labels
        }, 201, {'Access-Control-Allow-Origin':'*'}
        


api.add_resource(Page, '/')


if __name__ == '__main__':
    app.run(debug=True)