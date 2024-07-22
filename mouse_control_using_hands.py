import cv2
import mediapipe as mp
import pyautogui

capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Camera is not opened.")
    exit()

dragging = False
x1 = y1 = x2 = y2 = 0

try:
    while True:
        ret, image = camera.read()
        if not ret or image is None:
            continue

        image_height, image_width, _ = image.shape
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output_hands = capture_hands.process(rgb_image)

        all_hands = output_hands.multi_hand_landmarks
        if all_hands:
            for hand in all_hands:
                drawing_option.draw_landmarks(image, hand)
                one_hand_landmarks = hand.landmark
                thumb = middle_finger = None
                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)

                    if id == 8:  # İşaret parmağı
                        mouse_x = int(screen_width / image_width * x)
                        mouse_y = int(screen_height / image_height * y)
                        cv2.circle(image, (x, y), 10, (0, 255, 255))
                        if not dragging:
                            pyautogui.moveTo(mouse_x, mouse_y)
                        x1, y1 = x, y

                    if id == 12:  # Orta parmak
                        middle_finger = (x, y)
                        cv2.circle(image, (x, y), 10, (0, 255, 255))

                    if id == 4:  # Başparmak
                        thumb = (x, y)
                        x2, y2 = x, y
                        cv2.circle(image, (x, y), 10, (0, 255, 255))

                if thumb and middle_finger:
                    dist = ((thumb[0] - middle_finger[0]) ** 2 + (thumb[1] - middle_finger[1]) ** 2) ** 0.5
                    if dist < 40:  # Başparmak ve orta parmak yakınlaştığında
                        if not dragging:
                            pyautogui.mouseDown()
                            dragging = True
                    else:
                        if dragging:
                            pyautogui.mouseUp()
                            dragging = False

                # Eski tıklama işlevi
                dist_click = y2 - y1
                if dist_click < 40 and not dragging:
                    pyautogui.click()
                    print("clicked")

        cv2.imshow("Hand movement video capture", image)
        key = cv2.waitKey(100)
        if key == 27:
            break
finally:
    camera.release()
    cv2.destroyAllWindows()


