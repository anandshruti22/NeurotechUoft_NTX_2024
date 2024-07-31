import mne
import numpy as np
import pandas as pd
import keras
import serial
import argparse
import time
import sys
import os
from tensorflow.python.keras.models import Model
from pprint import pprint

brainflow_path = os.path.expanduser('~/neurotech_project/brainflow/python_package')
if brainflow_path not in sys.path:
    sys.path.append(brainflow_path)

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from tensorflow.keras.models import load_model


def parse_arguments():
    """ Parse command line arguments necessary for board configuration. """
    parser = argparse.ArgumentParser(description='Set up parameters for EEG board.')
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)

    return parser.parse_args()


def setup_board(args):
    """ Setup and return a board with the given parameters. """
    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    board = BoardShim(args.board_id, params)
    board.prepare_session()
    return board


def get_data(board, min_samples=401):
    while board.get_board_data_count() < min_samples:
        time.sleep(0.01)
    data = board.get_board_data()  # get all data and remove it from internal buffer
    return data


def process_realtime_data(data):
    """
    Processes realtime data
    """
    if data.shape[0] < 401:
        raise ValueError("Insufficient data samples available.")

    channel1 = data[3]
    channel2 = data[1]
    channel3 = data[2]
    final_array = np.array([channel1, channel2, channel3]).T
    print(final_array)

    original_freq = 250
    new_freq = 160
    reshaped_data = mne.filter.resample(final_array, axis=0, down=original_freq / new_freq)

    reshaped_data_1 = mne.filter.filter_data(reshaped_data, sfreq=160, l_freq=13, h_freq=17, verbose=False)
    reshaped_data_2 = mne.filter.filter_data(reshaped_data, sfreq=160, l_freq=1, h_freq=4, verbose=False)
    times = np.arange(len(reshaped_data)) / 160
    reshaped_data_new = mne.baseline.rescale(reshaped_data_1, times, (None, None), mode="mean")
    final_data = np.append(reshaped_data_new, reshaped_data_2, axis=1)

    print(reshaped_data.shape)
    reshaped = final_data.reshape(final_data.shape[1], final_data.shape[0])
    print(reshaped.shape)
    return reshaped


def epoch_realtime_data(data):
    """
    Processes realtime data and divides it into epochs of a specified length.
    Each epoch is transposed to fit the model's expected input shape of (401, 3).
    """
    processed_data = process_realtime_data(data)
    final_data = []

    epoch_length = 401  # Number of samples per epoch for approximately 1 second
    step_size = 401  # Set to epoch_length for no overlap (change if overlap is desired)

    lower_time = 0
    upper_time = epoch_length

    while upper_time <= processed_data.shape[0]:
        epoch = processed_data[lower_time:upper_time]
        epoch = epoch.T
        final_data.append(epoch)
        lower_time += step_size
        upper_time += step_size

    final_data = np.array(final_data)
    return final_data


