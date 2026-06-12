import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import cv2
import numpy as np
import math
from hand_tracker import HandTracker
from gesture_controller import GestureController

# ── Global drawing state ──────────────────────────────────────────────────────
xp, yp = 0, 0                    # previous fingertip position for line drawing

# FIX: canvas is created AFTER we know the real frame size (see main()).
# Declaring it here as None so the rest of the module can reference it.
canvas = None

draw_color = (255, 0, 255)       # default colour: purple

brush_thickness = 10
eraser_thickness = 50

# FIX: frame dimensions are populated once the camera is open.
# Using module-level variables so draw_toolbar() and main() share them.
FRAME_W = 1280   # will be overwritten with the camera's actual width
FRAME_H = 720    # will be overwritten with the camera's actual height


# ── Toolbar ───────────────────────────────────────────────────────────────────

def draw_toolbar(frame):
    """Draw the colour-picker toolbar at the top of the frame.

    FIX: box_width is now calculated from FRAME_W (the real camera width)
    instead of the hard-coded value 1280, so the toolbar always spans the
    full frame regardless of actual capture resolution.
    """

    colors = [
        ((255, 0, 255), "Purple"),
        ((255, 0, 0),   "Blue"),
        ((0, 255, 0),   "Green"),
        ((0, 0, 255),   "Red"),
        ((0, 255, 255), "Yellow"),
        ((0, 165, 255), "Orange"),
        ((255, 255, 0), "Cyan"),
        ((255, 255, 255),"White"),
        ((0, 0, 0),     "Black"),
    ]

    # FIX: use FRAME_W so tile widths match the actual frame, not 1280.
    box_width = FRAME_W // len(colors)

    for i, (color, name) in enumerate(colors):

        x1 = i * box_width
        x2 = (i + 1) * box_width

        cv2.rectangle(frame, (x1, 0), (x2, 80), color, -1)

        text_color = (0, 0, 0)
        if color == (0, 0, 0):           # black tile → white label
            text_color = (255, 255, 255)

        cv2.putText(frame, name,
                    (x1 + 10, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    text_color, 2)

    return frame


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():

    # Bring module-level variables into scope for writing
    global xp, yp
    global canvas
    global brush_thickness
    global draw_color
    global FRAME_W, FRAME_H          # FIX: need to update these after open()

    cap = cv2.VideoCapture(0)

    # Request a preferred resolution.  Many cameras don't honour these values
    # and silently fall back to a different size.  We always read the ACTUAL
    # size afterwards so every array we create matches the real frame.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # FIX: read back the resolution the camera actually agreed to use.
    FRAME_W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    FRAME_H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[INFO] Camera resolution: {FRAME_W}×{FRAME_H}")

    # FIX: create the canvas with the REAL frame dimensions, not hard-coded
    # (720, 1280).  If the camera gave us 640×480, the canvas is now 480×640,
    # which matches every frame that comes out of cap.read().
    canvas = np.zeros((FRAME_H, FRAME_W, 3), np.uint8)

    # Colour list used for both toolbar rendering and index→colour lookup.
    # Kept here so SELECT logic uses the same list as draw_toolbar().
    COLORS = [
        (255, 0, 255),    # Purple
        (255, 0, 0),      # Blue
        (0, 255, 0),      # Green
        (0, 0, 255),      # Red
        (0, 255, 255),    # Yellow
        (0, 165, 255),    # Orange
        (255, 255, 0),    # Cyan
        (255, 255, 255),  # White
        (0, 0, 0),        # Black (eraser-like; clears canvas pixels)
    ]

    detector = HandTracker()

    while True:

        success, frame = cap.read()
        if not success:
            break

        # Mirror the frame so it behaves like a mirror / whiteboard
        frame = cv2.flip(frame, 1)

        # FIX: safety guard – if for any reason the captured frame has a
        # different size than expected (e.g., mid-stream resolution change),
        # resize it so all subsequent operations stay consistent.
        if frame.shape[1] != FRAME_W or frame.shape[0] != FRAME_H:
            frame = cv2.resize(frame, (FRAME_W, FRAME_H))

        # Draw the colour-picker toolbar on the live frame
        frame = draw_toolbar(frame)

        # Run MediaPipe / hand detection
        frame = detector.find_hands(frame)
        landmarks = detector.find_position(frame)

        if landmarks:

            # Index fingertip (landmark 8) – primary pointer
            x1, y1 = landmarks[8][1], landmarks[8][2]

            fingers = GestureController.fingers_up(landmarks)
            mode    = GestureController.detect_mode(fingers)

            # ── COLOUR SELECTION ──────────────────────────────────────────
            # Triggered when the hand is in SELECT mode and the fingertip is
            # inside the toolbar strip (y < 80 px from the top).
            if mode == "SELECT" and y1 < 80:

                # FIX: box_width uses FRAME_W to match the toolbar tiles.
                box_width = FRAME_W // len(COLORS)
                selected  = x1 // box_width

                if selected < len(COLORS):
                    draw_color = COLORS[selected]

                # Reset previous position so no stray line is drawn next frame
                xp, yp = 0, 0

            # ── HUD overlays ─────────────────────────────────────────────
            cv2.putText(frame, f"Mode: {mode}",
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            cv2.putText(frame, f"Thickness: {brush_thickness}",
                        (20, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)

            # ── DRAW ─────────────────────────────────────────────────────
            if mode == "DRAW":

                # Visual cursor on the live frame
                cv2.circle(frame, (x1, y1), 15, draw_color, cv2.FILLED)

                # On the very first draw stroke, seed the previous position
                # so we don't get a line from (0,0) to the fingertip.
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # Draw the line segment onto the persistent canvas
                cv2.line(canvas, (xp, yp), (x1, y1),
                         draw_color, brush_thickness)

                xp, yp = x1, y1

            # ── THICKNESS CONTROL ────────────────────────────────────────
            elif mode == "THICKNESS":

                # Thumb tip (landmark 4) acts as the second anchor point
                tx, ty = landmarks[4][1], landmarks[4][2]

                # Visual feedback: dots on each fingertip + connecting line
                cv2.circle(frame, (tx, ty), 10, (0, 255, 255), cv2.FILLED)
                cv2.line(frame, (tx, ty), (x1, y1), (0, 255, 255), 3)

                # Map the Euclidean distance between the two fingertips to a
                # brush thickness range [5, 40].
                distance = math.hypot(x1 - tx, y1 - ty)

                new_thickness = int(
                    np.interp(distance, [40, 180], [5, 40])
                )

                # Exponential moving average keeps thickness changes smooth
                brush_thickness = int(
                    0.8 * brush_thickness + 0.2 * new_thickness
                )

                # Reset so no drawing happens during thickness adjustment
                xp, yp = 0, 0

            # ── ERASER ───────────────────────────────────────────────────
            elif mode == "ERASE":

                # Red dot shows the eraser position on the live frame
                cv2.circle(frame, (x1, y1), 20, (0, 0, 255), cv2.FILLED)

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # Erase by painting black (0,0,0) onto the canvas
                cv2.line(canvas, (xp, yp), (x1, y1),
                         (0, 0, 0), eraser_thickness)

                xp, yp = x1, y1

            # ── CLEAR CANVAS ─────────────────────────────────────────────
            elif mode == "CLEAR":

                # FIX: recreate canvas with REAL dimensions, not hard-coded.
                canvas = np.zeros((FRAME_H, FRAME_W, 3), np.uint8)
                xp, yp = 0, 0

            else:
                # Any unrecognised mode: just reset the drawing cursor
                xp, yp = 0, 0

        else:
            # No hand detected – reset cursor to avoid ghost strokes
            xp, yp = 0, 0

        # ── Composite the canvas onto the live frame ──────────────────────
        #
        # Strategy:
        #   1. Convert canvas to greyscale and threshold to get a binary mask.
        #   2. Invert that mask → drawn pixels become BLACK in `inv`,
        #      background becomes WHITE.
        #   3. bitwise_AND the live frame with `inv` → punches holes in the
        #      frame wherever something is drawn (masks out the webcam pixels).
        #   4. bitwise_OR the result with canvas → fills those holes with the
        #      actual canvas colours.
        #
        # FIX: all three arrays (frame, inv, canvas) now have the same shape
        # because canvas and FRAME_W/FRAME_H are derived from the actual
        # capture resolution, eliminating the (-209) size-mismatch crash.

        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

        _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        # Convert single-channel mask back to 3-channel so shapes match frame
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

        # Mask out the webcam pixels where the canvas has content
        frame = cv2.bitwise_and(frame, inv)

        # Overlay the canvas content onto the masked frame
        frame = cv2.bitwise_or(frame, canvas)

        cv2.imshow("Advanced Air Whiteboard", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Keyboard shortcut to clear the canvas (FIX: dynamic size)
            canvas = np.zeros((FRAME_H, FRAME_W, 3), np.uint8)

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()