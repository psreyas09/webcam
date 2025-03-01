import cv2
import pandas as pd

# Load color data from CSV
csv_path = "colors.csv"  # Ensure this file exists in the same folder
colors = pd.read_csv(csv_path)

# Ensure RGB values are integers
colors["R"] = colors["R"].astype(int)
colors["G"] = colors["G"].astype(int)
colors["B"] = colors["B"].astype(int)

# Function to find the closest color match
def get_color_name(r, g, b):
    min_dist = float("inf")
    color_name = "Unknown"

    for index, row in colors.iterrows():
        dist = abs(int(r) - row["R"]) + abs(int(g) - row["G"]) + abs(int(b) - row["B"])
        if dist < min_dist:
            min_dist = dist
            color_name = row["color_name"]
    
    return color_name

# Initialize global variables
r, g, b = 0, 0, 0
color_name = "Unknown"

# Mouse event callback function
def draw_function(event, x, y, flags, param):
    global r, g, b, color_name
    if event == cv2.EVENT_MOUSEMOVE:
        b, g, r = frame[y, x]
        b, g, r = int(b), int(g), int(r)  # Convert to integers
        color_name = get_color_name(r, g, b)

# Open webcam
cap = cv2.VideoCapture(0)

# Create window and set mouse callback
cv2.namedWindow("Color Detector")
cv2.setMouseCallback("Color Detector", draw_function)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show the detected color
    text = f"Color: {color_name} (R: {r}, G: {g}, B: {b})"
    cv2.rectangle(frame, (0, 0), (600, 40), (int(b), int(g), int(r)), -1)  # Convert to integers
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Color Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
