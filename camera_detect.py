import cv2
import numpy as np

def is_plus_shape(contour, approx):
    """
    Check if a contour resembles a plus shape based on specific geometry.
    """
    if len(approx) == 12:  # Plus shapes often have 12 corners after approximation
        # Calculate bounding box for width-height ratio
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check if the bounding box is more or less square
        aspect_ratio = float(w) / h
        if 0.8 < aspect_ratio < 1.2:  # The ratio for a cross should be close to 1
            return True
    return False

def get_orientation(approx, cp):

    p1 = approx[1, 0]
    p2 = approx[0, 0]

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle1 = -np.arctan2(dy, dx)
    angle1 = np.rad2deg(angle1)

    if angle1 >= 45:
        return -90 + angle1
    return angle1

def draw_line(frame, point1, point2, color=(0, 0, 255), thickness=3):
    cv2.line(frame, point1, point2, color, thickness)

def get_length(corners):
    p1 = corners[0, 0]
    p2 = corners[6, 0]

    dx = p2[0]-p1[0]
    dy = p2[1]-p1[1]
    mag = np.sqrt(dx**2 + dy**2)
    return mag

# Open the camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to detect black shapes (0) surrounded by white (255)
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop through the contours
    for contour in contours:
        # Approximate the contour to reduce the number of points
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Check if the shape is a plus/cross shape
        if is_plus_shape(contour, approx):
            # Draw the contour in green
            pixels_diagonal = get_length(approx)
            mm_per_pixel = 158.113/pixels_diagonal
            print(mm_per_pixel)
            
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 1)
            
            # Calculate and display the center of the shape
            M = cv2.moments(contour)
            cX = 0
            cY = 0
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)  # Mark the center

                # Display coordinates on the frame
                cv2.putText(frame, f"Center: ({cX}, {cY})", (cX - 20, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Calculate and display the orientation
            angle = get_orientation(approx, (cX, cY))
            cv2.putText(frame, f"Angle: {angle:.2f}", (cX + 10, cY + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the result
    cv2.imshow('Frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


