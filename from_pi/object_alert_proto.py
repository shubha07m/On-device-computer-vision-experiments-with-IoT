from ultralytics import YOLO
import cv2
import os
from temp_monitor import temp_monitoring as tmon


def pi_objdetect(model_used='yolov8n.pt', max_temp=60, max_frame=10000, special_obj=0, max_obj_frame=3,
                 rst_obj_frame=100, conf_thresh=.7):
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    obj_frame = 0
    total_frame = 0

    while cap.isOpened():
        total_frame += 1

        if total_frame == rst_obj_frame:
            obj_frame = 0

        if (total_frame > max_frame) or (tmon(max_temp) > max_temp):
            cap.release()
            cv2.destroyAllWindows()
            exit()

        else:
            success, frame = cap.read()

            if success:
                results = model(frame, conf=conf_thresh, show=True)

                for result in results:
                    boxes = result.boxes.cpu().numpy()

                    for box in boxes:
                        cls = int(box.cls[0])

                        if cls == special_obj:
                            obj_frame += 1

                            if obj_frame <= max_obj_frame:
                                print('there is a person')
                                os.system('cvlc --play-and-exit Desktop/object_detection/person.mp3')

                        else:
                            print(cls)


if __name__ == "__main__":
    pi_objdetect()