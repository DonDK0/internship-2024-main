from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")


def draw_boxes(frame, boxes):
    """Draw detected bounding boxes on image frame"""
    annotator = Annotator(frame)
    if boxes:
        # Create annotator object
        for box in boxes:
            class_id = box.cls
            class_name = model.names[int(class_id)]
            coordinator = box.xyxy[0]
            confidence = box.conf

        # Draw bounding box
        annotator.box_label(
            box=coordinator, label=class_name, color=colors(class_id, True)
        )

    return annotator.result()


def detect_object(frame):
    """Detect object from image frame"""
    # Detect object from image frame
    results = model.predict(frame, classes=[15], imgsz=320, iou=0.5,max_det=5, conf=0.5)
    for result in results:
        frame = draw_boxes(frame, result.boxes)

    return frame


if __name__ == "__main__":
    video_path = "CatZoomies.mp4"
    cap = cv2.VideoCapture(video_path)

    # Define the codec and create VideoWriter object
    video_writer = cv2.VideoWriter(
        video_path + "_demo.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (1280, 720)
    )

    while cap.isOpened():
        # Read image frame
        ret, frame = cap.read()

        if ret:
            # Detect motorcycle from image frame
            frame_result = detect_object(frame)
            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (750, 25) 
            fontScale = 1
            color = (0, 0, 255) 
            thickness = 2
            frame = cv2.putText(frame, 'Don-Clicknext-Internship-2024', org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 
            # Write result to video
            # video_writer.write(frame_result)

            # Show result
            cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
            cv2.imshow("Video", frame_result)
            cv2.waitKey(30)

        else:
            break

    # Release the VideoCapture object and close the window
    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()
