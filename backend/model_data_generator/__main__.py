from datetime import datetime
from pickletools import uint1
import time
import logging
from time import sleep
from control.plant import Plant
import random


if __name__ == '__main__':
    try:
        pump_time_min = 30
        pump_time_max = 31

        wave_death_time_min = 30 #s
        wave_death_time_max = 90 #s

        leak_time_min = 1
        leak_time_max = 5

        rest_time_after_pomping_min = 30
        rest_time_after_pomping_max = 90


        cycle_amount_to_generate = 30
        leaks_amount_to_generate_on_one_cycle = 5
        time_between_cycles = 10
        pipeline_mode = ["stationary"]


        logging.info('Test started')


        plant = Plant()


        plant.device(385).variable('Ctr_Mode_Alternating').write(True)

        for i in range(cycle_amount_to_generate):
            choosen_pipeline_mode = random.choice(pipeline_mode)

            if choosen_pipeline_mode == "stationary":
                logging.info('Stationary sequence')

                choosen_pump_time = random.randint(pump_time_min, pump_time_max)
                choosen_rest_after_pomping_time = random.randint(rest_time_after_pomping_min, rest_time_after_pomping_max)
                plant.device(385).variable('Ctr_Start').write(True)
                sleep(choosen_pump_time)
                
                plant.device(385).variable('Ctr_Stop').write(True)
                sleep(choosen_rest_after_pomping_time)

                for j in range(leaks_amount_to_generate_on_one_cycle):

                    choosen_valve_id = random.choice(range(457,463))
                    choosen_leak_time = random.randint(leak_time_min, leak_time_max)
                    choosen_rest_time = random.randint(wave_death_time_min, wave_death_time_max)

                    logging.info(f'Leak started: on device no. {choosen_valve_id} on {datetime.fromtimestamp(time.time())}')
                    plant.device(choosen_valve_id).variable('Ctr_Open').write(True)
                    sleep(choosen_leak_time)
                    plant.device(choosen_valve_id).variable('Ctr_Close').write(True)
                    logging.info(f'Leak stopped: on device no. {choosen_valve_id} on {datetime.fromtimestamp(time.time())}')
                    sleep(choosen_rest_time)

            if choosen_pipeline_mode == "quasistationary":
                logging.info('Quasistationary sequence')

            
                choosen_pump_time = random.randint(pump_time_min, pump_time_max)
                choosen_rest_after_pomping_time = random.randint(rest_time_after_pomping_min, rest_time_after_pomping_max)
                plant.device(385).variable('Ctr_Start').write(True)
                sleep(choosen_pump_time)

                for j in range(leaks_amount_to_generate_on_one_cycle):

                    choosen_valve_id = random.choice(range(457,463))
                    choosen_leak_time = random.randint(leak_time_min, leak_time_max)
                    choosen_rest_time = random.randint(wave_death_time_min, wave_death_time_max)

                    logging.info(f'Leak started: on device no. {choosen_valve_id} on {datetime.fromtimestamp(time.time())}')
                    plant.device(choosen_valve_id).variable('Ctr_Open').write(True)
                    sleep(choosen_leak_time)
                    plant.device(choosen_valve_id).variable('Ctr_Close').write(True)
                    logging.info(f'Leak stopped: on device no. {choosen_valve_id} on {datetime.fromtimestamp(time.time())}')
                    sleep(choosen_rest_time)

                plant.device(385).variable('Ctr_Stop').write(True)
                sleep(10)

            if choosen_pipeline_mode == "Undefined":
                pass

        logging.info('Test ended')

    except Exception as e:
        logging.error(e)   
