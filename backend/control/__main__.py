from datetime import datetime
import time
import logging
from time import sleep
from .plant import Plant



if __name__ == '__main__':

    try:
        pump_time = 180
        wave_death_time = 300
        logging.info('Test started')
        plant = Plant()

        plant.device(385).variable('Ctr_Mode_Alternating').write(True)

        plant.device(385).variable('Ctr_Start').write(True)
        sleep(pump_time)
        plant.device(385).variable('Ctr_Stop').write(True)
        sleep(wave_death_time)

        for id in range(457, 463):
            logging.info(f'Leak started: on device no. {id} on {datetime.fromtimestamp(time.time())}')
            plant.device(id).variable('Ctr_Leak').write(True)
            sleep(wave_death_time)
            plant.device(385).variable('Ctr_Start').write(True)
            sleep(pump_time)
            plant.device(385).variable('Ctr_Stop').write(True)
            sleep(wave_death_time)

        logging.info('Test ended')

    except Exception as e:
        logging.error(e)   
