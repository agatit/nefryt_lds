from flask import Flask
from flask_restful import reqparse, Resource, Api
import pyodbc
import struct

app = Flask(__name__)
api = Api(app)

def scale_values(values, scale):
    return list( map(lambda x: x * scale * 1/10, values))


class Page(Resource):


    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',     type=int, required=True, help='No id given.')
        parser.add_argument('begin',  type=int, required=True, help='No begin time given.')
        parser.add_argument('end',    type=int, required=True, help='No end time given.')
        parser.add_argument('number', type=int, required=True, help='No number given.')
        self.parser = parser
        self.db_cs = 'DRIVER={SQL Server}' + \
                     ';SERVER=192.168.18.11' + \
                     ';DATABASE=NefrytLDS_NEW' + \
                     ';UID=sa' + \
                     ';PWD=Onyks$us'
        pass
    
    def get_scale(self, trend_id):
        con = pyodbc.connect(self.db_cs, unicode_results=True)

        cur = con.cursor()
        cur.execute("select * from lds.TrendDefParam WHERE TrendDefID = ? and TrendDefParamDefID in (16,17,18,19) ORDER BY TrendDefParamDefID DESC", trend_id)
        
        args = list()
        r = cur.fetchone()

        if r is None :
            return 1
            
        while r:
            args.append(float(r[2]))
            r = cur.fetchone()

        con.close()

        return (args[0] - args[1]) / (args[2] - args[3])


    def get(self):
        args = self.parser.parse_args()
        contact = pyodbc.connect(self.db_cs, unicode_results = True, autocommit=True)
        cursor = contact.cursor()

        id = args['id']
        begin_time = args['begin']
        end_time = args['end']
        number = args['number']

        cursor.execute("SELECT * FROM lds.Trend WHERE TrendDefID = ? AND Time >= ? AND Time <= ? ORDER BY Time ASC", (id, begin_time, end_time))
        row = cursor.fetchone()
        
        cur_time = begin_time
        step = (end_time - begin_time + 1) / number 
        values = []
        times = []
        scale = self.get_scale(id)

        while row and cur_time <= end_time:

            if row[1] == round(cur_time):
                data = struct.unpack('<100H', row[2])
                values.append(scale_values(data, scale))
                times.append(round(cur_time))
                cur_time = cur_time + step

            elif row[1] > round(cur_time):
                data = 100 * [0]

                while row[1] > round(cur_time):
                    values.append(data)
                    times.append(round(cur_time))
                    cur_time = cur_time + step

                continue

            row = cursor.fetchone()


        return {'id':     id,
                'begin':  begin_time,
                'end':    end_time,
                'number': len(values),
                'values': values,
                'times': times
                }


api.add_resource(Page, '/')


if __name__ == '__main__':
    app.run(debug=True)