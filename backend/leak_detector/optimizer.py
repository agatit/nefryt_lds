import copy
import json
import math
from collections import defaultdict
from datetime import datetime
import sys
import os
from itertools import product

import numpy as np
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine, Settings, setup_logging
from leak_detector.plant import Plant

seconds_tolerance = 2
dataset_filename = 'backend/leak_detector/tests/leakage_dataset.json'
tested_pipeline_id = 1
tested_method_id = 20
experiment_results_filename = f'backend/leak_detector/tests/experiment_results_{tested_method_id}.csv'

class Leakage:
    time: float
    position: float

    def __init__(self, time: float, position: float):
        self.time = time
        self.position = position

    def __str__(self):
        return f'position: {self.position}, time: {datetime.fromtimestamp(self.time)}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.time == other.time and self.position == other.position


def load_leakages_from_json(filename: str) -> list[Leakage]:
    with open(filename, 'r') as f:
        leakages = json.load(f)

    return [Leakage(leakage['time'], leakage['position']) for leakage in leakages]


def create_detection_periods(leakages_dataset: list[Leakage]) -> list[tuple]:
    periods = []
    for leakage_start, leakage_end in zip(leakages_dataset[::5], leakages_dataset[4::5]):
        period_start = datetime.fromtimestamp(leakage_start.time - 8)
        period_end = datetime.fromtimestamp(leakage_end.time + 8)
        periods.append((period_start, period_end))

    return periods


def leak_detector(leakages_dataset: list[Leakage], method_params_dict: dict) -> list[Leakage]:
    setup_engine()
    plant = Plant()
    detection_time = 10000
    detection_periods = create_detection_periods(leakages_dataset)
    events = []
    for pipeline_id, pipeline_method_params in method_params_dict.items():
        for method_id, method_params in pipeline_method_params.items():
            plant.pipelines[pipeline_id].active_methods[method_id].update_params(method_params)

    for detection_period in detection_periods:
        begin_detection_date = detection_period[0]
        end_detection_date = detection_period[1]
        begin_detection_time = int(begin_detection_date.timestamp() * 1000) - plant.get_leakage_alarm_delta()

        while begin_detection_time < detection_period[1].timestamp() * 1000 - plant.get_leakage_alarm_delta():
            end_detection_time = begin_detection_time + plant.get_leakage_alarm_delta() + detection_time
            end_detection_time = end_detection_time if end_detection_time <= (
                        end_detection_date.timestamp() * 1000) else (end_detection_date.timestamp() * 1000)
            for pipeline in plant.pipelines.values():
                leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)
                for _, leak_events in leaks.items():
                    leak_events = sorted(leak_events, key=lambda leak_event: leak_event.datetime)
                    predicted_events = [Leakage(time=leak_event.time//1000, position=round(leak_event.position, 2))
                                        for leak_event in leak_events]
                    events.extend(predicted_events)

            begin_detection_time += detection_time
    return events


def validate_results(leakage_dataset: list[Leakage], detected_leakages: list[Leakage], print_summary: bool = True) -> dict:
    tp = 0
    fp = 0
    fn = len(leakage_dataset)
    real_not_matched = copy.deepcopy(leakage_dataset)
    predicted_not_matched = []
    matched = []
    sum_diff_pos = 0

    last_used = 0
    for predicted in detected_leakages:
        match = False
        for i, real in enumerate(leakage_dataset[last_used:]):
            diff_t = abs(predicted.time - real.time)
            diff_pos = abs(predicted.position - real.position)
            if diff_t <= seconds_tolerance:
                tp += 1
                fn -= 1
                last_used += i
                match = True
                if real in real_not_matched:
                    matched.append((real, predicted))
                    real_not_matched.remove(real)
                    sum_diff_pos += diff_pos
                    break
                elif print_summary:
                    print('two matches for one real leakage: ', str(real))
        if not match:
            predicted_not_matched.append(predicted)
            fp += 1

    if print_summary:
        print('=====SUMMARY=====')
        print(f'Matched {len(matched)} leakages')
        print(f'Missed {len(real_not_matched)} real leakages')
        print(f'Incorrect {len(predicted_not_matched)} predicted leakages')
        print('=====MATCHED=====')
        for match in matched:
            print(match)
        print('=====REAL NOT MATCHED=====')
        for real in real_not_matched:
            print(real)
        print('=====PREDICTED NOT MATCHED=====')
        for pred in predicted_not_matched:
            print(pred)

    return {
        'matched': len(matched),
        'real not matched': len(real_not_matched),
        'predicted not matched': len(predicted_not_matched),
        'average position difference': sum_diff_pos/len(matched)
    }


params_spaces = {
    1001: {
        'BASE_WAVE_SPEED': np.arange(400, 451, 25),
        'DROP_LEVEL': np.arange(25, 201, 50),
        'NO_DETECTION_WINDOW_SECONDS': np.arange(10, 50, 13)
    },
    20: {
        'BASE_WAVE_SPEED': np.arange(400, 451, 50),
        'LEAKAGE_LEVEL': np.arange(0.02, 0.04, 0.01),
        'ALARM_LEVEL': np.arange(0.05, 0.07, 0.1),
        'WAVE_COEFF': np.arange(0.0001, 0.001, 0.005),
        'NO_DETECTION_WINDOW_SECONDS': np.arange(10, 50, 250),
        'MIN_WAVE_VALUE': np.arange(10, 100, 500)
    }
}

if __name__ == '__main__':
    Settings.verbosity = 'ERROR'
    Settings.leak_detector_plot = False
    Settings.optimizer_method_id = tested_method_id
    Settings.optimizer_pipeline_id = tested_pipeline_id
    setup_logging()

    real_leakages = load_leakages_from_json(dataset_filename)

    params_space = params_spaces[tested_method_id]
    param_names = list(params_space.keys())
    param_values = list(params_space.values())

    combined_data = defaultdict(lambda: list())
    tests_count = math.prod([len(value) for value in params_space.values()])
    test_no = 1
    for values in product(*param_values):
        params_for_method = dict(zip(param_names, values))

        params = {
            tested_pipeline_id: {
                tested_method_id: params_for_method
            }
        }

        print(f'Test {test_no}/{tests_count} = {params}')

        event_leakages = leak_detector(real_leakages, params)
        validation_results = validate_results(real_leakages, event_leakages, False)
        for key, value in list(params[tested_pipeline_id][tested_method_id].items())+list(validation_results.items()):
            combined_data[key].append(value)

        test_no += 1
        if test_no > 2:
            break

    new_combined_data = {}
    for i, (key, value) in enumerate(combined_data.items()):
        new_combined_data[' '.join([part.lower() for part in key.split('_')])] = value
    combined_data_df = pd.DataFrame.from_dict(new_combined_data)
    combined_data_df.to_csv(experiment_results_filename, index=False)
    print(combined_data_df)
