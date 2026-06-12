class GestureController:

    @staticmethod
    def fingers_up(landmarks):

        fingers = []

        # ── Thumb ──────────────────────────────────────────────────────────
        # FIX: The frame is horizontally flipped with cv2.flip(frame, 1).
        # After flipping, the RIGHT hand's thumb tip (landmark 4) sits to the
        # RIGHT of landmark 3 on screen (higher x value), not to the left.
        # Original code used `landmarks[4][1] < landmarks[3][1]` which is the
        # rule for an UNMIRRORED frame — it was always returning 0 for a normal
        # right hand, breaking every gesture that depends on the thumb state.
        #
        # Fix: flip the comparison so thumb-up → landmark 4 x > landmark 3 x.
        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)   # thumb is open / extended
        else:
            fingers.append(0)   # thumb is closed

        # ── Index, Middle, Ring, Pinky ─────────────────────────────────────
        # For vertical fingers the tip y-coordinate is LESS than the pip
        # (two joints below) when the finger is raised (y increases downward).
        # This logic was already correct — no change needed here.
        tip_ids = [8, 12, 16, 20]

        for tip in tip_ids:
            if landmarks[tip][2] < landmarks[tip - 2][2]:
                fingers.append(1)   # finger is up
            else:
                fingers.append(0)   # finger is down

        return fingers

    @staticmethod
    def detect_mode(fingers):

        # DRAW: only index finger raised  →  [0, 1, 0, 0, 0]
        if fingers == [0, 1, 0, 0, 0]:
            return "DRAW"

        # SELECT: index + middle raised  →  [0, 1, 1, 0, 0]
        elif fingers == [0, 1, 1, 0, 0]:
            return "SELECT"

        # THICKNESS: thumb + index raised  →  [1, 1, 0, 0, 0]
        elif fingers == [1, 1, 0, 0, 0]:
            return "THICKNESS"

        # ERASE: fist (all fingers closed)  →  [0, 0, 0, 0, 0]
        elif fingers == [0, 0, 0, 0, 0]:
            return "ERASE"

        # CLEAR: all four fingers raised (thumb state ignored)
        # fingers[1:] covers index, middle, ring, pinky
        elif fingers[1:] == [1, 1, 1, 1]:
            return "CLEAR"

        return "NONE"