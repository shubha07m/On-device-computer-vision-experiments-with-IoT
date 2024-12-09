from ultralytics import YOLO

# Create a new YOLO model from scratch using the large variant
model = YOLO("yolo_phantom.yaml").load("yolov8n.pt")

# Print the model's device to ensure it's using "mps"
print(model.device)

# Load a dataset for training
# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data="coco8.yaml", epochs=3, device="mps")

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model("https://ultralytics.com/images/bus.jpg")

# Export the model to ONNX format