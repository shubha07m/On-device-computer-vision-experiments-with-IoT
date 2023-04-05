## yolov8 for object detection and tracking from live camera feed ##

I utilized the latest version of YOLO, V8, developed by Ultralytics, to construct an object detection demonstration. I used the Ultralytics library to enable detection and tracking tasks from a live camera feed.

To facilitate a rapid and simplistic implementation, I utilized my OnePlus 6 android phone as a live camera device. I used a free limentary application called "Camo Studio", which I installed on both my phone and M1 MacBook Air. This application permits my phone's camera to function as an external webcam for my laptop. The primary objective of this project was to simulate a surveillance camera scenario for detecting both vehicles and pedestrians.

During my experimentation with various pre-trained YOLOv8 models, I discovered that the YOLOv8n variant was efficient enough at detecting and tracking fast-moving traffic even in low-light and nocturnal conditions.

For reference, here are the relevant resources I employed for Ultralytics and Camo:
https://github.com/ultralytics/ultralytics
https://reincubate.com/camo/

Using the above idea, UNIMODAL was developed for search and disaster recovery and was tested with older versions of YOLO (V3, V4 and V7). My paper on the same can be accessed here: 

S. Mukherjee, O. Coudert and C. Beard, "UNIMODAL: UAV-Aided Infrared Imaging Based Object Detection and Localization for Search and Disaster Recovery," 2022 IEEE International Symposium on Technologies for Homeland Security (HST), Boston, MA, USA, 2022, pp. 1-6, doi: 10.1109/HST56032.2022.10025436.


