# 🎯 Alpha-Shots: Gesture Shooter Game 🎮

Welcome to the **Gesture Shooter Game**! This is a fun and interactive game controlled by hand gestures using your webcam. Shoot bullets, collect power-ups, and score big — all with just your hand movements! 🖐️💥

---

## 🚀 About The Game

This game uses **MediaPipe Hands** for real-time hand tracking and **OpenCV** for rendering the game visuals. Players control the aim and shoot bullets by making specific gestures. Different power-ups randomly appear to enhance your gameplay, making it more exciting and challenging! 🎉

---

## 🎮 Gameplay Features

- 🔫 **Shoot bullets** by pointing your index finger and making a trigger gesture.
- 🎯 **Aim marker** shows where your bullet will hit, controlled by your hand.
- 🔥 **Power-ups** randomly drop from the top:
  - 🟠 **Big Bullets**: Bullets grow bigger for 30 seconds.
  - 🔵 **Big Aim Marker**: Enlarges the aim marker for 20 seconds and gives higher points.
  - ⚡ **Double Points**: Score points twice as fast for a limited time.
- 📊 **Score UI** displays your current score and remaining bullets.
- 🎨 Cool colorful bullets and aim marker for a visually appealing experience.

---

## 🎯 How To Play

- Use your hand in front of the webcam.
- Point your index finger and simulate a trigger to shoot bullets.
- Collect power-ups that fall from the top by moving your hand over them.
- Watch your score increase and bullets decrease with each shot.
- Avoid running out of bullets or missing too many shots!

---

## 🧩 Code Structure Overview

- **Main Loop:** Captures video frames and detects hand landmarks.
- **Gesture Detection:** Recognizes finger positions to trigger shooting.
- **Bullet Mechanics:** Updates bullet position, size, and colors based on power-ups.
- **Power-ups:** Randomly spawn and apply effects like bigger bullets, bigger aim, or double points.
- **Score UI:** Displays current score and bullet count.

---

## 🎨 Screenshots

---

## 💡 Possible Improvements

- Add sound effects for shooting and power-up collection 🎵
- Introduce multiple difficulty levels 🔥
- Add animations and transitions ✨
- Implement leaderboard to track high scores 🏆


### 🛠️ Libraries Used

- **cv2**: Handles video capture and drawing graphics on the screen.
- **numpy**: Used for mathematical calculations, especially vector math for bullet directions.
- **mediapipe**: Detects hand landmarks (key points on your hand) to interpret gestures.
- **random**: Spawns power-ups randomly.
- **time**: Manages timing for power-up effects duration.

---

## 📝 License

This project is open-source and free to use under the MIT License.

---



## 🙌 Thanks for playing and feel free to contribute!

If you want to improve the game or add new features, just fork the repo and submit a pull request. Happy coding! 💻✨

---

# Made with ❤️ and 🖐️ by The Great Mohit Kumawat
