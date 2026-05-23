import logging
import multiprocessing
from logging.handlers import RotatingFileHandler

multiprocessing.freeze_support()

import sys
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import asyncio
import multiprocessing
import threading
import socket

from config import setup_engine
from trends_writer import modbus, plant
from trends_writer.profiler import Profiler


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TrendsWriterService"
    _svc_display_name_ = "Trends Writer Service"
    _svc_description_ = "Service serves as a writer for modbus communication of trends data from the devices"

    def __init__(self, args):
        if getattr(sys, "frozen", False):
            path = os.path.join(os.path.dirname(sys.executable), "..", "logs")
        else:
            path = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(path, exist_ok=True)
        try:
            logging.basicConfig(
                handlers=[
                    RotatingFileHandler(
                        os.path.join(path, f"{self._svc_name_}.log"),
                        maxBytes=5_242_880,
                        backupCount=5,
                    )
                ],
                level=logging.INFO,
                format="%(asctime)s %(levelname)s %(message)s",
            )

            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
            self.running = True
            self.loop = None
        except Exception as e:
            logging.fatal(f"{self._svc_name_} creation failed. Exception: {e}")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        children = multiprocessing.active_children()
        for child in children:
            child.terminate()
            child.join(timeout=3)

    def SvcDoRun(self):
        try:
            logging.info(f"{self._svc_name_} starting.")
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, ""),
            )
            self.main()
        except Exception as e:
            logging.fatal(f"{self._svc_name_} start failed. Exception: {e}")

    def main(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(MyService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(MyService)
    except Exception as exc:
        print(f"Main failed. Exception: {exc}")
