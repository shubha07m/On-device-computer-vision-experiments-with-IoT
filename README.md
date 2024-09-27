##  MODIPHY: ##

## ✨🎉 **Latest Update!** 🎉✨

"MODIPHY" is now available freely on IEEE Xplore, follow [IEEE paper link](https://ieeexplore.ieee.org/document/10648081) for free early access.


## ✨🎉 **Exciting News!** 🎉✨

We are thrilled to announce that our paper:

### **“MODIPHY: Multimodal Obscured Detection for IoT using PHantom Convolution-Enabled Faster YOLO”**

will be presented at the upcoming **2024 IEEE International Conference on Image Processing** **(ICIP 2024)** in Abu Dhabi, UAE! 🚀

✨🌟✨🌟✨🌟✨🌟✨

We are beyond excited to share that our paper has been **recognized as one of the top 5% of accepted papers at ICIP 2024!**  🎉🌟

**Stay tuned for more updates!**

## Multimodal Obscured Detection for IoT using PHantom Convolution-Enabled Faster YOLO ##

We developed “YOLO Phantom” for detection in low-light conditions and occluded scenarios within resource-constrained IoT applications. We proposed the novel "Phantom Convolution," which enables YOLO Phantom to achieve comparable accuracy to YOLOv8n with a 43% reduction in parameters and size, resulting in a 19% reduction in GFLOPs. By employing transfer learning on our multimodal dataset, the model demonstrates enhanced vision capabilities in adverse conditions. Our Raspberry Pi IoT platform equipped with noIR cameras and integration with AWS IoT Core and SNS showcases a substantial 17% and 14% boost in frames per second for thermal and RGB data detection, respectively, compared to the baseline YOLOv8n model.


### Comparison of small models ###

![GFLOP Comparison](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/gflop.png)


### Detection in various low light and occluded conditions ###

![Low light detections](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/ous_images.png)

To know more about the MODIPHY please refer to the preprint available in [arXiv](https://arxiv.org/abs/2402.07894)

Please refer to [yolo_phantom](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/tree/main/yolo_phantom) for the implementation.

Download the [multimodal dataset](https://drive.google.com/drive/folders/1a54u6PpfHOSTL4AME25S1_b1AfTvRCfL?usp=sharing)

### Steps to use YOLO Phantom ###

1\. Install the [Ultralytics](https://github.com/ultralytics/ultralytics) library in a Conda or virtual environment.

2\. Once in the environment, verify the installation location of the Ultralytics library using `pip list`. 
   - The path should end with `/site-packages`, and there should be an `ultralytics` folder inside it.

3\. Clone my repository to your computer.

4\. Navigate to the [yolo_phantom](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/tree/main/yolo_phantom) folder and copy the `cfg` and [nn](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/tree/main/yolo_phantom/nn) folders.

5\. Paste the copied `cfg` and `nn` folders into the Ultralytics folder mentioned in step 2.

6\. Verify that the YOLO Phantom model and weights are functioning correctly by using the [yolophantom_testing](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/yolo_phantom/yolophantom_testing.ipynb) file.


## Initial experiments with pre-trained Ultralytics YOLO model ##

### yolov8 for object detection and tracking from live camera feed ###

![alt text](https://github.com/shubha07m/yolov8-testing/blob/main/yolov8_snap.png?raw=true)


I utilized the latest version of YOLO, V8, developed by Ultralytics, to construct an object detection demonstration. I used the Ultralytics library to enable detection and tracking tasks from a live camera feed.

I utilized my OnePlus 6 Android phone as a live camera device to facilitate a rapid and simplistic implementation. I used a free elementary application called "Camo Studio", which I installed on both my phone and M1 MacBook Air. This application permits my phone's camera to function as an external webcam for my laptop. The primary objective of this project was to simulate a surveillance camera scenario for detecting both vehicles and pedestrians.

While experimenting with various pre-trained YOLOv8 models, I discovered that the YOLOv8n variant was efficient enough to detect and track fast-moving traffic even in low-light and nocturnal conditions.

For reference, here are the relevant resources I employed for Ultralytics and Camo:

https://github.com/ultralytics/ultralytics

https://reincubate.com/camo/

## Raspberry pi based human / other object detection and audio notification with CPU temperature-controlled environment ##

![alt text](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/from_pi/rpi4b.png)

I used a [CanaKit](https://www.amazon.com/dp/B08B6F1FV5?psc=1&ref=ppx_yo2ov_dt_b_product_details) based raspberry pi version 4, model B (CanaKit extreme, 128 Gb, 8Gb, BullsEye OS) and a USB camera for object detection this time. A few of the interesting features were tested this time:

1. YOLOV8 ('yolov8n.pt' the smaller model by Ultralytics) was tested working successfully with a much smaller capacity CPU-based IoT system.
2. An audio-based alert system on detection with various conditions and parameters was tested.
3. A predefined CPU temperature threshold was used to control the run, such that the detection ends when it crosses a certain CPU temperature.
4. Inside house or low-light outside environments were also tested.

A few of the learnings are:

1. Ultralytics-based YOLOV8 only works in a 64-bit OS and 64-bit Python-based system, the default CanaKit pi board had to re-image with the latest 64-bit Raspberry Pi image.
2. FPS is slow as expected but detection accuracy was decent.
3. Raspberry Pi board reaches up to 60 within 15 minutes of running roughly, although usually, pi works fine up to 80 deg C.


## Object detection and notification with multimodal fusion using AWS ##

I recently used my Raspberry Pi to develop a low-light detection and notification system, using AWS. Thanks to my newly trained multimodal YOLO variants (trained on RGB and thermal image fusion data), I was able to achieve decent detection capability even in poor lighting conditions, regardless of the time of day. Here are some of the key learnings from this exercise:

1.  The n variants of models (the smaller models) worked much faster, with decent detection capability compared to the x variants(the larger models with higher accuracy), this is valid for multimodal models as well.
2.  Although larger variants did run in pi, considering the latency it is impractical to use one for real-time detection, esp. for low-power IoT devices.
3. The fusion-data-trained multimodal models worked more accurately in low-light conditions compared to the pre-trained versions of YOLOV8.
4.  The new addition was the AWS-based notification this time. Using AWS IoT core and SNS I built a notification system and worked perfectly.
5. The smaller multimodal model does false detection occasionally, which is extremely rare and acceptable for the speed.
6. The Raspberry Pi CPU temperature monitoring system I developed previously was also running parallel to protect my precious Pi.
7. While larger variants pre-trained / fusion-trained YOLO models max out the pre-set temparature limit for pi (60 c), smaller variants runs easily for the whole day, makes it more practical for low power IoT based applications.


# The Raspberry Pi setup #
![alt text](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/from_pi/raspberry_pi_setup.png)


# Notification in AWS IoT core for person detection #
![alt text](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/from_pi/notification_aws_IoT.png)

# Note # 
If you are wondering why the images here look a bit meh, remember the camera was behind double-glazing glass and a net, thereafter the photo of live detection was taken from that monitor. For reference, an out-of-sample RGB detection example by fusion data trained multimodal YOLOV8X model in my Mac is also shown.

![alt text](https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/blob/main/from_pi/yolov8x_fusion_mac.png)

For implementation please refer: https://github.com/shubha07m/On-device-computer-vision-experiments-with-IoT/tree/main/from_pi


## **Cite Our Work**

If you like our work, please consider citing it as follows:

```bibtex
@INPROCEEDINGS{10648081,
  author={Mukherjee, Shubhabrata and Beard, Cory and Li, Zhu},
  booktitle={2024 IEEE International Conference on Image Processing (ICIP)}, 
  title={MODIPHY: Multimodal Obscured Detection for IoT using PHantom Convolution-Enabled Faster YOLO}, 
  year={2024},
  volume={},
  number={},
  pages={2613-2619},
  keywords={YOLO;Accuracy;Convolution;Computational modeling;Transfer learning;Phantoms;Real-time systems;Low light object detection;Multimodal fusion;IoT;YOLO;Phantom Convolution},
  doi={10.1109/ICIP51287.2024.10648081}}

## Previous work ##

In my previous research, UNIMODAL was developed for search and disaster recovery using infrared images and tested with older YOLO versions (V3, V4, and V7). My paper on the same can be accessed here: https://ieeexplore.ieee.org/document/10025436

This paper can be cited as below:

@INPROCEEDINGS{10025436,
  author={Mukherjee, Shubhabrata and Coudert, Oliver and Beard, Cory},
  booktitle={2022 IEEE International Symposium on Technologies for Homeland Security (HST)}, 
  title={UNIMODAL: UAV-Aided Infrared Imaging Based Object Detection and Localization for Search and Disaster Recovery}, 
  year={2022},
  volume={},
  number={},
  pages={1-6},
  keywords={Location awareness;Training;5G mobile communication;Transfer learning;Object detection;Infrared imaging;US Department of Homeland Security;UAV aided disaster recovery;YOLO based infrared object detection;YOLOV7-official;Autonomous Vehicular Network operations},
  doi={10.1109/HST56032.2022.10025436}}

## Acknowledgement ##

YOLO Phantom code base is built with ![ultralytics](https://github.com/ultralytics/ultralytics) and many of the base modules of YOLOV8 were used.
Thanks for the great implementations!
