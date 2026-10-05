import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw
import urllib.request
import io
import math


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Face Detection Studio",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99, 255, 177, 0.08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(72, 149, 239, 0.07), transparent 25%),
        #0b100e;
    color: #edf5ef;
}

.block-container {
    max-width: 1500px;
    padding-top: 35px;
    padding-bottom: 80px;
}

.hero {
    border: 1px solid rgba(145, 232, 179, 0.24);
    border-radius: 28px;
    padding: 38px 42px;
    background:
        linear-gradient(
            135deg,
            rgba(22, 34, 27, 0.96),
            rgba(14, 22, 18, 0.96)
        );
    box-shadow:
        0 25px 70px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.03);
    margin-bottom: 40px;
}

.hero-small {
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    font-size: clamp(42px, 6vw, 78px);
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 0.95;
    margin: 0;
}

.hero-title span {
    color: #8ee8b4;
}

.hero-subtitle {
    margin-top: 20px;
    color: #aab8af;
    font-size: 17px;
}

.hero-pills {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 25px;
}

.pill {
    border: 1px solid rgba(142,232,180,0.25);
    background: rgba(142,232,180,0.07);
    color: #bdeecf;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 29px;
    font-weight: 800;
    margin-top: 45px;
    margin-bottom: 12px;
}

.section-line {
    width: 82px;
    height: 4px;
    border-radius: 20px;
    background: #8ee8b4;
    margin-bottom: 25px;
}

