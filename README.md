# 👤 Face Detection 

An interactive **Computer Vision web application** built using **Python, OpenCV, NumPy, Pillow, and Streamlit**.

This project demonstrates different face analysis approaches through visual processing, pixel inspection, mathematical calculations, and processed image results.



# 🚀 Live Demo

https://face-detection-n7fkiewgnnds6q2srdtamm.streamlit.app/

---

# 📌 Features

- 🖼️ Default human portrait
- 📤 Upload your own image
- 🔎 Multiple face analysis operations
- 🔬 Interactive pixel inspection
- 🎨 RGB and grayscale pixel analysis
- 🧮 Mathematical operation calculations
- 🖼️ Processed output visualization
- 📊 Image dimensions and pixel statistics
- ✨ Final analysis result

---

# 🔍 Available Operations

# 1. Template Matching

Template Matching is used to locate a known visual pattern inside an image.

The application:

- Detects a face region
- Uses the detected region as a template
- Compares the template with the image
- Calculates a similarity score
- Displays the best matching location

Formula:

R(x,y) = TM_CCOEFF_NORMED(T,I)

---

# 2. Viola-Jones Algorithm

The Viola-Jones approach is a classical method for face detection.

The application demonstrates:

- Grayscale conversion
- Integral image
- Haar-like features
- AdaBoost concept
- Cascade classifier
- Face detection

Grayscale conversion:

Gray = 0.299R + 0.587G + 0.114B

Integral Image:

II(x,y) = Σ I(i,j)

---

# 3. DeepFace

This section demonstrates the concept of deep-learning based facial representation.

The application shows:

- Face detection
- Face region extraction
- Face area calculation
- Face area ratio
- Deep feature representation concept
- Similarity calculation concept

---

# 4. FaceNet

This section demonstrates the concept of face embeddings.

The application shows:

- Face detection
- Face crop
- Face normalization concept
- Embedding generation concept
- Numerical face representation
- Euclidean distance concept

Formula:

d(A,B) = √Σ(Aᵢ − Bᵢ)²

---

# 🔬 Pixel Inspection

The application allows the user to select an individual pixel using its:

- X coordinate
- Y coordinate

For the selected pixel, the application displays:

- Red value
- Green value
- Blue value
- Grayscale intensity
- Pixel coordinate
- Grayscale calculation

Grayscale formula:

Gray = 0.299R + 0.587G + 0.114B

---

# 📊 Image Analysis

The application displays basic image information such as:

| Metric | Description |
|---|---|
| Image Width | Width of the image in pixels |
| Image Height | Height of the image in pixels |
| Total Pixels | Width × Height |
| Channels | Number of image channels |

---

# 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **OpenCV**
- **NumPy**
- **Pillow**
- **HTML/CSS**

---

# 📁 Project Structure

```text
face-detection/
│
├── app.py
├── requirements.txt
└── README.md
