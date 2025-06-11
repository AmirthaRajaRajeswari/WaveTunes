import cv2
import time
from utils.mediapipe_helpers import (
    get_hands_model,
    draw_hand_landmarks,
    fingers_status,
    detect_gesture,
    get_palm_center_y
)
from spotify_controls import sp, play_pause, next_track, previous_track, volume_up, volume_down

print("Spotify Authenticated User:", sp.current_user()["display_name"])

hands = get_hands_model()
cap = cv2.VideoCapture(0)

last_gesture_time = 0
gesture_delay = 1 
prev_palm_y = None
volume_threshold = 0.03

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand_landmarks(frame, hand_landmarks)

            finger_states = fingers_status(hand_landmarks)
            gesture = detect_gesture(finger_states, hand_landmarks)
            current_time = time.time()

            if gesture == "open_palm":
                playback = sp.current_playback()
                if playback and playback.get("device", {}).get("is_active", False):
                    current_palm_y = get_palm_center_y(hand_landmarks)
                    if prev_palm_y is not None:
                        delta = prev_palm_y - current_palm_y
                        if abs(delta) > volume_threshold and (current_time - last_gesture_time > gesture_delay):
                            if delta > 0:
                                volume_up()
                            else:
                                volume_down()
                            last_gesture_time = current_time
                    prev_palm_y = current_palm_y
                else:
                    prev_palm_y = None
            else:
                prev_palm_y = None

            if current_time - last_gesture_time > gesture_delay:
                playback = sp.current_playback()

                if gesture == "open_palm":
                    if playback and not playback["is_playing"]:
                        play_pause()
                        last_gesture_time = current_time

                elif gesture == "fist":
                    if playback and playback["is_playing"]:
                        play_pause()
                        last_gesture_time = current_time

                elif gesture == "index_left":
                    previous_track()
                    last_gesture_time = current_time

                elif gesture == "index_right":
                    next_track()
                    last_gesture_time = current_time

    cv2.imshow("WaveTunes", frame)
    if cv2.waitKey(1) & 0xFF == 27: 
        break
cap.release()
cv2.destroyAllWindows()
