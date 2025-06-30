from flask import Flask, Response, render_template
import cv2
import numpy as np
import mediapipe as mp
import random
import time

app = Flask(__name__)

# === Config ===
width, height = 1280, 720
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

MAX_MAG = 50000
mag = MAX_MAG
score = 0

bullets = []
BULLET_SPEED = 15
color_1 = (0, 255, 255)
color_2 = (0, 0, 255)

powerups = []
powerup_effects = {'big': False, 'fast': False}
effect_start_time = {}
cooldown = 30
last_powerup_time = 0

powerup_types = {
    'rapid_fire': {'color': (0, 255, 255), 'effect': 'fast', 'duration': 10},
    'badi_goli': {'color': (255, 0, 0), 'effect': 'big', 'duration': 10}
}

targets = []

def new_target():
    return [random.randint(100, width - 100), random.randint(100, height - 100)]


def detect_gestures(landmarks):
    f8, f12, f16, thumb = landmarks[8], landmarks[12], landmarks[16], landmarks[4]
    d1 = np.hypot(f8.x - thumb.x, f8.y - thumb.y)
    d2 = np.hypot(f12.x - thumb.x, f12.y - thumb.y)
    d3 = np.hypot(f16.x - thumb.x, f16.y - thumb.y)
    return d1 > 0.1, d2 > 0.1 ,d3 > 0.1  # index, middle, ring


def is_hand_open(lm):
    """
    Improved hand open detection for Flask stream.
    Detects if the hand is open by checking:
    - Fingers are extended (tip.y < pip.y)
    - Thumb is spread out (x distance between tip and base)
    """
    fingers_open = 0
    tips = [8, 12, 16, 20]  # Index to pinky
    for tip in tips:
        if lm[tip].y < lm[tip - 2].y:
            fingers_open += 1

    thumb_open = abs(lm[4].x - lm[3].x) > 0.03  # Slightly relaxed threshold

    return fingers_open >= 3 and thumb_open


def is_game_over_pose(multi_hand_lms):
    if len(multi_hand_lms) < 2:
        print("Only one or no hand detected")
        return False

    open_hands = 0
    for hand in multi_hand_lms:
        lm = hand.landmark
        if is_hand_open(lm):
            open_hands += 1

    print(f"Open hands detected: {open_hands}")
    return open_hands == 2

def fire_bullet(x, y, dx, dy, color):
    bullets.append([x, y, dx * BULLET_SPEED, dy * BULLET_SPEED, color])

def drop_powerup():
    global last_powerup_time
    if time.time() - last_powerup_time >= cooldown and len(powerups) < 3:
        x = random.randint(50, width - 50)
        ptype = random.choice(list(powerup_types.keys()))
        powerups.append({'x': x, 'y': 0, 'type': ptype})
        last_powerup_time = time.time()

def generate_frames():
    global mag, score, bullets, powerups, powerup_effects, effect_start_time, targets
    game_over = False

    while True:
        ok, frame = camera.read()
        if not ok:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        screen = frame.copy()

        if not game_over:
            cv2.rectangle(screen, (0, 0), (350, 120), (30, 30, 30), -1)
            cv2.putText(screen, f"Score: {score}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(screen, f"Bullets: {mag}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)

            y = 75
            for effect in powerup_effects:
                if powerup_effects[effect] and effect in effect_start_time:
                    ptype = next((k for k, v in powerup_types.items() if v['effect'] == effect), None)
                    if ptype:
                        left = int(powerup_types[ptype]['duration'] - (time.time() - effect_start_time[effect]))
                        if left > 0:
                            cv2.putText(screen, f"{effect}: {left}s", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                            y += 20

            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(screen, hand, mp_hands.HAND_CONNECTIONS)
                    lm = hand.landmark
                    tir1, tir2, tir3 = detect_gestures(lm)



                    if results.multi_hand_landmarks and is_game_over_pose(results.multi_hand_landmarks):
                        game_over = True


                    if tir1 and mag > 0:
                        x, y = int(lm[8].x * width), int(lm[8].y * height)
                        xb, yb = int(lm[5].x * width), int(lm[5].y * height)
                        dx, dy = x - xb, y - yb
                        norm = np.hypot(dx, dy)
                        if norm:
                            fire_bullet(x, y, dx / norm, dy / norm, color_1)
                            mag -= 1

                    if tir2 and mag > 0:
                        x, y = int(lm[12].x * width), int(lm[12].y * height)
                        xb, yb = int(lm[9].x * width), int(lm[9].y * height)
                        dx, dy = x - xb, y - yb
                        norm = np.hypot(dx, dy)
                        if norm:
                            fire_bullet(x, y, dx / norm, dy / norm, color_2)
                            mag -= 1

                    if tir3 and mag > 0:
                        x, y = int(lm[16].x * width), int(lm[16].y * height)
                        xb, yb = int(lm[13].x * width), int(lm[13].y * height)
                        dx, dy = x - xb, y - yb
                        norm = np.hypot(dx, dy)
                        if norm:
                            fire_bullet(x, y, dx / norm, dy / norm, (0, 255, 0))  # green bullet for ring finger
                            mag -= 1

            new_bullets = []
            for b in bullets:
                b[0] += int(b[2])
                b[1] += int(b[3])
                if 0 <= b[0] < width and 0 <= b[1] < height:
                    size = 10 if powerup_effects['big'] else 5
                    cv2.circle(screen, (int(b[0]), int(b[1])), size, b[4], -1)
                    new_bullets.append(b)
            bullets = new_bullets

            while len(targets) < 7:
                targets.append(new_target())

            new_targets = []
            for t in targets:
                hit = False
                for b in bullets:
                    if np.hypot(t[0] - b[0], t[1] - b[1]) < (50 if powerup_effects['big'] else 30):
                        score += 2 if powerup_effects['fast'] else 1
                        hit = True
                        break
                if not hit:
                    cv2.circle(screen, tuple(t), 30, (255, 0, 255), -1)
                    cv2.circle(screen, tuple(t), 20, (255, 255, 255), -1)
                    cv2.circle(screen, tuple(t), 10, (255, 0, 255), -1)
                    new_targets.append(t)
            targets = new_targets

            drop_powerup()
            for p in powerups:
                color = powerup_types[p['type']]['color']
                if p['type'] == 'rapid_fire':
                    cv2.rectangle(screen, (p['x'], p['y']), (p['x'] + 20, p['y'] + 20), color, -1)
                elif p['type'] == 'badi_goli':
                    cv2.circle(screen, (p['x'], p['y']), 12, color, -1)
                p['y'] += 5

            for p in powerups[:]:
                if p['y'] >= height - 50:
                    effect = powerup_types[p['type']]['effect']
                    powerup_effects[effect] = True
                    effect_start_time[effect] = time.time()
                    powerups.remove(p)

            for e in list(effect_start_time):
                ptype = next((k for k, v in powerup_types.items() if v['effect'] == e), None)
                if ptype and time.time() - effect_start_time[e] > powerup_types[ptype]['duration']:
                    powerup_effects[e] = False
                    del effect_start_time[e]

        else:
            cv2.rectangle(screen, (width//2 - 200, height//2 - 50), (width//2 + 200, height//2 + 50), (50, 50, 50), -1)
            cv2.putText(screen, f"Final Score: {score}", (width//2 - 180, height//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
            cv2.putText(screen, "Hands Up!!!", (width//2 - 150, height//2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', screen)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)

    