.step-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(142,232,180,0.10);
    border: 1px solid rgba(142,232,180,0.28);
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.card {
    border: 1px solid rgba(142,232,180,0.18);
    background: rgba(20,30,24,0.78);
    border-radius: 22px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 12px 40px rgba(0,0,0,0.20);
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

.card-text {
    color: #aab8af;
    line-height: 1.7;
    font-size: 14px;
}

.operation-card {
    border: 1px solid rgba(142,232,180,0.20);
    background: linear-gradient(
        145deg,
        rgba(22,34,27,0.95),
        rgba(14,22,18,0.95)
    );
    border-radius: 20px;
    padding: 23px;
    min-height: 190px;
}

.operation-number {
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    margin-bottom: 18px;
}

.operation-name {
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 10px;
}

.operation-desc {
    color: #9eaaa3;
    font-size: 13px;
    line-height: 1.6;
}

.calculation {
    border: 1px solid rgba(142,232,180,0.23);
    background: #111a15;
    border-radius: 24px;
    padding: 30px;
    margin-top: 15px;
}

.calc-label {
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.calc-step {
    padding: 15px 18px;
    border-left: 3px solid #8ee8b4;
    background: rgba(142,232,180,0.045);
    border-radius: 0 12px 12px 0;
    margin: 10px 0;
    color: #dce8df;
    line-height: 1.65;
}

.formula {
    font-family: 'DM Mono', monospace;
    color: #baf3ce;
    font-size: 15px;
}

.final-result {
    border: 1px solid rgba(142,232,180,0.42);
    border-radius: 26px;
    padding: 30px;
    background:
        linear-gradient(
            135deg,
            rgba(36,72,51,0.42),
            rgba(17,28,22,0.94)
        );
    box-shadow:
        0 0 50px rgba(142,232,180,0.07);
}

.result-title {
    color: #8ee8b4;
    font-size: 26px;
    font-weight: 800;
}

.result-value {
    font-family: 'DM Mono', monospace;
    font-size: 17px;
    color: #e8fff0;
    margin-top: 10px;
}

.metric-card {
    border: 1px solid rgba(142,232,180,0.17);
    background: rgba(20,30,24,0.8);
    border-radius: 17px;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-size: 25px;
    font-weight: 800;
    color: #8ee8b4;
}

.metric-label {
    color: #89968e;
    font-size: 12px;
    margin-top: 4px;
}

div[data-baseweb="select"] > div {
    background: #111a15 !important;
    border-color: rgba(142,232,180,0.3) !important;
    border-radius: 13px !important;
}

.stButton > button {
    border-radius: 13px;
    border: 1px solid rgba(142,232,180,0.35);
    background: rgba(142,232,180,0.09);
    color: #dfffea;
    font-weight: 700;
    min-height: 45px;
}

.stButton > button:hover {
    border-color: #8ee8b4;
    background: rgba(142,232,180,0.16);
}

.stNumberInput input {
    background: #111a15 !important;
    color: white !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #8ee8b4 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

.pixel-panel {
    border: 1px solid rgba(142,232,180,0.30);
    background:
        linear-gradient(
            145deg,
            rgba(25,40,31,0.95),
            rgba(12,20,16,0.98)
        );
    border-radius: 24px;
    padding: 26px;
    margin-top: 18px;
    box-shadow:
        0 15px 45px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.025);
}

.pixel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.pixel-title {
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    letter-spacing: 2px;
}

.pixel-badge {
    color: #baf3ce;
    background: rgba(142,232,180,0.09);
    border: 1px solid rgba(142,232,180,0.22);
    padding: 6px 11px;
    border-radius: 999px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
}

.pixel-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

.pixel-item {
    background: rgba(142,232,180,0.045);
    border: 1px solid rgba(142,232,180,0.13);
    border-radius: 15px;
    padding: 16px;
}

.pixel-label {
    color: #89968e;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.pixel-value {
    color: #e8fff0;
    font-family: 'DM Mono', monospace;
    font-size: 18px;
}

.pixel-coordinate {
    grid-column: span 3;
    border: 1px solid rgba(142,232,180,0.24);
    background: rgba(142,232,180,0.075);
}

.pixel-coordinate .pixel-value {
    color: #8ee8b4;
    font-size: 22px;
}

.pixel-formula {
    margin-top: 16px;
    padding: 17px;
    border-radius: 15px;
    border-left: 3px solid #8ee8b4;
    background: rgba(142,232,180,0.045);
}

.pixel-formula-label {
    color: #89968e;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.pixel-formula-text {
    color: #baf3ce;
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    line-height: 1.7;
}

.pixel-final {
    margin-top: 16px;
    padding: 17px;
    border-radius: 15px;
    background:
        linear-gradient(
            90deg,
            rgba(142,232,180,0.12),
            rgba(142,232,180,0.035)
        );
    border: 1px solid rgba(142,232,180,0.22);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.pixel-final-label {
    color: #aab8af;
    font-size: 13px;
}

.pixel-final-value {
    color: #8ee8b4;
    font-family: 'DM Mono', monospace;
    font-size: 18px;
}

.selected-operation-box {
    margin-top: 18px;
    padding: 18px 22px;
    border-radius: 18px;
    border: 1px solid rgba(142,232,180,0.45);
    background:
        linear-gradient(
            135deg,
            rgba(142,232,180,0.14),
            rgba(142,232,180,0.04)
        );
}

.selected-operation-label {
    color: #89968e;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    margin-bottom: 7px;
}

.selected-operation-name {
    color: #8ee8b4;
    font-size: 22px;
    font-weight: 800;
}

.selected-operation-description {
    color: #aab8af;
    font-size: 13px;
    margin-top: 6px;
}

@media (max-width: 700px) {

    .pixel-grid {
        grid-template-columns: 1fr;
    }

    .pixel-coordinate {
        grid-column: span 1;
    }

    .pixel-final {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEFAULT IMAGE
# ============================================================

IMAGE_URL = (
    "https://raw.githubusercontent.com/ageitgey/"
    "face_recognition/master/examples/obama.jpg"
)


@st.cache_data
def load_default_image():

    try:

        request = urllib.request.Request(
            IMAGE_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read()

        return Image.open(
            io.BytesIO(data)
        ).convert("RGB")

    except Exception:

        img = Image.new(
            "RGB",
            (512, 512),
            (205, 215, 220)
        )

        draw = ImageDraw.Draw(img)

        draw.rectangle(
            (215, 350, 300, 512),
            fill=(170, 115, 90)
        )

        draw.ellipse(
            (135, 70, 380, 370),
            fill=(180, 125, 98)
        )

        draw.pieslice(
            (120, 35, 395, 260),
            180,
            360,
            fill=(35, 30, 28)
        )

        draw.ellipse((190, 190, 225, 215), fill="white")
        draw.ellipse((290, 190, 325, 215), fill="white")

        draw.ellipse((202, 197, 213, 208), fill="black")
        draw.ellipse((302, 197, 313, 208), fill="black")

        draw.line(
            (260, 205, 248, 270, 270, 275),
            fill=(100, 65, 55),
            width=4
        )

        draw.arc(
            (215, 265, 310, 315),
            10,
            170,
            fill=(90, 45, 45),
            width=4
        )

        draw.polygon(
            [
                (215, 350),
                (155, 405),
                (90, 512),
                (425, 512),
                (355, 405),
                (300, 350)
            ],
            fill=(45, 70, 90)
        )

        return img


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def pil_to_cv(image):

    return cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )


def cv_to_pil(image):

    return Image.fromarray(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )
    )


def detect_faces(image_bgr):

    gray = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY
    )

    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(45, 45)
    )

    return faces


def draw_faces(
    image_bgr,
    faces,
    label="Face"
):

    result = image_bgr.copy()

    for i, (x, y, w, h) in enumerate(faces):

        cv2.rectangle(
            result,
            (x, y),
            (x + w, y + h),
            (142, 232, 180),
            3
        )

        cv2.putText(
            result,
            f"{label} {i + 1}",
            (x, max(30, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (142, 232, 180),
            2,
            cv2.LINE_AA
        )

    return result


def calculate_pixel_information(
    image_bgr,
    x,
    y
):

    height, width = image_bgr.shape[:2]

    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))

    b, g, r = image_bgr[y, x]

    gray_image = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY
    )

    gray_value = gray_image[y, x]

    return (
        int(r),
        int(g),
        int(b),
        int(gray_value)
    )


def template_match(source_bgr, template_bgr):

    source_gray = cv2.cvtColor(
        source_bgr,
        cv2.COLOR_BGR2GRAY
    )

    template_gray = cv2.cvtColor(
        template_bgr,
        cv2.COLOR_BGR2GRAY
    )

    sh, sw = source_gray.shape
    th, tw = template_gray.shape

    if th > sh or tw > sw:

        scale = min(
            sw / tw,
            sh / th
        ) * 0.8

        new_w = max(20, int(tw * scale))
        new_h = max(20, int(th * scale))

        template_gray = cv2.resize(
            template_gray,
            (new_w, new_h)
        )

        th, tw = template_gray.shape

    result = cv2.matchTemplate(
        source_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
        result
    )

    return (
        float(max_val),
        max_loc,
        (tw, th)
    )


# ============================================================
# DEEPFACE IMPORT
# ============================================================

@st.cache_resource
def load_deepface():

    from deepface import DeepFace

    return DeepFace


# ============================================================
# DEEPFACE ANALYSIS
# ============================================================

def run_deepface_analysis(image_bgr):

    DeepFace = load_deepface()

    result = DeepFace.analyze(
        img_path=image_bgr,
        actions=[
            "age",
            "gender",
            "emotion",
            "race"
        ],
        detector_backend="opencv",
        enforce_detection=True,
        silent=True
    )

    if isinstance(result, list):

        return result[0]

    return result


# ============================================================
# FACENET EMBEDDING
# ============================================================

def get_facenet_embedding(image_bgr):

    DeepFace = load_deepface()

    result = DeepFace.represent(
        img_path=image_bgr,
        model_name="Facenet",
        detector_backend="opencv",
        enforce_detection=True
    )

    if isinstance(result, list):

        result = result[0]

    return np.array(
        result["embedding"],
        dtype=np.float32
    )


# ============================================================
# FACENET COMPARISON
# ============================================================

def compare_facenet(
    image1_bgr,
    image2_bgr
):

    DeepFace = load_deepface()

    result = DeepFace.verify(
        img1_path=image1_bgr,
        img2_path=image2_bgr,
        model_name="Facenet",
        detector_backend="opencv",
        distance_metric="cosine",
        enforce_detection=True
    )

    return result


# ============================================================
# HERO
# ============================================================

st.markdown(
"""
<div class="hero">

<div class="hero-small">
INTERACTIVE COMPUTER VISION STUDIO
</div>

<div class="hero-title">
FACE <span>DETECTION</span>
</div>

<div class="hero-subtitle">
Explore facial analysis algorithms through visual processing,
pixel inspection, mathematical calculations and real-world applications.
</div>

<div class="hero-pills">

<div class="pill">
Pixel Inspection
</div>

<div class="pill">
Face Detection
</div>

<div class="pill">
Algorithm Analysis
</div>

<div class="pill">
Visual Results
</div>

</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# STEP 1 — INPUT IMAGE
# ============================================================

st.markdown(
"""
<div class="step-badge">
STEP 01
</div>

<div class="section-heading">
🖼️ Input Image
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


default_image = load_default_image()


uploaded = st.file_uploader(
    "Upload another single-person image (optional)",
    type=["jpg", "jpeg", "png"],
    help="Keep the default human portrait or upload your own.",
    key="main_image"
)


if uploaded is not None:

    input_image = Image.open(
        uploaded
    ).convert("RGB")

else:

    input_image = default_image


image_bgr = pil_to_cv(input_image)

height, width = image_bgr.shape[:2]

channels = image_bgr.shape[2]

total_pixels = width * height


st.image(
    input_image,
    caption="Default Input — Single Human Portrait"
    if uploaded is None
    else "Uploaded Input Image",
    width=350
)


# ============================================================
# IMAGE METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-number">{width}</div>
        <div class="metric-label">IMAGE WIDTH</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m2:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-number">{height}</div>
        <div class="metric-label">IMAGE HEIGHT</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-number">{total_pixels:,}</div>
        <div class="metric-label">TOTAL PIXELS</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m4:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-number">{channels}</div>
        <div class="metric-label">CHANNELS</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# STEP 2 — SELECT OPERATION
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 02
</div>

<div class="section-heading">
🔎 Select Operation
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


operations = [

    (
        "01",
        "Template Matching",
        "Upload a template image and locate the same visual pattern inside the input image."
    ),

    (
        "02",
        "Viola-Jones",
        "Actual Haar Cascade face detection using the classical Viola-Jones approach."
    ),

    (
        "03",
        "DeepFace",
        "Actual deep facial analysis including age, gender, emotion and facial representation."
    ),

    (
        "04",
        "FaceNet",
        "Generate FaceNet embeddings and compare two face images."
    )

]


cols = [c1, c2, c3, c4]


for col, operation in zip(cols, operations):

    with col:

        st.markdown(
            f"""
            <div class="operation-card">

            <div class="operation-number">
            {operation[0]}
            </div>

            <div class="operation-name">
            {operation[1]}
            </div>

            <div class="operation-desc">
            {operation[2]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)


selected_operation = st.selectbox(
    "Choose the operation to analyze",
    [
        "Template Matching",
        "Viola-Jones Algorithm",
        "DeepFace",
        "FaceNet"
    ],
    index=1
)


# ============================================================
# OPERATION-SPECIFIC INPUT
# ============================================================

template_image = None
comparison_image = None


if selected_operation == "Template Matching":

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        🎯 Template Image
        </div>

        <div class="card-text">
        Upload the image region that you want to locate inside
        the main input image.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    template_upload = st.file_uploader(
        "Upload Template Image",
        type=["jpg", "jpeg", "png"],
        key="template_upload"
    )

    if template_upload is not None:

        template_image = Image.open(
            template_upload
        ).convert("RGB")

        st.image(
            template_image,
            caption="Template Image",
            width=250
        )


elif selected_operation == "FaceNet":

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        👥 Face Comparison Image
        </div>

        <div class="card-text">
        Upload another face image. FaceNet will generate embeddings
        for both images and calculate their similarity.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    comparison_upload = st.file_uploader(
        "Upload Comparison Face Image",
        type=["jpg", "jpeg", "png"],
        key="comparison_upload"
    )

    if comparison_upload is not None:

        comparison_image = Image.open(
            comparison_upload
        ).convert("RGB")

        st.image(
            comparison_image,
            caption="Comparison Image",
            width=250
        )


# ============================================================
# SELECTED OPERATION
# ============================================================

st.markdown(
    f"""
    <div class="selected-operation-box">

    <div class="selected-operation-label">
    SELECTED OPERATION
    </div>

    <div class="selected-operation-name">
    {selected_operation}
    </div>

    <div class="selected-operation-description">
    This operation will be applied to the input image.
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COMMON FACE DETECTION
# ============================================================

faces = detect_faces(
    image_bgr
)

face_count = len(faces)

output_bgr = image_bgr.copy()


# ============================================================
# RESULT VARIABLES
# ============================================================

template_score = 0.0
template_location = (0, 0)

deepface_result = None

facenet_embedding = None
facenet_result = None


# ============================================================
# TEMPLATE MATCHING
# ============================================================

if selected_operation == "Template Matching":

    if template_image is not None:

        template_bgr = pil_to_cv(
            template_image
        )

        try:

            template_score, template_location, template_size = template_match(
                image_bgr,
                template_bgr
            )

            tw, th = template_size

            x, y = template_location

            cv2.rectangle(
                output_bgr,
                (x, y),
                (x + tw, y + th),
                (142, 232, 180),
                4
            )

            cv2.putText(
                output_bgr,
                f"Match {template_score:.3f}",
                (x, max(30, y - 12)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (142, 232, 180),
                2,
                cv2.LINE_AA
            )

        except Exception as e:

            st.error(
                f"Template Matching error: {e}"
            )

    else:

        st.info(
            "Upload a template image above to perform actual template matching."
        )


# ============================================================
# VIOLA-JONES
# ============================================================

elif selected_operation == "Viola-Jones Algorithm":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "Face"
    )


# ============================================================
# DEEPFACE
# ============================================================

elif selected_operation == "DeepFace":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "DeepFace"
    )

    try:

        deepface_result = run_deepface_analysis(
            image_bgr
        )

        if face_count > 0:

            x, y, w, h = faces[0]

            cv2.putText(
                output_bgr,
                "DeepFace Analysis",
                (
                    x,
                    min(
                        height - 20,
                        y + h + 28
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (142, 232, 180),
                2,
                cv2.LINE_AA
            )

    except Exception as e:

        deepface_result = {
            "error": str(e)
        }


# ============================================================
# FACENET
# ============================================================

else:

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "FaceNet"
    )

    try:

        facenet_embedding = get_facenet_embedding(
            image_bgr
        )

        if comparison_image is not None:

            comparison_bgr = pil_to_cv(
                comparison_image
            )

            facenet_result = compare_facenet(
                image_bgr,
                comparison_bgr
            )

        if face_count > 0:

            x, y, w, h = faces[0]

            cv2.putText(
                output_bgr,
                "FaceNet Embedding",
                (
                    x,
                    min(
                        height - 20,
                        y + h + 28
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (142, 232, 180),
                2,
                cv2.LINE_AA
            )

    except Exception as e:

        facenet_embedding = None

        facenet_result = {
            "error": str(e)
        }


# ============================================================
# OUTPUT IMAGE
# ============================================================

output_image = cv_to_pil(
    output_bgr
)


# ============================================================
# PROCESSED OUTPUT
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
PROCESSED OUTPUT
</div>

<div class="section-heading">
🖼️ Processed Output
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


left, right = st.columns(2)


with left:

    st.image(
        input_image,
        caption="Input Image",
        width=350
    )


with right:

    st.image(
        output_image,
        caption=f"Output — {selected_operation}",
        width=350
    )


# ============================================================
# STEP 3 — PIXEL INSPECTION
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 03
</div>

<div class="section-heading">
🔬 Pixel Inspection
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


p1, p2 = st.columns(2)


with p1:

    selected_x = st.number_input(
        "Select X coordinate",
        min_value=0,
        max_value=width - 1,
        value=width // 2,
        step=1
    )


with p2:

    selected_y = st.number_input(
        "Select Y coordinate",
        min_value=0,
        max_value=height - 1,
        value=height // 2,
        step=1
    )


r, g, b, gray = calculate_pixel_information(
    image_bgr,
    selected_x,
    selected_y
)


# ============================================================
# PIXEL DISPLAY
# ============================================================

st.markdown(
    f"""
    <div class="pixel-panel">

    <div class="pixel-header">

    <div class="pixel-title">
    SELECTED PIXEL
    </div>

    <div class="pixel-badge">
    LIVE VALUE
    </div>

    </div>

    <div class="pixel-grid">

    <div class="pixel-item pixel-coordinate">

    <div class="pixel-label">
    COORDINATE
    </div>

    <div class="pixel-value">
    ({selected_x}, {selected_y})
    </div>

    </div>

    <div class="pixel-item">

    <div class="pixel-label">
    RED CHANNEL
    </div>

    <div class="pixel-value">
    R = {r}
    </div>

    </div>

    <div class="pixel-item">

    <div class="pixel-label">
    GREEN CHANNEL
    </div>

    <div class="pixel-value">
    G = {g}
    </div>

    </div>

    <div class="pixel-item">

    <div class="pixel-label">
    BLUE CHANNEL
    </div>

    <div class="pixel-value">
    B = {b}
    </div>

    </div>

    </div>

    <div class="pixel-formula">

    <div class="pixel-formula-label">
    GRAYSCALE CALCULATION
    </div>

    <div class="pixel-formula-text">
    Gray = 0.299R + 0.587G + 0.114B
    </div>

    </div>

    <div class="pixel-formula">

    <div class="pixel-formula-label">
    SUBSTITUTION
    </div>

    <div class="pixel-formula-text">
    0.299({r}) + 0.587({g}) + 0.114({b})
    <br>
    = {gray}
    </div>

    </div>

    <div class="pixel-final">

    <div class="pixel-final-label">
    FINAL PIXEL INTENSITY
    </div>

    <div class="pixel-final-value">
    {gray} / 255
    </div>

    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STEP 4 — DETAILED OPERATION CALCULATION
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 04
</div>

<div class="section-heading">
🧮 Detailed Operation Calculation
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


# ============================================================
# TEMPLATE CALCULATION
# ============================================================

if selected_operation == "Template Matching":

    st.markdown(
        f"""
        <div class="calculation">

        <div class="calc-label">
        TEMPLATE MATCHING CALCULATION
        </div>

        <div class="calc-step">
        <b>Step 1 — Source Image</b><br>
        Input image size = {width} × {height}
        </div>

        <div class="calc-step">
        <b>Step 2 — Template Image</b><br>
        A separate uploaded template image is used as the reference pattern.
        </div>

        <div class="calc-step">
        <b>Step 3 — Sliding Window</b><br>
        The template is moved across the source image and compared at each location.
        </div>

        <div class="calc-step">
        <b>Step 4 — OpenCV Similarity Calculation</b><br>
        <span class="formula">
        TM_CCOEFF_NORMED
        </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if template_image is not None:

        st.markdown(
            f"""
            <div class="calc-step">
            <b>Maximum Matching Score:</b><br>
            <span class="formula">
            {template_score:.6f}
            </span>
            </div>

            <div class="calc-step">
            <b>Similarity:</b><br>
            <span class="formula">
            {template_score * 100:.2f}%
            </span>
            </div>

            <div class="calc-step">
            <b>Best Matching Position:</b><br>
            ({template_location[0]}, {template_location[1]})
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# VIOLA-JONES CALCULATION
# ============================================================

elif selected_operation == "Viola-Jones Algorithm":

    gray_image = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY
    )

    integral = cv2.integral(
        gray_image
    )

    total_intensity = int(
        np.sum(gray_image)
    )

    st.markdown(
        f"""
        <div class="calculation">

        <div class="calc-label">
        VIOLA–JONES CALCULATION
        </div>

        <div class="calc-step">
        <b>Step 1 — Input Image</b><br>
        Width = {width} pixels<br>
        Height = {height} pixels<br>
        Total pixels = {total_pixels:,}
        </div>

        <div class="calc-step">
        <b>Step 2 — Grayscale Conversion</b><br>
        <span class="formula">
        Gray = 0.299R + 0.587G + 0.114B
        </span>
        </div>

        <div class="calc-step">
        <b>Step 3 — Integral Image</b><br>
        <span class="formula">
        II(x,y) = Σ(i≤x,j≤y) I(i,j)
        </span><br>
        Integral image size =
        {integral.shape[1]} × {integral.shape[0]}
        </div>

        <div class="calc-step">
        <b>Step 4 — Haar-like Features</b><br>
        Rectangular regions measure local contrast.
        </div>

        <div class="calc-step">
        <b>Step 5 — AdaBoost</b><br>
        Weak classifiers are combined into stronger classifiers.
        </div>

        <div class="calc-step">
        <b>Step 6 — Cascade Classifier</b><br>
        Non-face regions are rejected through multiple stages.
        </div>

        <div class="calc-step">
        <b>Total Grayscale Intensity:</b>
        {total_intensity:,}
        </div>

        <div class="calc-step">
        <b>Detected Faces:</b>
        {face_count}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DEEPFACE CALCULATION
# ============================================================

elif selected_operation == "DeepFace":

    if deepface_result is not None and "error" not in deepface_result:

        age = deepface_result.get(
            "age",
            "N/A"
        )

        gender = deepface_result.get(
            "dominant_gender",
            deepface_result.get("gender", "N/A")
        )

        emotion = deepface_result.get(
            "dominant_emotion",
            "N/A"
        )

        race = deepface_result.get(
            "dominant_race",
            "N/A"
        )

        region = deepface_result.get(
            "region",
            {}
        )

        face_area = (
            region.get("w", 0) *
            region.get("h", 0)
        )

        face_ratio = (
            face_area / total_pixels * 100
            if total_pixels > 0
            else 0
        )

        st.markdown(
            f"""
            <div class="calculation">

            <div class="calc-label">
            DEEPFACE ACTUAL ANALYSIS
            </div>

            <div class="calc-step">
            <b>Step 1 — Face Detection</b><br>
            Detected faces = {face_count}
            </div>

            <div class="calc-step">
            <b>Step 2 — Facial Region</b><br>
            Face width = {region.get("w", 0)} pixels<br>
            Face height = {region.get("h", 0)} pixels<br>
            Face area = {face_area:,} pixels
            </div>

            <div class="calc-step">
            <b>Step 3 — Face Area Ratio</b><br>
            <span class="formula">
            Face Ratio = Face Area / Image Area × 100
            </span><br>
            = {face_ratio:.2f}%
            </div>

            <div class="calc-step">
            <b>Step 4 — Estimated Age</b><br>
            <span class="formula">
            {age}
            </span>
            </div>

            <div class="calc-step">
            <b>Step 5 — Gender</b><br>
            <span class="formula">
            {gender}
            </span>
            </div>

            <div class="calc-step">
            <b>Step 6 — Dominant Emotion</b><br>
            <span class="formula">
            {emotion}
            </span>
            </div>

            <div class="calc-step">
            <b>Step 7 — Dominant Race Category</b><br>
            <span class="formula">
            {race}
            </span>
            </div>

            <div class="calc-step">
            <b>Step 8 — Deep Facial Representation</b><br>
            DeepFace performs deep neural-network based facial representation.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif deepface_result is not None:

        st.error(
            f"DeepFace could not run: {deepface_result['error']}"
        )

    else:

        st.info(
            "DeepFace analysis is waiting for the model to run."
        )


# ============================================================
# FACENET CALCULATION
# ============================================================

else:

    if facenet_embedding is not None:

        embedding_dimension = len(
            facenet_embedding
        )

        embedding_norm = float(
            np.linalg.norm(
                facenet_embedding
            )
        )

        st.markdown(
            f"""
            <div class="calculation">

            <div class="calc-label">
            FACENET ACTUAL EMBEDDING
            </div>

            <div class="calc-step">
            <b>Step 1 — Face Detection</b><br>
            Detected faces = {face_count}
            </div>

            <div class="calc-step">
            <b>Step 2 — Face Representation</b><br>
            FaceNet model converts the face into a numerical vector.
            </div>

            <div class="calc-step">
            <b>Step 3 — Embedding Dimension</b><br>
            <span class="formula">
            {embedding_dimension} dimensions
            </span>
            </div>

            <div class="calc-step">
            <b>Step 4 — Embedding Vector</b><br>
            <span class="formula">
            E = [e₁, e₂, e₃, ..., eₙ]
            </span>
            </div>

            <div class="calc-step">
            <b>Step 5 — Embedding Norm</b><br>
            <span class="formula">
            ||E|| = {embedding_norm:.6f}
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if comparison_image is not None and facenet_result is not None:

            if "error" not in facenet_result:

                verified = facenet_result.get(
                    "verified",
                    False
                )

                distance = facenet_result.get(
                    "distance",
                    0
                )

                threshold = facenet_result.get(
                    "threshold",
                    0
                )

                similarity = max(
                    0.0,
                    min(
                        100.0,
                        (1 - float(distance)) * 100
                    )
                )

                match_text = (
                    "MATCH — Same person likely"
                    if verified
                    else "NO MATCH — Different person likely"
                )

                st.markdown(
                    f"""
                    <div class="calc-step">
                    <b>Step 6 — FaceNet Comparison</b><br>
                    Second face image uploaded successfully.
                    </div>

                    <div class="calc-step">
                    <b>Cosine Distance:</b><br>
                    <span class="formula">
                    {float(distance):.6f}
                    </span>
                    </div>

                    <div class="calc-step">
                    <b>Model Threshold:</b><br>
                    <span class="formula">
                    {float(threshold):.6f}
                    </span>
                    </div>

                    <div class="calc-step">
                    <b>Comparison Result:</b><br>
                    <span class="formula">
                    {match_text}
                    </span>
                    </div>

                    <div class="calc-step">
                    <b>Educational Similarity Score:</b><br>
                    <span class="formula">
                    {similarity:.2f}%
                    </span>
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                st.error(
                    f"FaceNet comparison could not run: "
                    f"{facenet_result['error']}"
                )

        else:

            st.markdown(
                """
                <div class="calc-step">
                <b>Step 6 — Face Comparison</b><br>
                Upload a comparison image above to compare
                two faces using the actual FaceNet model.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        error_text = ""

        if facenet_result is not None:

            error_text = facenet_result.get(
                "error",
                "Unknown FaceNet error"
            )

        st.error(
            f"FaceNet could not run: {error_text}"
        )


# ============================================================
# STEP 5 — APPLICATION
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 05
</div>

<div class="section-heading">
🌐 Real-World Application
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


applications = {

    "Template Matching": (
        "Pattern-Based Face Search",
        "Useful for locating a known visual pattern inside a larger image using an actual uploaded template."
    ),

    "Viola-Jones Algorithm": (
        "Real-Time Face Detection",
        "Useful for classical real-time face detection using Haar features and cascade classifiers."
    ),

    "DeepFace": (
        "Deep Facial Analysis",
        "Actual deep-learning facial analysis can estimate age, gender, emotion and other facial attributes."
    ),

    "FaceNet": (
        "Face Embedding & Similarity",
        "FaceNet converts faces into embeddings and compares facial representations using distance measurements."
    )

}


app_title, app_description = applications[
    selected_operation
]


st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    {app_title}
    </div>

    <div class="card-text">
    {app_description}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STEP 6 — PROCESSED OUTPUT
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 06
</div>

<div class="section-heading">
🖼️ Processed Output
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


left2, right2 = st.columns(2)


with left2:

    st.image(
        input_image,
        caption="Original Input",
        width=350
    )


with right2:

    st.image(
        output_image,
        caption=f"Processed — {selected_operation}",
        width=350
    )


# ============================================================
# STEP 7 — FINAL RESULT
# ============================================================

st.markdown(
"""
<div class="step-badge" style="margin-top:50px;">
STEP 07
</div>

<div class="section-heading">
✨ Final Result
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


detection_text = (
    f"{face_count} face(s) detected"
    if face_count > 0
    else "No face detected"
)


if selected_operation == "Template Matching":

    if template_image is not None:

        final_value = (
            f"{template_score * 100:.2f}% matching score"
        )

    else:

        final_value = "Upload template image"

elif selected_operation == "Viola-Jones Algorithm":

    final_value = detection_text

elif selected_operation == "DeepFace":

    if deepface_result is not None and "error" not in deepface_result:

        final_value = (
            f"Age: {deepface_result.get('age', 'N/A')} • "
            f"Gender: {deepface_result.get('dominant_gender', 'N/A')} • "
            f"Emotion: {deepface_result.get('dominant_emotion', 'N/A')}"
        )

    else:

        final_value = "DeepFace analysis unavailable"

else:

    if facenet_result is not None and "error" not in facenet_result:

        verified = facenet_result.get(
            "verified",
            False
        )

        final_value = (
            "MATCH"
            if verified
            else "NO MATCH"
        )

    elif facenet_embedding is not None:

        final_value = (
            f"Embedding generated "
            f"({len(facenet_embedding)} dimensions)"
        )

    else:

        final_value = "Upload comparison image"


st.markdown(
    f"""
    <div class="final-result">

    <div class="result-title">
    Analysis Complete
    </div>

    <div class="result-value">
    Operation: {selected_operation}
    </div>

    <div class="result-value">
    Detection: {detection_text}
    </div>

    <div class="result-value">
    Image Size: {width} × {height}
    </div>

    <div class="result-value">
    Total Pixels: {total_pixels:,}
    </div>

    <div class="result-value">
    Pixel Coordinate: ({selected_x}, {selected_y})
    </div>

    <div class="result-value">
    Pixel RGB: ({r}, {g}, {b})
    </div>

    <div class="result-value">
    Grayscale Intensity: {gray}
    </div>

    <div class="result-value">
    Final Operation Result: {final_value}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<br><br>

<div style="
text-align:center;
color:#718078;
font-family:'DM Mono', monospace;
font-size:12px;
padding:25px;
">
FACE DETECTION STUDIO
&nbsp;•&nbsp;
PIXEL INSPECTION
&nbsp;•&nbsp;
VISUAL ANALYSIS
&nbsp;•&nbsp;
COMPUTER VISION
</div>
""",
unsafe_allow_html=True
)
