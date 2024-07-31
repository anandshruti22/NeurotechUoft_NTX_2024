# EEG-Controlled Prosthetic Arm

## Overview
The EEG-Controlled Prosthetic Arm project aims to create a functional prosthetic arm that responds to brain signals. By integrating an EEG (electroencephalogram) headset, a 3D printed hand, a microcontroller, and servo motors, this project enables users to control the arm using their brain activity.

## CAD Files
The project includes the following CAD files:

- **Fingers**: There are 10 files for the fingers, each corresponding to a specific joint of a finger. These files are exported in both `.3mf` and `.f3d` formats (located in `hardware/CADfiles/3mf` and `hardware/CADfiles/f3d`, respectively).
- **Palm**: The palm design consists of two files: one cover and one main body (located in `hardware/CADfiles/palm`).
- **Shaft**: The shaft file (located in `hardware/CADfiles/shaft`) connects the finger joints. It has a diameter of approximately 2.8mm The shafts should be glued to the outer wall of the junction part so that it allows the inner part to move freely. The junction parts are designed not to bend more than 90 degrees or bend backwards.

## 3D Prints Assembly
To assemble the 3D prints:
- Place the motors inside the palm and glue them for maximum steadiness
- Put the string through the holes of each finger component
- Connect each finger joint using the 3D printed shafts.
- hook the rubber bands
- Push the cover of the palm into the main body (no need for gluing).

## Motors
The prosthetic arm features 5 SG90 servo motors placed inside the palm. Continuous motors were chosen because of their ability to keep winding. The choice of continuous motors allows for more rotations with a smaller radius, eliminating the need for bulky servo motor horns or attachments. This design optimization enables us to fit the motors comfortably inside the hand. Here's how they are set up:

- **Motor Placement**: The servo motors are strategically positioned within the palm to drive finger movements. There are small poles inside the palm that guides the string to its corresponding motor.
- **Control**: An Arduino microcontroller (tested with Arduino Due) runs the `control.ino` code (located in `hardware/ArduinoCode/control.ino`) to manage motor rotation.
- **String Mechanism**: For each finger, a strong (able to withstand at least 6kg of load) string (with a diameter of no more than 2.0 mm) is threaded through holes in the finger components. At the fingertip, the strings are securely tied to prevent them from slipping out. The other end of the strings is firmly attached to the servo motor shaft using modified servo motor horns and super glue. The horns create a groove where the strings wind and unwind.
- **Motor Control Wires**: The wires from the motors exit through five square windows at the wrist cross-section. The power pins (orange) receive 5V voltage and draw a current of 360mA. Since Arduino Due has only one 5V pin, two Arduino Power Supply Modules provide additional 4 5V power pins (2 power pins for each supply module). The ground pins (black) of the motors are connected to the same voltage. Control pins (yellow) are connected to the digital pins of the Arduino Due as follows:
  - Thumb: Pin 2
  - Index: Pin 9
  - Middle: Pin 10
  - Ring: Pin 11
  - Pinky: Pin 12
- **Feedback Wires**: On top of each finger, wires form a closed circuit. One end connects to a 3.3V power source, while the other end attaches to the analog pins of the Arduino Due:
  - Index: A0
  - Middle: A1
  - Ring: A2
  - Pinky: A3
  - A short jumper wire with woven edges ensures good contact. When the fingers are fully extended, the woven edges touch, creating a 3.3V signal. Arduino detects this and stops motor rotation.
- **Rubber Bands**: Plastic hair ties hooked onto small protrusions on each finger joint assist in retracting the fingers when the motor unwinds. Adjust their length to maintain tension.

## Arduino
Upload the "control.ino" file to the Arduino Due using the Arduino IDE software. Connect Arduino to the Raspberry Pi using a USB-A to MicroUSB cable for communication.