def main():
    BoardShim.enable_dev_board_logger()

    args = parse_arguments()
    board = setup_board(args)
    board.start_stream()

    ser = serial.Serial('/dev/ttyUSB0', 19200)
    model = load_model('model_with_delta.keras', compile=True)

    try:
        while True:
            data = get_data(board)
            if data.shape[1] >= 401:  # Ensure we have enough samples to form an epoch
                final_data = epoch_realtime_data(data)
                old = 0
                for i in model.predict(final_data):
                    for j in i:
                        if old == 0 and j == 1:
                            ser.write(b'1')
                            print("Clench")
                        elif old == 1 and j == 0:
                            ser.write(b'0')
                            print("Unclench")
                        old = j
            else:
                print("Insufficient data. Waiting for more samples.")
                time.sleep(0.1)  # Sleep briefly to avoid high CPU usage when no data is available
    except KeyboardInterrupt:
        print("Stopping by user request.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            board.stop_stream()
        except Exception as e:
            print(f"Failed to stop stream: {e}")
        board.release_session()
        ser.close()


if __name__ == '__main__':
    main()
import mne
import numpy as np
import serial
import argparse
import time
import sys
import os
from tensorflow.keras.models import load_model
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets

brainflow_path = os.path.expanduser('~/neurotech_project/brainflow/python_package')
if brainflow_path not in sys.path:
    sys.path.append(brainflow_path)

def parse_arguments():
    """ Parse command line arguments necessary for board configuration. """
    parser = argparse.ArgumentParser(description='Set up parameters for EEG board.')
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False, default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards', required=False, default=BoardIds.NO_BOARD)

    return parser.parse_args()

def setup_board(args):
    """ Setup and return a board with the given parameters. """
    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    board = BoardShim(args.board_id, params)
    board.prepare_session()
    return board

def process_realtime_data(data):
    """
    Processes realtime data
    """
    channel1 = data[3]
    channel2 = data[1]
    channel3 = data[2]
    final_array = np.array([channel1, channel2, channel3]).T
    print(final_array)

    original_freq = 250
    new_freq = 160
    reshaped_data = mne.filter.resample(final_array, axis=0, down=original_freq / new_freq)

    reshaped_data_1 = mne.filter.filter_data(reshaped_data, sfreq=160, l_freq=13, h_freq=17, verbose=False)
    reshaped_data_2 = mne.filter.filter_data(reshaped_data, sfreq=160, l_freq=1, h_freq=4, verbose=False)
    times = np.arange(len(reshaped_data)) / 160
    reshaped_data_new = mne.baseline.rescale(reshaped_data_1, times, (None, None), mode="mean")
    final_data = np.append(reshaped_data_new, reshaped_data_2, axis=1)

    print(reshaped_data.shape)
    reshaped = final_data.reshape(final_data.shape[1], final_data.shape[0])
    print(reshaped.shape)
    return reshaped

def epoch_realtime_data(data):
    """
    Processes realtime data and divides it into epochs of a specified length.
    Each epoch is transposed to fit the model's expected input shape of (401, 3).
    """
    processed_data = process_realtime_data(data)
    final_data = []

    epoch_length = 401  # Number of samples per epoch for approximately 1 second
    step_size = 401     # Set to epoch_length for no overlap (change if overlap is desired)

    lower_time = 0
    upper_time = epoch_length

    while upper_time <= processed_data.shape[0]:
        epoch = processed_data[lower_time:upper_time]
        epoch = epoch.T
        final_data.append(epoch)
        lower_time += step_size
        upper_time += step_size

    final_data = np.array(final_data)
    return final_data

def main():
    BoardShim.enable_dev_board_logger()

    args = parse_arguments()
    board = setup_board(args)
    board.start_stream()

    ser = serial.Serial('/dev/ttyUSB0', 19200)
    model = load_model('model_with_delta.keras', compile=True)

    accumulated_data = []

    try:
        while True:
            # Fetch small chunks of data
            data = board.get_current_board_data(401)  # Fetch 25 samples at a time

            if data.size == 0:
                time.sleep(0.01)
                continue

            # Accumulate data
            accumulated_data.append(data)

            # Concatenate accumulated data into a single array
            accumulated_data = np.concatenate(accumulated_data, axis=1)

            if accumulated_data.shape[1] >= 401:
                final_data = epoch_realtime_data(accumulated_data[:, :401])
                accumulated_data = accumulated_data[:, 401:]  # Remove the processed part

                old = 0
                for i in model.predict(final_data):
                    for j in i:
                        if old == 0 and j == 1:
                            ser.write(b'1')
                            print("Clench")
                        elif old == 1 and j == 0:
                            ser.write(b'0')
                            print("Unclench")
                        old = j
            else:
                print("Insufficient data. Waiting for more samples.")
                time.sleep(0.1)  # Sleep briefly to avoid high CPU usage when no data is available

    except KeyboardInterrupt:
        print("Stopping by user request.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            board.stop_stream()
        except Exception as e:
            print(f"Failed to stop stream: {e}")
        board.release_session()
        ser.close()

if __name__ == '__main__':
    main()
