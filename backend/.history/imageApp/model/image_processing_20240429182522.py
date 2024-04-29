# image_processing.py

import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import cv2
import numpy as np
from rembg import remove
from PIL import Image

model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

#code to detect wrist

def detect_wrist(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = F.to_tensor(image).unsqueeze(0)
    confidence_threshold = 0.15

    with torch.no_grad():
        prediction = model(image_tensor)

    boxes = prediction[0]['boxes'].cpu().numpy()
    labels = prediction[0]['labels'].cpu().numpy()
    scores = prediction[0]['scores'].cpu().numpy()

    # Filter out based on confidence threshold and wrist class label (replace 1 with your actual class label for wrists)
    wrist_boxes = [box for box, label, score in zip(boxes, labels, scores) if score > confidence_threshold]

    # Assuming there's only one wrist detected, get its bounding box
    wrist_box = wrist_boxes[0] if wrist_boxes else None
    
    print("Here in Detect Wrist")
    print(wrist_box)
    
    return wrist_box

def overlay_watch(wrist_box, wrist_image_path, watch_image_path, output_path="output.jpg"):
    # Detect the wrist area
    wrist_box = detect_wrist(wrist_image_path)

    if wrist_box is None:
        print("Wrist not detected.")
        return

    # Load images
    image = cv2.imread(wrist_image_path)
    watch_image = cv2.imread(watch_image_path)
    
    wrist_boxes.sort(key=lambda box: (box[2] - box[0]) * (box[3] - box[1]))
    smallest_wrist_box = wrist_boxes[0]
    
    print("Here in Overlay watch")
    #print(image)
    #print(watch_image)
    # Resize watch image to fit the wrist box
    watch_h, watch_w, _ = watch_image.shape
    scale_factor = min(wrist_box[2] - wrist_box[0], wrist_box[3] - wrist_box[1]) / max(watch_h, watch_w)
    watch_image = cv2.resize(watch_image, (int(watch_w * scale_factor), int(watch_h * scale_factor)))

    # Overlay watch image on the wrist area
    x_offset = int(wrist_box[0] + (wrist_box[2] - wrist_box[0] - watch_image.shape[1]) / 2)
    y_offset = int(wrist_box[1] + (wrist_box[3] - wrist_box[1] - watch_image.shape[0]) / 2)

    # Check if watch image has an alpha channel
    if watch_image.shape[2] == 3:  # No alpha channel
        image[y_offset:y_offset + watch_image.shape[0], x_offset:x_offset + watch_image.shape[1]] = watch_image
    else:  # Watch image has an alpha channel
        for c in range(0, 3):
            image[y_offset:y_offset + watch_image.shape[0], x_offset:x_offset + watch_image.shape[1], c] = (
                image[y_offset:y_offset + watch_image.shape[0], x_offset:x_offset + watch_image.shape[1], c] *
                (1 - watch_image[:, :, 3] / 255.0) +
                watch_image[:, :, c] * (watch_image[:, :, 3] / 255.0)
            )

    # Save the result image
    print("2nd fn")
    #print(f"result image: {image}")
    cv2.imwrite(output_path, image)
    return output_path, image