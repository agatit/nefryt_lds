import logging
from .plant import Plant



if __name__ == '__main__':

    try:
        logging.info('Test started')
        plant = Plant()

        logging.info('Reding variable...')
        a = plant.device(462).variable('Cfg_LeakTime').read()
        logging.info(f'Variable value: {a}')

        logging.info('Writing variable...')
        a += 10
        plant.device(462).variable('Cfg_LeakTime').write(a)
        logging.info(f'Variable value: {a}')  

        logging.info('Reding variable...')
        a = plant.device(462).variable('Cfg_LeakTime').read()
        logging.info(f'Variable value: {a}')   
    except Exception as e:
        logging.error(e)   
