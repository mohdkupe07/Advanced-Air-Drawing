import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            # FIX: Lowered from 0.7 to 0.5.
            # A confidence threshold of 0.7 is too strict for a low-light or
            # low-resolution webcam (640×480, dim room).  MediaPipe often
            # scores valid detections at 0.55–0.65 under these conditions and
            # silently discards them, making the hand "invisible" to the app.
            # 0.5 is the recommended starting point for real-world webcams.
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.mp_draw  = mp.solutions.drawing_utils
        # FIX: store an empty result so find_position() never crashes on the
        # first frame before find_hands() has been called even once.
        self.results  = None

    def find_hands(self, img, draw=True):
        # MediaPipe requires RGB input
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return img

    def find_position(self, img):
        landmarks = []

        # FIX: guard against find_position() being called before find_hands()
        # (self.results would be None and crash with AttributeError).
        if self.results is None:
            return landmarks

        if self.results.multi_hand_landmarks:

            hand    = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape

            for idx, lm in enumerate(hand.landmark):
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                landmarks.append([idx, cx, cy])

        return landmarks