# image_processing.py

import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import cv2
from rembg import remove
from PIL import Image

model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

def preProcessWatchImage(watch_image_path):
    print("Here in Pre Processing")
    watch_image = cv2.imread(watch_image_path)
    removedBackGround = remove(watch_image)
    print("Checkpoint 1")
    height, width, _ = removedBackGround.shape

    print("Checkpoint 2")
    # Define the cropping margin (how much to crop from top and bottom)
    crop_margin = int(height * 0.13)  # Cropping 10% from top and bottom

    # Crop the image
    print("Checkpoint 3")
    cropped_watch_image = removedBackGround[crop_margin:height-crop_margin, 0:width]
    print("Checkpoint 4")
    return cropped_watch_image


#code to detect wrist
#wrist image comes here
def detect_wrist(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = F.to_tensor(image).unsqueeze(0)
    confidence_threshold = 0.15

    with torch.no_grad():
        prediction = model(image_tensor)

    boxes = prediction[0]['boxes'].cpu().numpy()
    labels = prediction[0]['labels'].cpu().numpy()

    scores = prediction[0]['scores'].cpu().numpy()

    wrist_boxes = [box for box, label, score in zip(boxes, labels, scores) if score > confidence_threshold]

    wrist_box = wrist_boxes[0] if wrist_boxes else None
    
    print()

    return wrist_boxes


#Overlay watch

def overlay_watch(wrist_boxes, wrist_image_path, watch_image):
    print("OVERLAY WATCH")
    wrist_image = cv2.imread(wrist_image_path)
    #watch_image = cv2.imread(watch_image_path)
    
    if not wrist_boxes:
        print("Wrist not detected.")
        return wrist_image
    print("HERE IN OVERLAY WATCH")
    wrist_boxes.sort(key=lambda box: (box[2] - box[0]) * (box[3] - box[1]), reverse=True)
    largest_wrist_box = wrist_boxes[0]

    print("Checkpoint 1 ")
    # Prepare the wrist image where we will overlay the watch
    wrist_image_with_box = wrist_image.copy()  # Copy of the wrist image to modify
    
    # Read the image data
    #image_data = wrist_image.read()

    # Create a copy of the image data
    #wrist_image_with_box = BytesIO(image_data)

    print("Checkpoint 2 ")
    # Calculate scale factor to resize watch to fit within the wrist box width
    wrist_width = largest_wrist_box[2] - largest_wrist_box[0]
    scale_factor = 0.23 * wrist_width / watch_image.shape[1]  # Adjusted scale factor

    print("Checkpoint 3 ")
    # Resize watch image to fit the wrist box
    watch_image_resized = cv2.resize(watch_image, (int(watch_image.shape[1] * scale_factor), int(watch_image.shape[0] * scale_factor)),
                                     interpolation=cv2.INTER_AREA)

    print("Checkpoint 4 ")
    # Calculate offsets to place the watch image exactly on the wrist box
    x_offset = int(largest_wrist_box[0] + (wrist_width - watch_image_resized.shape[1]) / 2)
    vertical_shift = int((largest_wrist_box[3] - largest_wrist_box[1]) * 0.07)
    y_offset = int(largest_wrist_box[1] + ((largest_wrist_box[3] - largest_wrist_box[1] - watch_image_resized.shape[0]) / 2) - vertical_shift)

    # Loop over the resized watch image to blend it with the wrist image
    if watch_image.shape[2] == 4:  # Check if watch image has an alpha channel
        for y in range(watch_image_resized.shape[0]):
            for x in range(watch_image_resized.shape[1]):
                if y + y_offset >= wrist_image.shape[0] or x + x_offset >= wrist_image.shape[1]:
                    continue
                alpha = watch_image_resized[y, x, 3] / 255.0
                if alpha > 0:
                    for c in range(3):  # Ensuring proper channel-wise blending
                        wrist_image_with_box[y + y_offset, x + x_offset, c] = \
                            (alpha * watch_image_resized[y, x, c] + (1 - alpha) * wrist_image_with_box[y + y_offset, x + x_offset, c])
    else:  # If no alpha channel, use simple overlay
        for y in range(watch_image_resized.shape[0]):
            for x in range(watch_image_resized.shape[1]):
                if y + y_offset < wrist_image.shape[0] and x + x_offset < wrist_image.shape[1]:
                    wrist_image_with_box[y + y_offset, x + x_offset] = watch_image_resized[y, x]

    return wrist_image_with_box