import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw
import urllib.request
import io


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
    transition: 0.2s;
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
    font-size: 18px;
    color: #e8fff0;
    margin-top: 8px;
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


/* ============================================================
   HIGHLIGHT CHOOSE OPERATION LABEL
   ============================================================ */

label[data-testid="stWidgetLabel"] p {
    color: #8ee8b4 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}


/* ============================================================
   SELECTED PIXEL UI
   ============================================================ */

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
    font-weight: 500;
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
    font-weight: 500;
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
    font-weight: 500;
}


/* ============================================================
   SELECTED OPERATION HIGHLIGHT BOX — NEW
   ============================================================ */

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
    box-shadow:
        0 8px 30px rgba(0,0,0,0.20);
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
# DEFAULT HUMAN IMAGE
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

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = response.read()

        image = Image.open(
            io.BytesIO(data)
        ).convert("RGB")

        return image

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

        draw.ellipse(
            (190, 190, 225, 215),
            fill="white"
        )

        draw.ellipse(
            (290, 190, 325, 215),
            fill="white"
        )

        draw.ellipse(
            (202, 197, 213, 208),
            fill="black"
        )

        draw.ellipse(
            (302, 197, 313, 208),
            fill="black"
        )

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


def calculate_template_score(
    image_bgr,
    face
):

    x, y, w, h = face

    gray = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY
    )

    template = gray[
        y:y + h,
        x:x + w
    ]

    if template.size == 0:

        return 0.0, (0, 0), (w, h)

    result = cv2.matchTemplate(
        gray,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(
        result
    )

    return (
        float(max_val),
        max_loc,
        (w, h)
    )


def calculate_pixel_information(
    image_bgr,
    x,
    y
):

    height, width = image_bgr.shape[:2]

    x = max(
        0,
        min(x, width - 1)
    )

    y = max(
        0,
        min(y, height - 1)
    )

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
    help="Keep the default human portrait or upload your own."
)


if uploaded is not None:

    input_image = Image.open(
        uploaded
    ).convert("RGB")

else:

    input_image = default_image


image_bgr = pil_to_cv(
    input_image
)

height, width = image_bgr.shape[:2]

channels = image_bgr.shape[2]

total_pixels = width * height


# ============================================================
# DEFAULT INPUT IMAGE DISPLAY SIZE = 350
# ============================================================

st.image(
    input_image,
    caption="Default Input — Single Human Portrait",
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

        <div class="metric-number">
        {width}
        </div>

        <div class="metric-label">
        IMAGE WIDTH
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with m2:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {height}
        </div>

        <div class="metric-label">
        IMAGE HEIGHT
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {total_pixels:,}
        </div>

        <div class="metric-label">
        TOTAL PIXELS
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with m4:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {channels}
        </div>

        <div class="metric-label">
        CHANNELS
        </div>

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
        "Locate a known facial pattern using similarity between image regions."
    ),

    (
        "02",
        "Viola-Jones",
        "Classical real-time face detection using Haar features and cascade classifiers."
    ),

    (
        "03",
        "DeepFace",
        "Deep-learning based facial representation and verification concept."
    ),

    (
        "04",
        "FaceNet",
        "Converts a face into an embedding for similarity-based comparison."
    )

]


cols = [
    c1,
    c2,
    c3,
    c4
]


for col, operation in zip(
    cols,
    operations
):

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


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


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
# SELECTED OPERATION — HIGHLIGHT BOX
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
# PROCESS FACE DETECTION / OUTPUT IMAGE
# ============================================================

faces = detect_faces(
    image_bgr
)

face_count = len(faces)

output_bgr = image_bgr.copy()


# ============================================================
# TEMPLATE MATCHING OUTPUT
# ============================================================

if selected_operation == "Template Matching":

    if face_count > 0:

        score, loc, size = calculate_template_score(
            image_bgr,
            faces[0]
        )

        x, y, w, h = faces[0]

        cv2.rectangle(
            output_bgr,
            (x, y),
            (x + w, y + h),
            (142, 232, 180),
            4
        )

        cv2.putText(
            output_bgr,
            f"Match {score:.3f}",
            (x, max(35, y - 12)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (142, 232, 180),
            2,
            cv2.LINE_AA
        )


# ============================================================
# VIOLA JONES OUTPUT
# ============================================================

elif selected_operation == "Viola-Jones Algorithm":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "Face"
    )


