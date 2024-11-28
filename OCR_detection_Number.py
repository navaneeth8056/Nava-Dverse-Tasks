import cv2
import pytesseract
import numpy as np
import queue
import threading
# Set the path to tesseract executable (adjust for your environment)
# For Windows: 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# For Linux/Mac, you can skip this or ensure it's installed in the PATH.
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Update this path as per your installation

# Global queue for frames to process
frame_queue = queue.Queue(maxsize=5)  # Limit the queue size to prevent memory issues
detected_numbers = []  # To store detected numbers
max_buffer_size = 10  # Number of frames to consider for averaging the result

def preprocess_frame(frame):
    """Apply preprocessing to improve OCR accuracy."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Resize the frame to a smaller resolution for faster processing
    resized = cv2.resize(gray, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # Adaptive thresholding for better accuracy in variable lighting
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    return thresh

def extract_number_from_frame(frame):
    """Extract number from the frame using pytesseract OCR."""
    custom_config = r'--oem 3 --psm 6 outputbase digits'  # Use LSTM engine for better accuracy
    text = pytesseract.image_to_string(frame, config=custom_config)
    return text.strip()

def capture_video():
    """Thread function to capture video frames."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Only push new frames if the queue is not full
        if not frame_queue.full():
            frame_queue.put(frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def process_frames():
    """Thread function to process frames and perform OCR."""
    global detected_numbers

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            # Define a region of interest (ROI) for number detection (adjust as per your sheet layout)
            roi = frame[100:400, 200:600]  # Adjust based on your sheet's number location

            # Preprocess the ROI for better OCR accuracy
            processed_frame = preprocess_frame(roi)

            # Extract the number from the processed frame
            detected_number = extract_number_from_frame(processed_frame)

            # Only add valid detected numbers (filter out garbage or empty strings)
            if detected_number.isdigit():
                detected_numbers.append(detected_number)

            # Maintain a buffer of detected numbers and average the results
            if len(detected_numbers) > max_buffer_size:
                detected_numbers.pop(0)  # Keep the buffer size fixed

            # Determine the most common detected number (for robustness over multiple frames)
            if detected_numbers:
                most_common_number = max(set(detected_numbers), key=detected_numbers.count)
            else:
                most_common_number = "Detecting..."

            # Display the detected number on the original frame
            cv2.putText(frame, f"Detected Number: {most_common_number}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Display the frame with detected number
            cv2.imshow('Real-time Number Detection', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    # Create two threads: one for video capture and one for processing
    capture_thread = threading.Thread(target=capture_video)
    process_thread = threading.Thread(target=process_frames)

    # Start both threads
    capture_thread.start()
    process_thread.start()

    # Wait for both threads to finish
    capture_thread.join()
    process_thread.join()

    # Destroy all OpenCV windows after the threads have finished
    cv2.destroyAllWindows()
