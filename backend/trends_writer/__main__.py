import datetime

from trends_writer import Writer


def get_utc_timestamp(local_timestamp):
    return datetime.utcfromtimestamp(local_timestamp).timestamp()


if __name__ == '__main__':
    t = Writer('DRIVER={SQL Server}' + \
                    ';SERVER=SERVERDB,1447' + \
                    ';DATABASE=NefrytLDSDemo' + \
                    ';UID=sa' + \
                    ';PWD=Onyks$us')
    t.run()