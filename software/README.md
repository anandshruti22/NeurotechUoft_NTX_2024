# Files

## Raspberry Pi
```
├── real_time_processing.py: code loaded onto raspberry pi that interpets EEG signals and sends ML model output to Arduino via serial communication
```

## Data 

```
├── data_1_4_Hz
│   ├── processed training data files (bandpass filter of 1-4Hz + epoch)
├── data_13_17_Hz
│   ├── processed training data files (bandpass filter of 13-17Hz + baseline correction + epoch)
├── test_data
│   ├── processed test data files (bandpass filter of 1-4Hz + epoch)
│   ├── processed training data files (bandpass filter of 13-17Hz + baseline correction + epoch)
│   ├── data_collection_method.md: description on how test data was collected
│   ├── testing_model.md: python notebook where test data was used to see performance of model
```

## Preprocessing Code
```
├── Preprocessing
│   ├── preprocessing.ipynb: preprocessing code showing time frequency analysis and epoching
│   ├── citations.md: Details regarding citations justifying our use of C2, C4, Cz channels
│   ├── raw_data.md: Link to the raw data that is used for model training
```

## ML Model
```
├── ML Model
│   ├── model_training.ipynb: model training code
│   ├── model_with_delta.keras: model to be loaded
│   ├── model_description.md: Details regarding model architecture and citations
```

