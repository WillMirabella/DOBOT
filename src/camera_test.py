"""
Camera Test Script
Tests USB camera connection and displays live feed with object detection capabilities.
Press 'q' to quit, 's' to save a test image, 'b' to toggle background subtraction.
"""

import cv2
import numpy as np
from datetime import datetime
import os


def test_camera(camera_index=0, width=1280, height=720):
    """
    Test camera connection and display live feed.

    Args:
        camera_index: Camera device index (0 for default camera)
        width: Desired frame width
        height: Desired frame height
    """
    print(f"Attempting to connect to camera {camera_index}...")

    # Initialize camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"ERROR: Could not open camera {camera_index}")
        print("Try different camera indices: 0, 1, 2, etc.")
        return

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Get actual resolution (might differ from requested)
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"✓ Camera connected successfully!")
    print(f"Resolution: {actual_width}x{actual_height}")
    print(f"FPS: {fps}")
    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save current frame")
    print("  'b' - Toggle background subtraction (for object detection)")
    print("  'c' - Toggle contour detection")
    print("  'r' - Reset background")

    # Create output directory for saved images
    os.makedirs("data/raw", exist_ok=True)

    # Background subtraction setup
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500, varThreshold=16, detectShadows=True
    )
    show_bg_subtraction = False
    show_contours = False
    background_learned = False

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Failed to grab frame")
            break

        frame_count += 1
        display_frame = frame.copy()

        # Apply background subtraction if enabled
        if show_bg_subtraction or show_contours:
            fg_mask = bg_subtractor.apply(frame)

            # Remove shadows (they appear as gray in the mask)
            _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)

            # Clean up noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

            if show_contours:
                # Find contours
                contours, _ = cv2.findContours(
                    fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                # Draw contours and bounding boxes for significant objects
                for contour in contours:
                    area = cv2.contourArea(contour)

                    # Filter small noise (adjust threshold as needed)
                    if area > 500:  # Minimum area in pixels
                        # Get bounding box
                        x, y, w, h = cv2.boundingRect(contour)

                        # Draw bounding box
                        cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                        # Calculate center point
                        cx = x + w // 2
                        cy = y + h // 2
                        cv2.circle(display_frame, (cx, cy), 5, (0, 0, 255), -1)

                        # Display info
                        text = f"Area: {int(area)} | Pos: ({cx},{cy})"
                        cv2.putText(
                            display_frame, text, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                        )

            if show_bg_subtraction:
                # Show the foreground mask alongside original
                fg_mask_colored = cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)
                display_frame = np.hstack([display_frame, fg_mask_colored])

        # Add info overlay
        info_text = f"Frame: {frame_count} | Press 'q' to quit"
        cv2.putText(
            display_frame, info_text, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

        if show_bg_subtraction:
            cv2.putText(
                display_frame, "BG Subtraction: ON", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
            )

        if show_contours:
            cv2.putText(
                display_frame, "Contour Detection: ON", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
            )

        # Display frame
        cv2.imshow('Camera Test - DOBOT Vision System', display_frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("\nQuitting...")
            break

        elif key == ord('s'):
            # Save current frame
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Image saved: {filename}")

        elif key == ord('b'):
            # Toggle background subtraction
            show_bg_subtraction = not show_bg_subtraction
            if show_bg_subtraction:
                print("Background subtraction: ON")
            else:
                print("Background subtraction: OFF")

        elif key == ord('c'):
            # Toggle contour detection
            show_contours = not show_contours
            if show_contours:
                show_bg_subtraction = False  # Contours include bg subtraction
                print("Contour detection: ON")
            else:
                print("Contour detection: OFF")

        elif key == ord('r'):
            # Reset background model
            bg_subtractor = cv2.createBackgroundSubtractorMOG2(
                history=500, varThreshold=16, detectShadows=True
            )
            print("Background model reset")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✓ Camera test completed. Total frames: {frame_count}")


def list_available_cameras(max_test=5):
    """
    Test and list all available camera indices.

    Args:
        max_test: Maximum number of camera indices to test
    """
    print("Scanning for available cameras...")
    available = []

    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"  Camera {i}: Available ({width}x{height})")
            cap.release()

    if not available:
        print("  No cameras found!")

    return available


if __name__ == "__main__":
    print("="*50)
    print("DOBOT Vision System - Camera Test")
    print("="*50)
    print()

    # First, list available cameras
    available_cameras = list_available_cameras()

    if available_cameras:
        print(f"\nUsing camera {available_cameras[0]}...")
        print()
        test_camera(camera_index=available_cameras[0])
    else:
        print("\nERROR: No cameras detected!")
        print("Troubleshooting:")
        print("  1. Check USB connection")
        print("  2. Try a different USB port")
        print("  3. Check camera permissions")
        print("  4. Verify camera works in other applications")
