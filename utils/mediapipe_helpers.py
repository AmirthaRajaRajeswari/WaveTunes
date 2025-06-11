import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_hands_model(static_image_mode=False, max_num_hands=1, detection_conf=0.7, tracking_conf=0.5):
    return mp_hands.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=detection_conf,
        min_tracking_confidence=tracking_conf
    )
def draw_hand_landmarks(image, hand_landmarks):
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
def fingers_status(hand_landmarks):
    lm = hand_landmarks.landmark
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    fingers_open = [lm[tip].y < lm[pip].y for tip, pip in zip(tips, pips)]

    thumb_tip = lm[4]
    thumb_ip = lm[2]
    wrist = lm[0]
    thumb_open = abs(thumb_tip.x - wrist.x) > abs(thumb_ip.x - wrist.x)

    fingers_open.insert(0, thumb_open)
    return fingers_open  
def detect_gesture(finger_states, hand_landmarks):
    thumb, index, middle, ring, pinky = finger_states
    extended = sum(finger_states)

    if finger_states == [True, True, True, True, True]:
        return "open_palm"
    elif extended == 0:
        return "fist"
    elif finger_states == [True, False, False, False, False]:
        return "thumbs_up"
    elif index and extended <= 2:
        tip_x = hand_landmarks.landmark[8].x
        base_x = hand_landmarks.landmark[5].x
        if tip_x < base_x - 0.03:
            return "index_left"
        elif tip_x > base_x + 0.03:
            return "index_right"
    return "unknown"
def get_palm_center_y(hand_landmarks):
    lm = hand_landmarks.landmark
    palm_points = [lm[0], lm[1], lm[5], lm[9], lm[13], lm[17]]
    avg_y = sum(point.y for point in palm_points) / len(palm_points)
    return avg_y