# ============================================================
# DEEPFACE OUTPUT
# ============================================================

elif selected_operation == "DeepFace":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "DeepFace"
    )

    if face_count > 0:

        x, y, w, h = faces[0]

        cv2.putText(
            output_bgr,
            "Deep Facial Representation",
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


# ============================================================
# FACENET OUTPUT
# ============================================================

else:

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "FaceNet"
    )

    if face_count > 0:

        x, y, w, h = faces[0]

        cv2.putText(
            output_bgr,
            "Face Embedding Region",
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
# SELECTED PIXEL
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
# STEP 4 — OPERATION CALCULATION
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
# TEMPLATE MATCHING
# ============================================================

if selected_operation == "Template Matching":

    st.markdown(
        """
        <div class="calculation">

        <div class="calc-label">
        TEMPLATE MATCHING CALCULATION
        </div>

        <div class="calc-step">
        <b>Step 1 — Grayscale Conversion</b><br>
        RGB image is converted into a single-channel intensity image.
        </div>

        <div class="calc-step">
        <b>Step 2 — Template Selection</b><br>
        A detected facial region is selected as the reference template.
        </div>

        <div class="calc-step">
        <b>Step 3 — Sliding Window</b><br>
        The template is compared with different image locations.
        </div>

        <div class="calc-step">
        <b>Step 4 — Similarity Calculation</b><br>
        <span class="formula">
        R(x,y) = TM_CCOEFF_NORMED(T,I)
        </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if face_count > 0:

        score, loc, size = calculate_template_score(
            image_bgr,
            faces[0]
        )

        st.markdown(
            f"""
            <div class="calc-step">
            <b>Maximum similarity score:</b><br>
            <span class="formula">
            {score:.6f}
            </span>
            </div>

            <div class="calc-step">
            <b>Similarity percentage:</b><br>
            <span class="formula">
            {score * 100:.2f}%
            </span>
            </div>

            <div class="calc-step">
            <b>Best matching position:</b><br>
            ({loc[0]}, {loc[1]})
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        score = 0.0

        st.warning(
            "No face detected for template extraction."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# VIOLA JONES
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
        Total pixels = {width} × {height} = {total_pixels:,}
        </div>

        <div class="calc-step">
        <b>Step 2 — Grayscale Conversion</b><br>
        Each RGB pixel is converted using:
        <br>
        <span class="formula">
        Gray = 0.299R + 0.587G + 0.114B
        </span>
        </div>

        <div class="calc-step">
        <b>Step 3 — Integral Image</b><br>
        <span class="formula">
        II(x,y) = Σ(i≤x,j≤y) I(i,j)
        </span>
        <br>
        Integral image size = {integral.shape[1]} × {integral.shape[0]}
        </div>

        <div class="calc-step">
        <b>Step 4 — Haar-like Features</b><br>
        A Haar feature measures contrast between rectangular regions.
        <br>
        <span class="formula">
        Feature = Σ(white region) − Σ(black region)
        </span>
        </div>

        <div class="calc-step">
        <b>Step 5 — AdaBoost</b><br>
        Multiple weak classifiers are combined to form a stronger classifier.
        </div>

        <div class="calc-step">
        <b>Step 6 — Cascade Classifier</b><br>
        Candidate regions pass through multiple stages.
        Non-face regions are rejected early.
        </div>

        <div class="calc-step">
        <b>Total grayscale intensity:</b>
        {total_intensity:,}
        </div>

        <div class="calc-step">
        <b>Detected faces:</b>
        {face_count}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DEEPFACE
# ============================================================

elif selected_operation == "DeepFace":

    detected_area = 0

    if face_count > 0:

        x, y, w, h = faces[0]

        detected_area = w * h

        face_ratio = (
            detected_area / total_pixels
        ) * 100

    else:

        x = y = w = h = 0

        face_ratio = 0


    st.markdown(
        f"""
        <div class="calculation">

        <div class="calc-label">
        DEEPFACE ANALYSIS
        </div>

        <div class="calc-step">
        <b>Step 1 — Face Detection</b><br>
        Detected face count = {face_count}
        </div>

        <div class="calc-step">
        <b>Step 2 — Face Region</b><br>
        Face width = {w} pixels<br>
        Face height = {h} pixels<br>
        Face area = {detected_area:,} pixels
        </div>

        <div class="calc-step">
        <b>Step 3 — Face Area Ratio</b><br>
        <span class="formula">
        Face Ratio = Face Area / Image Area × 100
        </span>
        <br>
        = {detected_area:,} / {total_pixels:,} × 100
        <br>
        = {face_ratio:.2f}%
        </div>

        <div class="calc-step">
        <b>Step 4 — Deep Feature Representation</b><br>
        A deep neural network transforms the detected face
        into numerical feature representations.
        </div>

        <div class="calc-step">
        <b>Step 5 — Similarity Calculation</b><br>
        <span class="formula">
        Cosine Similarity =
        (A · B) / (||A|| × ||B||)
        </span>
        </div>

        <div class="calc-step">
        <b>Interpretation:</b><br>
        The resulting feature representation can be compared
        with another representation for facial verification.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FACENET
# ============================================================

else:

    embedding_dimension = 128

    if face_count > 0:

        x, y, w, h = faces[0]

        face_area = w * h

    else:

        x = y = w = h = 0

        face_area = 0


    st.markdown(
        f"""
        <div class="calculation">

        <div class="calc-label">
        FACENET CALCULATION
        </div>

        <div class="calc-step">
        <b>Step 1 — Face Detection</b><br>
        Detected faces = {face_count}
        </div>

        <div class="calc-step">
        <b>Step 2 — Face Crop</b><br>
        Face width = {w} pixels<br>
        Face height = {h} pixels<br>
        Face area = {face_area:,} pixels
        </div>

        <div class="calc-step">
        <b>Step 3 — Face Normalization</b><br>
        The detected face is prepared for feature extraction.
        </div>

        <div class="calc-step">
        <b>Step 4 — Embedding Generation</b><br>
        FaceNet represents a face using a numerical embedding.
        </div>

        <div class="calc-step">
        <b>Step 5 — Embedding Vector</b><br>
        <span class="formula">
        E = [e₁,e₂,e₃,...,eₙ]
        </span>
        <br>
        Educational embedding dimension = {embedding_dimension}
        </div>

        <div class="calc-step">
        <b>Step 6 — Euclidean Distance</b><br>
        <span class="formula">
        d(A,B) = √Σ(Aᵢ − Bᵢ)²
        </span>
        </div>

        <div class="calc-step">
        <b>Interpretation:</b><br>
        A smaller distance indicates greater similarity
        between two face embeddings.
        </div>

        </div>
        """,
        unsafe_allow_html=True
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
        "Useful for locating a known visual pattern inside a larger image."
    ),

    "Viola-Jones Algorithm": (
        "Real-Time Face Detection",
        "Useful for classical face detection in images and camera streams."
    ),

    "DeepFace": (
        "Deep Facial Analysis",
        "Deep-learning based facial representations can support verification "
        "and facial analysis systems."
    ),

    "FaceNet": (
        "Face Embedding & Similarity",
        "FaceNet-style embeddings represent faces numerically and compare "
        "facial representations using distance measurements."
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
# STEP 6 — OUTPUT IMAGE
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


# Output is already generated before Step 03.


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


if face_count > 0:

    detection_text = (
        f"{face_count} face(s) detected"
    )

else:

    detection_text = "No face detected"


if selected_operation == "Template Matching":

    if face_count > 0:

        final_value = (
            f"{score * 100:.2f}% similarity"
        )

    else:

        final_value = "No template generated"


elif selected_operation == "Viola-Jones Algorithm":

    final_value = detection_text


elif selected_operation == "DeepFace":

    final_value = (
        f"{detection_text} • "
        f"feature representation prepared"
    )


else:

    final_value = (
        f"{detection_text} • "
        f"embedding representation prepared"
    )


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