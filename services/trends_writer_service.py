import socket

import win32serviceutil

import servicemanager
import win32event
import win32service
import logging

from trends_writer import TrendWriter

from logging.handlers import RotatingFileHandler

path = "C:/nefryt_lds"

class TrendsWriterService(win32serviceutil.ServiceFramework):

    _svc_name_ = 'TrendsWriterService'
    _svc_display_name_ = 'Trends Writer Service'
    _svc_description_ = 'Service for Trends Writer.'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        try:
            handler = RotatingFileHandler(path + '/log/' + self._svc_name_ + '.log',
                                            maxBytes=5242880, backupCount=5)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                                            "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logging.basicConfig(level=logging.DEBUG, handlers=[handler])
            logging.info(f"{self._svc_name_} created.")

            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
        except:
            logging.fatal(f"{self._svc_name_} creation failed.")

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        logging.info(f"Trends Writer started as service {self._svc_name_}.")
        self.writer = TrendWriter('DRIVER={SQL Server};SERVER=192.168.18.11' + \
                     ';DATABASE=NefrytLDS_NEW' + \
                     ';UID=sa' + \
                     ';PWD=Onyks$us')

    def stop(self):
        self.writer.stop()
        logging.info(f"Trends Writer stopped as service {self._svc_name_}.")


    def main(self):
        self.writer.run()

if __name__ == '__main__':
    TrendsWriterService.parse_command_line()