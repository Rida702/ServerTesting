# image_processing.py

import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import cv2
import numpy as np
from rembg import remove
from PIL import Image
from PIL import Image as PILImage
from io import BytesIO

model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

def get_image_dimensions(image):
    # Load image using PIL
    image_data = BytesIO(image.read())
    pil_image = PILImage.open(image_data)
    
    # Get dimensions
    dimensions = pil_image.size
    
    return dimensions

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
    print(wrist_boxes)
    
    return wrist_boxes

def overlay_watch(wrist_boxes, wrist_image_path, watch_image_path, output_path="output.jpg"):
    # Detect the wrist area
    print("Here in Overlay watch")
    wrist_boxes = detect_wrist(wrist_image_path)
    
    wrist_image = cv2.imread(wrist_image_path)
    watch_image = cv2.imread(watch_image_path)

    if not wrist_boxes:
        print("Wrist not detected.")
        return wrist_image
    
    wrist_boxes.sort(key=lambda box: (box[2] - box[0]) * (box[3] - box[1]))
    smallest_wrist_box = wrist_boxes[0]
    
    scale = 0.4 # Adjusted to make the watch smaller
    # Calculate scale factor to resize watch to fit within the wrist box width    
    scale_factor = scale * (smallest_wrist_box[2] - smallest_wrist_box[0]) / watch_image.shape[1]
    
    # Resize watch image to fit the wrist box
    watch_h, watch_w, _ = watch_image.shape
    watch_image_resized = cv2.resize(watch_image, (int(watch_w * scale_factor), int(watch_h * scale_factor)), interpolation=cv2.INTER_AREA)

    # Calculate offsets to place the watch image exactly on the wrist box
    x_offset = int(smallest_wrist_box[0] + (smallest_wrist_box[2] - smallest_wrist_box[0] - watch_image_resized.shape[1]) / 2)
    y_offset = int(smallest_wrist_box[1] + (smallest_wrist_box[3] - smallest_wrist_box[1] - watch_image_resized.shape[0]) / 2)

    # Loop over the alpha channel to blend the watch with the wrist image
    print("Here in Overlay watch 1")
    for y in range(watch_image_resized.shape[0]):
        print("Here in Overlay watch 2")
        for x in range(watch_image_resized.shape[1]):
            print("Here in Overlay watch 3")
            if y + y_offset >= wrist_image.shape[0] or x + x_offset >= wrist_image.shape[1]:
                print("Here in Overlay watch 4")
                continue  # If the watch goes outside of the wrist image bounds, skip
            alpha = watch_image_resized[y, x, 3] / 255.0
            print("Here in Overlay watch 5")
            if alpha > 0:  # If the pixel is not transparent
                print("Here in Overlay watch 6")
                wrist_image[y + y_offset, x + x_offset] = alpha * watch_image_resized[y, x, :3] + (1 - alpha) * wrist_image[y + y_offset, x + x_offset]

    # Save the result image
    print("Here in Overlay watch 22")
    cv2.imwrite(output_path, wrist_image)
    print(f"result image: {wrist_image}")
    print(f"output_path: {output_path}")
    return output_path, wrist_image