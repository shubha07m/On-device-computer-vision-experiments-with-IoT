## yolov8 for object detection and tracking from live camera feed ##

![alt text](https://github.com/shubha07m/yolov8-testing/blob/main/yolov8_snap.png?raw=true)


I utilized the latest version of YOLO, V8, developed by Ultralytics, to construct an object detection demonstration. I used the Ultralytics library to enable detection and tracking tasks from a live camera feed.

To facilitate a rapid and simplistic implementation, I utilized my OnePlus 6 android phone as a live camera device. I used a free limentary application called "Camo Studio", which I installed on both my phone and M1 MacBook Air. This application permits my phone's camera to function as an external webcam for my laptop. The primary objective of this project was to simulate a surveillance camera scenario for detecting both vehicles and pedestrians.

During my experimentation with various pre-trained YOLOv8 models, I discovered that the YOLOv8n variant was efficient enough at detecting and tracking fast-moving traffic even in low-light and nocturnal conditions.

For reference, here are the relevant resources I employed for Ultralytics and Camo:

https://github.com/ultralytics/ultralytics

https://reincubate.com/camo/

Using the above idea, UNIMODAL was developed for search and disaster recovery and was tested with older versions of YOLO (V3, V4 and V7). My paper on the same can be accessed here: https://ieeexplore.ieee.org/document/10025436

S. Mukherjee, O. Coudert and C. Beard, "UNIMODAL: UAV-Aided Infrared Imaging Based Object Detection and Localization for Search and Disaster Recovery," 2022 IEEE International Symposium on Technologies for Homeland Security (HST), Boston, MA, USA, 2022, pp. 1-6, doi: 10.1109/HST56032.2022.10025436.


## Raspberry pi based human / other object detection, audio alarm creation in CPU temperature controlled environment ##

I used a CanaKit based raspberry pi version 4B (BullsEye OS) and an USB camera for object detection this time. Few of the interesting features were tested this time:

1. YOLOV8 ('yolov8n.pt' the smaller moodel by Ultralytics) were tested working successfully with a much smaller capacity CPU based IoT system.
2. An audio based alert system on detection with various conditions and parameters was tested.
3. A predefined CPU temperature threshold was used to control the run, such that the detection ends when it crosses a certain CPU temperature.
4. Inside house or low-light outside environment were also tested.

Few of the learnings are:

1. Ultralytics based YOLOV8 only works in a 64 bit OS and 64 bit python based system, the default CanaKit pi board had to re-image with latest 64 bit raspberry pi image.
2. FPS is slow as expected but detection accuracy was decent.
3. Raspberry pi board reaches upto 60 within 15 minutes of run roughly, although usually pi works fine upto 80 deg C.


For code and demo detection videos please refer to the from_pi section of the repo.




