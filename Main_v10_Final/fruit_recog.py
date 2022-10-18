import argparse
import time
from pathlib import Path
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
# from color_sign_recog import color_sign_recog

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

def fruit_recog(color):
    width = 640
    height = 640
    x_benchmark = width/2
    cls = 0

    source = '3'
    weights = 'model_weight/best.pt'
    imgsz = 416
    cuda_device = '0'
    augment_inf = False
    conf_thres = 0.8
    iou_thres = 0.45
    classes = None
    save_conf = False
    agnostic_nms = False
    trace = 0
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))
    # Initialize
    set_logging()
    device = select_device(cuda_device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if trace:
        model = TracedModel(model, device, imgsz)

    if half:
        model.half()  # to FP16


    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)
    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=augment_inf)[0]

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=augment_inf)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)
        t3 = time_synchronized()


        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    print('class', int(cls), 'position', int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]))
                    if view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

                    if color == 'yellow' and int(cls) == 1:
                        point1_x = int(xyxy[0])
                        point1_y = int(xyxy[1])
                        point2_x = int(xyxy[2])
                        point2_y = int(xyxy[3])
                        print('yellow!!!')
                    
                    elif color == 'red'and int(cls) == 2:
                        point1_x = int(xyxy[0])
                        point1_y = int(xyxy[1])
                        point2_x = int(xyxy[2])
                        point2_y = int(xyxy[3]) 

                    elif color == 'black' and int(cls) == 0:
                        point1_x = int(xyxy[0])
                        point1_y = int(xyxy[1])
                        point2_x = int(xyxy[2])
                        point2_y = int(xyxy[3])          


                    # cv2.line(frame, (int(x_benchmark), 0), (int(x_benchmark), int(height)), (0, 0, 255), 5)
                    # cv2.rectangle(frame, (int(point1_x), int(point1_y)), (int(point2_x), int(point2_y)), (0, 255, 0), 2)
                    # cv2.imshow('frame', frame)
                    if (point1_x + point2_x)/2 == x_benchmark:
                        #TODO
                        #stretch the arm and grip the fruit
                        return True
                    else: return False

            # Print time (inference + NMS)
            # print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

            # Stream results
            if view_img:
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond



# if __name__ == '__main__':
#     # if color_sign_recog() == True:
#     #     # break 掉 while true的迴圈
#     #     pass
#     fruit_recog('yellow')