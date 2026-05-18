import logging
import multiprocessing
from logging.handlers import RotatingFileHandler

multiprocessing.freeze_support()
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages'))

import multiprocessing
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time


import asyncio
import multiprocessing
import sys
import threading
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv')
sys.path.insert(0, os.path.join(venv_path, 'Lib', 'site-packages'))
from config import setup_engine
from trends_writer import modbus, plant
from trends_writer.profiler import Profiler


import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'TrendsWriterService'
    _svc_display_name_ = 'Trends Writer Service'
    _svc_description_ = 'Service serves as a writer for modbus communication of trends data from the devices'

    def __init__(self, args):
        if getattr(sys, "frozen", False):
            path = os.path.join(os.path.dirname(sys.executable), "..", "logs")
        else:
            path = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(path, exist_ok=True)
        try:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            logger.handlers.clear()
            handler = RotatingFileHandler(os.path.join(path, self._svc_name_ + '.log'), maxBytes=5242880, backupCount=5)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                                          "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logging.basicConfig(level=logging.DEBUG, handlers=[handler])
            logging.info(f"{self._svc_name_} created.")

            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
            self.loop = None
        except Exception as e:
            logging.fatal(f"{self._svc_name_} creation failed. Exception: {e}")

    def SvcStop(self):
        logging.info(f"{self._svc_name_} stopping.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.loop.call_soon_threadsafe(self.loop.stop)
        children = multiprocessing.active_children()
        for child in children:
            child.terminate()
            child.join(timeout=3)

    def SvcDoRun(self):
        try:
            logging.info(f"{self._svc_name_} starting.")
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, ''))
            self.main()
        except Exception as e:
            logging.fatal(f"{self._svc_name_} start failed. Exception: {e}")

    def main(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        import multiprocessing.spawn
        multiprocessing.set_executable(
            os.path.join(os.path.dirname(sys.executable), 'python.exe')
        )

        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            setup_engine()
            Profiler.init()

            thread = threading.Thread(target=self.run_server, daemon=True)
            thread.start()

            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        except Exception as e:
            logging.fatal(f"{self._svc_name_} start failed. Exception: {e}")

    def run_server(self):
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(modbus.run_server(plant.PipePlant()))
        except Exception as e:
            logging.fatal(f"{self._svc_name_} run_server failed. Exception: {e}")

    @classmethod
    def svc_name(cls):
        return cls._svc_name_

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(MyService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(MyService)
            if 'install' in sys.argv:
                import winreg

                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                         f"SYSTEM\\CurrentControlSet\\Services\\{MyService.svc_name()}",
                                         0, winreg.KEY_SET_VALUE)
                    correct_path = os.path.join(os.path.dirname(sys.executable), 'pythonservice.exe')
                    winreg.SetValueEx(key, 'ImagePath', 0, winreg.REG_EXPAND_SZ, f'"{correct_path}"')
                    winreg.CloseKey(key)
                    print(f"Fixed ImagePath to: {correct_path}")
                except Exception as exc:
                    print(f"Could not fix ImagePath: {exc}")
    except Exception as exc:
        print(f'Main failed. Exception: {exc}')
