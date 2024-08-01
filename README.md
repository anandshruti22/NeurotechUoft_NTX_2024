# NeurotechUoft_NTX_2024
The University of Toronto's Neurotechnology design team's submission to NTX competition 2024

## Contributors:
##### Software Subsystem: 
* Subsystem Lead: Shruti Anand (Undergrad Biomedical Engineering, Year 3) 
* Subsystem Members: Brandon Wong (Undergrad Computer Science, Year 2)
  Naoraj Farhan
  Yunran Yang
##### Hardware Subsystem:
* Subsystem Lead: Shuntaro Wakamatsu (Undergrad Computer Engineering, Year 3)
* Subsystem Members:
  Nafew Islam (Undergrad Mechanical Engineering, Year 2),
  Robert Youssef (Undergrad Mechanical Engineering, Year 2),
  Luna Sun (Undergrad Electrical Engineering, Year 2)

## Description of Project: 

About 15% of the world's population lives with some form of disability, of whom 2-4% experience significant difficulties in functioning. Among this statistic are individuals with weakened grip strength or hand amputees. Weakened grip strength or inability to perform grasping motions strongly limit the ability to perform daily household tasks. 

Our aim is to create a prototype of a mind controlled prosthetic hand that can conduct hand grasping motions based on the user’s thoughts. The objectives of our design are to: 
1) Create a prosthetic hand that can conduct the following two motions:
* Opening hand 
* Closing hand 

2) Identify the above two hand motions from EEG signals 

3) Retrieve relevant EEG signals from OpenBCI headset


## Pipeline:

The flow of data in our EEG controlled prosthetic hand works as follows:
1) Setup and Connection: Connect the OpenBCI headset to the OpenBCI Cyton board.
2) Data Transmission: Communicate with  Raspberry Pi through OpenBCI dongle. 
3) Data Streaming: Implement BrainFlow to stream EEG data live.
4) Data Processing : Run signal processing algorithms to denoise the EEG signals.
5) Machine Learning Model Execution : Execute the machine learning model to classify EEG signals.
6) Communication with Arduino: Send the result of the ML model to an Arduino via serial communication
7) Hand Motion: Arduino instructs the motors on the prosthetic hand to conduct the specified hand motion

## Navigation

Navigate through our repository and find the following information: 

* Software Subsystem: Our code to preprocess training data, train our ML model, and test our ML model using data we collected.
* Hardware Subsystem: Our CAD Files containing our prosthetic hand design, hand assembly instructions, Arduino code to control the hand, and a PCB design to be implemented in future iterations.
* Presentation: Our Presentation recording and the associated slides.

## Equipment and Software Installation: 

### Hardware Equipment required: 
* Raspberry Pi 4
* Arduino
* Jumper wires
* 2 Arduino Power Supply Modules
*  5 SG90 servo motors
*  PLA for 3d Printing
*  Rubber bands
*  USB-A to MicroUSB cable
*  2 AC to DC power coverters
  
### Software libraries to be installed: 
Read requirements.txt file for python libraries needed to run the code in the software subsystem folder. 


