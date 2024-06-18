# NeilA Ground Station Interface

NeilA Ground Station Interface is developed for the Teknofest 7th Model Satellite Competition to act as a ground station. The project visualizes the data received every second from an ESP module.

# Serial Data Format
The program expects data from the serial port in the following format:
```bash
<team_no>,<packet_no>,<mission_time>,<payload_pressure>,<container_pressure>,<payload_altitude>,<container_altitude>,<altitude>,<speed>,<temperature>,<voltage>,<gps_latitude>,<gps_longitude>,<gps_altitude>,<container_latitude>,<container_longitude>,<container_altitude>,<statu>,<pitch>,<roll>,<yaw>,<turn_num>,<video_state>,<microprocessor_temperature>
```
# Example Data
Here is an example of the expected data format:
```bash
356356,12,2023-06-18 12:34:56,1013.25,1012.78,500,450,50,5.0,25.4,3.7,40.7128,-74.0060,10,40.7127,-74.0059,15,1,0.5,0.0,0.0,3,1,40.0
```

![alt text](https://github.com/rai-shi/NEILA-Ground_Station/blob/master/ui.png?raw=true)

## Technologies Used

- **Programming Language:** Python
- **GUI Design and Development:** Tkinter
- **Graphics:** Matplotlib
- **Satellite Position Animation:** Matplotlib 3D Plot
- **Map View:** TkinterMapView
- **Camera Display and Recording:** OpenCV
- **Serial Data Communication:** Serial
- **Asynchronous Video Streaming:** Ftplib

## Installation Instructions

Ensure you have the following libraries installed:

```bash
pip install tkinter matplotlib pillow psutil pyserial opencv-python tkintermapview
```
## Usage Instructions
To run the project, execute the following file:
```bash
path\to\NEILA-Ground_Station\NeilA-UI\dist\NeilA_UI.exe
```
For development, use the following file:
```bash
path\to\NEILA-Ground_Station\NeilA-UI\NeilA_UI.py
```
## Contributing
The project currently experiences performance issues and frequent program freezes after running for some time. The threading implementation needs improvement. Contributions focusing on threading and optimization are welcome.

Contact Information
For any inquiries or feedback, please contact: aysenurtak1@gmail.com
