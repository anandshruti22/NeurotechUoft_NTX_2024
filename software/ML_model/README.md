# EEG Classification with Temporal Convolutional Neural Networks (TCNN)

## Overview
In our project, we faced significant issues with vanishing and exploding gradients when attempting to train an RNN/LSTM-based model for EEG classification tasks. To address these challenges, we explored the use of Temporal Convolutional Neural Networks (TCNNs), which have shown success in similar tasks such as motion imagery classification (Lun et al., 2020). This document outlines the architecture, training strategy, and performance of our TCNN model.

## Model Architecture
We designed our TCNN model with the following key components and considerations:

- **Significant Dropout (80%)**: Applied to reduce overfitting to the training dataset.
- **He Initialization**: Used in convolutional layers to mitigate vanishing/exploding gradients (He et al., 2015).
- **Large Number of Filters**: Employed in the 1D convolutional layers (32, 64) to capture a richer set of features from the EEG input data.

### Model Code
```python
from tensorflow.keras import layers, models, initializers

def create_model():
    dropout_rate = 0.2
    input_layer = layers.Input(shape=(401, 3))

    x = layers.Conv1D(filters=32, kernel_size=3, strides=2, activation='relu', kernel_initializer=initializers.HeNormal(), padding="same")(input_layer)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2, strides=2)(x)

    x = layers.Conv1D(filters=64, kernel_size=3, strides=2, activation='relu', kernel_initializer=initializers.HeNormal(), padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2, strides=2)(x)

    x = layers.Conv1D(filters=128, kernel_size=3, strides=2, activation='relu', kernel_initializer=initializers.HeNormal(), padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2, strides=2)(x)

    x = layers.Flatten()(x)

    x = layers.Dense(1024, activation="relu", kernel_initializer=initializers.HeNormal())(x)
    x = layers.Dropout(dropout_rate)(x)

    x = layers.Dense(256, activation="relu", kernel_initializer=initializers.HeNormal())(x)
    x = layers.Dropout(dropout_rate)(x)

    output_layer = layers.Dense(1, kernel_initializer=initializers.HeNormal(), activation="sigmoid")(x)

    return models.Model(inputs=input_layer, outputs=output_layer)
```

## Training Strategy
We employed several strategies to improve the performance and stability of our model:

- **Hyperparameter Tuning**: Adjusted learning rates, learning rate schedules, and the number of epochs.
- **Learning Rate Schedule**: Implemented to ensure stable convergence. If the model's loss did not improve after 3 epochs, the learning rate was reduced by 10%.
- **Repeated Training**: Conducted short training sessions (50 epochs) with hyperparameter adjustments to iteratively improve model performance.

### Key Considerations
1. **Dropout**: To counteract overfitting, significant dropout was applied. Initial experiments showed that training accuracy was often 15-20% higher than validation accuracy.
2. **Model Complexity**: While reducing the number of units in dense layers decreased both training and validation accuracy, maintaining a higher complexity was necessary to avoid high bias and variance.
3. **Vanishing/Exploding Gradients**: Although TCNNs are less prone to these issues compared to RNN/LSTM networks, He initialization was crucial to mitigate potential problems.

## Performance Metrics
Our evaluation metrics included binary accuracy, area under the curve (AUC), precision, and recall. We compared our model's performance against existing literature and other models trained on the same dataset.

### Results
- **Training Data**:
  - Classification Accuracy: 80%
  - Precision: 80%
  - Recall: 88%
  
- **Test Data**:
  - Classification Accuracy: 74%
  - Precision: 80%
  - Recall: 79%

These results are competitive with other machine learning models used for motor imagery tasks.

### Own Data Collection
We collected additional data in a manner similar to the dataset's original collection process. Our model achieved around 80% accuracy in predicting hand motions on this new data as well.

## Citation
He, K., Zhang, X., Ren, S., & Sun, J. (2015, February 6). Delving deep into rectifiers: Surpassing human-level performance on ImageNet Classification. arXiv.org. https://arxiv.org/abs/1502.01852
Lun, X., Yu, Z., Chen, T., Wang, F., & Hou, Y. (2020a, July 31). A simplified CNN classification method for Mi-EEG via the electrode pairs signals. Frontiers. https://www.frontiersin.org/articles/10.3389/fnhum.2020.00338/full#B10 


## Summary
Our approach focused on hyperparameter tuning and short epoch training sessions while adjusting learning rates and schedules to achieve stable convergence. The use of TCNNs with He initialization and significant dropout proved effective in addressing the vanishing/exploding gradient issues, resulting in competitive performance in EEG classification tasks.
