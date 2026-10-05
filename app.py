import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw
import urllib.request
import io


# ============================================================
# PAGE CONFIG
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

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,255,177,0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(72,149,239,0.07),
            transparent 25%
        ),
        #0b100e;

    color: #edf5ef;
}

.block-container {
    max-width: 1500px;
    padding-top: 35px;
    padding-bottom: 80px;
}

.hero {
    border: 1px solid rgba(145,232,179,0.24);
    border-radius: 28px;
    padding: 38px 42px;
    background:
        linear-gradient(
            135deg,
            rgba(22,34,27,0.96),
            rgba(14,22,18,0.96)
        );
    box-shadow:
        0 25px 70px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.03);

    margin-bottom: 40px;
}

.hero-small {
    color: #8ee8b4;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    font-size: clamp(42px,6vw,78px);
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 0.95;
}

.hero-title span {
    color: #8ee8b4;
}

.hero-subtitle {
    margin-top: 20px;
    color: #aab8af;
    font-size: 17px;
}

.pill {
    display: inline-block;
    border: 1px solid rgba(142,232,180,0.25);
    background: rgba(142,232,180,0.07);
    color: #bdeecf;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    margin: 15px 8px 0 0;
}

.section-heading {
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
    font-size: 12px;
    letter-spacing: 1px;
}

.card {
    border: 1px solid rgba(142,232,180,0.18);
    background: rgba(20,30,24,0.78);
    border-radius: 22px;
    padding: 24px;
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

.calculation {
    border: 1px solid rgba(142,232,180,0.23);
    background: #111a15;
    border-radius: 24px;
    padding: 30px;
    margin-top: 15px;
}

.calc-label {
    color: #8ee8b4;
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
}

.result-title {
    color: #8ee8b4;
    font-size: 26px;
    font-weight: 800;
}

.result-value {
    font-size: 17px;
    color: #e8fff0;
    margin-top: 10px;
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

div[data-baseweb="select"] > div {
    background: rgba(20,30,24,0.9);
    border-color: rgba(142,232,180,0.25);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEFAULT IMAGE
# ============================================================

IMAGE_URL = (
    "https://raw.githubusercontent.com/"
    "ageitgey/face_recognition/master/examples/obama.jpg"
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

        return img


# ============================================================
# IMAGE CONVERSION
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


# ============================================================
# OPENCV HAAR CASCADE
# ============================================================

@st.cache_resource
def load_face_detector():

    cascade_path = (
        cv2.data.haarcascades
        +
        "haarcascade_frontalface_default.xml"
    )

    cascade = cv2.CascadeClassifier(
        cascade_path
    )

    if cascade.empty():

        raise RuntimeError(
            "Haar Cascade could not be loaded."
        )

    return cascade


def detect_faces(image_bgr):

    gray = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY
    )

    cascade = load_face_detector()

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(45, 45)
    )

    return faces


# ============================================================
# DRAW FACES
# ============================================================

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


# ============================================================
# PIXEL INFORMATION
# ============================================================

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
# TEMPLATE MATCHING
# ============================================================

def template_match(
    source_bgr,
    template_bgr
):

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

        new_w = max(
            20,
            int(tw * scale)
        )

        new_h = max(
            20,
            int(th * scale)
        )

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

    min_val, max_val, min_loc, max_loc = (
        cv2.minMaxLoc(result)
    )

    return (
        float(max_val),
        max_loc,
        (tw, th)
    )


# ============================================================
# DEEPFACE
# ============================================================

@st.cache_resource
def load_deepface():

    from deepface import DeepFace

    return DeepFace


def run_deepface_single_action(
    image_bgr,
    action
):

    DeepFace = load_deepface()

    result = DeepFace.analyze(
        img_path=image_bgr,
        actions=[action],
        detector_backend="opencv",
        enforce_detection=True,
        silent=True
    )

    if isinstance(result, list):

        if len(result) > 0:

            return result[0]

    return result


# ============================================================
# FACENET
# ============================================================

@st.cache_resource
def load_facenet_deepface():

    from deepface import DeepFace

    return DeepFace


def get_facenet_embedding(
    image_bgr
):

    DeepFace = load_facenet_deepface()

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


def compare_facenet(
    image1_bgr,
    image2_bgr
):

    DeepFace = load_facenet_deepface()

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
# SESSION STATE
# ============================================================

if "operation_ran" not in st.session_state:
    st.session_state.operation_ran = False

if "operation_result" not in st.session_state:
    st.session_state.operation_result = None

if "deepface_result" not in st.session_state:
    st.session_state.deepface_result = None

if "facenet_embedding" not in st.session_state:
    st.session_state.facenet_embedding = None

if "facenet_result" not in st.session_state:
    st.session_state.facenet_result = None

if "template_score" not in st.session_state:
    st.session_state.template_score = 0.0

if "template_location" not in st.session_state:
    st.session_state.template_location = (0, 0)

if "template_size" not in st.session_state:
    st.session_state.template_size = (0, 0)


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
Explore facial analysis algorithms through
visual processing, pixel inspection,
mathematical calculations and real-world
applications.
</div>

<div>
<span class="pill">Pixel Inspection</span>
<span class="pill">Face Detection</span>
<span class="pill">Algorithm Analysis</span>
<span class="pill">Visual Results</span>
</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# STEP 01 — INPUT IMAGE
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
    "Upload another single-person image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    key="main_image"
)


if uploaded:

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

total_pixels = (
    width * height
)


st.image(
    input_image,
    width=350
)


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "IMAGE WIDTH",
        width
    )


with m2:

    st.metric(
        "IMAGE HEIGHT",
        height
    )


with m3:

    st.metric(
        "TOTAL PIXELS",
        f"{total_pixels:,}"
    )


with m4:

    st.metric(
        "CHANNELS",
        channels
    )


# ============================================================
# STEP 02 — OPERATION
# ============================================================

st.markdown(
"""
<div class="step-badge">
STEP 02
</div>

<div class="section-heading">
🔎 Select Operation
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


selected_operation = st.selectbox(
    "Choose the operation",
    [
        "Template Matching",
        "Viola-Jones Algorithm",
        "DeepFace",
        "FaceNet"
    ],
    index=1
)


# Reset operation results when operation changes
if st.session_state.get("last_operation") != selected_operation:

    st.session_state.operation_ran = False

    st.session_state.operation_result = None

    st.session_state.deepface_result = None

    st.session_state.facenet_embedding = None

    st.session_state.facenet_result = None

    st.session_state.template_score = 0.0

    st.session_state.last_operation = selected_operation


template_image = None

comparison_image = None


# ============================================================
# TEMPLATE INPUT
# ============================================================

if selected_operation == "Template Matching":

    template_upload = st.file_uploader(
        "Upload Template Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="template_upload"
    )

    if template_upload:

        template_image = Image.open(
            template_upload
        ).convert("RGB")

        st.image(
            template_image,
            width=250
        )


# ============================================================
# DEEPFACE INPUT
# ============================================================

elif selected_operation == "DeepFace":

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        🧠 DeepFace Analysis
        </div>

        <div class="card-text">
        Select one analysis model. Only the selected
        model will be loaded, reducing memory usage
        during deployment.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    deepface_action = st.selectbox(
        "Choose DeepFace analysis",
        [
            "emotion",
            "age",
            "gender",
            "race"
        ]
    )


# ============================================================
# FACENET INPUT
# ============================================================

elif selected_operation == "FaceNet":

    comparison_upload = st.file_uploader(
        "Upload Comparison Face Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="comparison_upload"
    )

    if comparison_upload:

        comparison_image = Image.open(
            comparison_upload
        ).convert("RGB")

        st.image(
            comparison_image,
            width=250
        )


# ============================================================
# STEP 03 — FACE DETECTION
# ============================================================

faces = []

try:

    faces = detect_faces(
        image_bgr
    )

except Exception as e:

    st.warning(
        f"OpenCV face detection error: {e}"
    )


face_count = len(faces)


# ============================================================
# OUTPUT INITIALIZATION
# ============================================================

output_bgr = image_bgr.copy()


template_score = st.session_state.template_score

template_location = (
    st.session_state.template_location
)

template_size = (
    st.session_state.template_size
)

deepface_result = (
    st.session_state.deepface_result
)

facenet_embedding = (
    st.session_state.facenet_embedding
)

facenet_result = (
    st.session_state.facenet_result
)


# ============================================================
# ACTUAL OPERATION BUTTON
# ============================================================

run_operation = False


if selected_operation == "Template Matching":

    if template_image is not None:

        run_operation = st.button(
            "▶ Run Template Matching",
            use_container_width=True
        )

    else:

        st.info(
            "Upload a template image to perform Template Matching."
        )


elif selected_operation == "Viola-Jones Algorithm":

    run_operation = st.button(
        "▶ Run Viola-Jones Face Detection",
        use_container_width=True
    )


elif selected_operation == "DeepFace":

    run_operation = st.button(
        f"▶ Run DeepFace {deepface_action.title()} Analysis",
        use_container_width=True
    )


elif selected_operation == "FaceNet":

    run_operation = st.button(
        "▶ Generate FaceNet Embedding / Compare",
        use_container_width=True
    )


# ============================================================
# TEMPLATE MATCHING — ACTUAL
# ============================================================

if (
    run_operation
    and
    selected_operation == "Template Matching"
    and
    template_image is not None
):

    template_bgr = pil_to_cv(
        template_image
    )

    try:

        with st.spinner(
            "Performing actual template matching..."
        ):

            (
                template_score,
                template_location,
                template_size
            ) = template_match(
                image_bgr,
                template_bgr
            )

        st.session_state.template_score = (
            template_score
        )

        st.session_state.template_location = (
            template_location
        )

        st.session_state.template_size = (
            template_size
        )

        st.session_state.operation_ran = True

        st.session_state.operation_result = (
            "Template Matching completed"
        )

    except Exception as e:

        st.error(
            f"Template Matching error: {e}"
        )


# ============================================================
# VIOLA-JONES — ACTUAL
# ============================================================

if (
    run_operation
    and
    selected_operation == "Viola-Jones Algorithm"
):

    try:

        with st.spinner(
            "Running actual Viola-Jones detection..."
        ):

            faces = detect_faces(
                image_bgr
            )

        face_count = len(faces)

        st.session_state.operation_ran = True

        st.session_state.operation_result = (
            "Viola-Jones detection completed"
        )

    except Exception as e:

        st.error(
            f"Viola-Jones error: {e}"
        )


# ============================================================
# DEEPFACE — ACTUAL
# ============================================================

if (
    run_operation
    and
    selected_operation == "DeepFace"
):

    try:

        with st.spinner(
            f"Loading DeepFace {deepface_action} model "
            "and analyzing the image..."
        ):

            deepface_result = (
                run_deepface_single_action(
                    image_bgr,
                    deepface_action
                )
            )

        st.session_state.deepface_result = (
            deepface_result
        )

        st.session_state.operation_ran = True

        st.session_state.operation_result = (
            f"DeepFace {deepface_action} analysis completed"
        )

    except Exception as e:

        st.session_state.deepface_result = {
            "error": str(e)
        }

        st.error(
            "DeepFace could not complete the analysis."
        )

        st.info(
            "This can happen on low-memory CPU deployments "
            "because DeepFace models are large."
        )


# ============================================================
# FACENET — ACTUAL
# ============================================================

if (
    run_operation
    and
    selected_operation == "FaceNet"
):

    try:

        with st.spinner(
            "Loading FaceNet and generating embedding..."
        ):

            facenet_embedding = (
                get_facenet_embedding(
                    image_bgr
                )
            )

        st.session_state.facenet_embedding = (
            facenet_embedding
        )

        if comparison_image is not None:

            comparison_bgr = pil_to_cv(
                comparison_image
            )

            with st.spinner(
                "Comparing the two faces..."
            ):

                facenet_result = (
                    compare_facenet(
                        image_bgr,
                        comparison_bgr
                    )
                )

            st.session_state.facenet_result = (
                facenet_result
            )

        st.session_state.operation_ran = True

        st.session_state.operation_result = (
            "FaceNet operation completed"
        )

    except Exception as e:

        st.session_state.facenet_result = {
            "error": str(e)
        }

        st.error(
            f"FaceNet error: {e}"
        )


# ============================================================
# DRAW ACTUAL OUTPUT
# ============================================================

if selected_operation == "Template Matching":

    if st.session_state.operation_ran:

        x, y = template_location

        tw, th = template_size

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


elif selected_operation == "Viola-Jones Algorithm":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "Face"
    )


elif selected_operation == "DeepFace":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "DeepFace"
    )


elif selected_operation == "FaceNet":

    output_bgr = draw_faces(
        image_bgr,
        faces,
        "FaceNet"
    )


# ============================================================
# STEP 03 — PROCESSED OUTPUT
# ============================================================

output_image = cv_to_pil(
    output_bgr
)


st.markdown(
"""
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
# STEP 04 — PIXEL INSPECTION
# ============================================================

st.markdown(
"""
<div class="step-badge">
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
        value=width // 2
    )


with p2:

    selected_y = st.number_input(
        "Select Y coordinate",
        min_value=0,
        max_value=height - 1,
        value=height // 2
    )


r, g, b, gray = (
    calculate_pixel_information(
        image_bgr,
        selected_x,
        selected_y
    )
)


st.markdown(
f"""
<div class="calculation">

<div class="calc-label">
SELECTED PIXEL
</div>

<div class="calc-step">
<b>Coordinate:</b>
({selected_x}, {selected_y})
</div>

<div class="calc-step">
<b>RGB:</b>
R = {r},
G = {g},
B = {b}
</div>

<div class="calc-step">

<b>Grayscale Formula</b><br>

<span class="formula">
Gray = 0.299R + 0.587G + 0.114B
</span>

</div>

<div class="calc-step">

<b>Calculation</b><br>

0.299({r}) +
0.587({g}) +
0.114({b})
=
{gray}

</div>

<div class="calc-step">

<b>Final Intensity:</b>

{gray} / 255

</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# STEP 05 — DETAILED CALCULATION
# ============================================================

st.markdown(
"""
<div class="step-badge">
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

    if st.session_state.operation_ran:

        st.markdown(
f"""
<div class="calculation">

<div class="calc-label">
TEMPLATE MATCHING — ACTUAL CALCULATION
</div>

<div class="calc-step">
<b>Source Image:</b>
{width} × {height}
</div>

<div class="calc-step">
<b>Template Size:</b>
{template_size[0]} × {template_size[1]}
</div>

<div class="calc-step">
<b>Method:</b>
Sliding window template comparison
</div>

<div class="calc-step">
<b>OpenCV Method:</b>
TM_CCOEFF_NORMED
</div>

<div class="calc-step">
<b>Best Location:</b>
({template_location[0]}, {template_location[1]})
</div>

<div class="calc-step">
<b>Actual Matching Score:</b>
{template_score:.6f}
</div>

<div class="calc-step">
<b>Similarity:</b>
{template_score * 100:.2f}%
</div>

</div>
""",
unsafe_allow_html=True
        )

    else:

        st.info(
            "Run Template Matching to display the actual calculation."
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
VIOLA-JONES — ACTUAL PROCESSING
</div>

<div class="calc-step">
<b>Step 1 — Grayscale Conversion</b><br>
Original image:
{width} × {height} × {channels}
</div>

<div class="calc-step">
<b>Step 2 — Grayscale Image</b><br>
Generated grayscale image:
{gray_image.shape[1]} × {gray_image.shape[0]}
</div>

<div class="calc-step">
<b>Step 3 — Integral Image</b><br>
Integral image size:
{integral.shape[1]} × {integral.shape[0]}
</div>

<div class="calc-step">
<b>Step 4 — Haar-like Features</b><br>
The Haar cascade evaluates rectangular contrast
patterns used by the trained classifier.
</div>

<div class="calc-step">
<b>Step 5 — Cascade Classification</b><br>
The OpenCV Haar cascade evaluates candidate
regions and rejects non-face regions through
multiple classifier stages.
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

    if (
        deepface_result is not None
        and
        "error" not in deepface_result
    ):

        region = deepface_result.get(
            "region",
            {}
        )

        face_w = region.get(
            "w",
            0
        )

        face_h = region.get(
            "h",
            0
        )

        face_area = (
            face_w * face_h
        )

        face_ratio = (
            face_area /
            total_pixels *
            100
            if total_pixels
            else 0
        )

        action_value = (
            deepface_result.get(
                "dominant_" + deepface_action,
                deepface_result.get(
                    deepface_action,
                    "N/A"
                )
            )
        )

        st.markdown(
f"""
<div class="calculation">

<div class="calc-label">
DEEPFACE — ACTUAL ANALYSIS
</div>

<div class="calc-step">
<b>Analysis Type:</b>
{deepface_action.title()}
</div>

<div class="calc-step">
<b>Detected Faces:</b>
{face_count}
</div>

<div class="calc-step">
<b>Face Width:</b>
{face_w}px<br>

<b>Face Height:</b>
{face_h}px<br>

<b>Face Area:</b>
{face_area:,} pixels
</div>

<div class="calc-step">
<b>Face Area Ratio:</b>
{face_ratio:.2f}%
</div>

<div class="calc-step">
<b>Actual DeepFace Result:</b>
{action_value}
</div>

<div class="calc-step">
<b>Model:</b>
DeepFace deep-learning facial analysis
</div>

</div>
""",
unsafe_allow_html=True
        )

    elif deepface_result:

        st.error(
            "DeepFace failed: "
            +
            str(
                deepface_result.get(
                    "error",
                    "Unknown error"
                )
            )
        )

    else:

        st.info(
            "Run DeepFace analysis to display the actual result."
        )


# ============================================================
# FACENET CALCULATION
# ============================================================

elif selected_operation == "FaceNet":

    if facenet_embedding is not None:

        dimension = len(
            facenet_embedding
        )

        norm = float(
            np.linalg.norm(
                facenet_embedding
            )
        )

        st.markdown(
f"""
<div class="calculation">

<div class="calc-label">
FACENET — ACTUAL EMBEDDING
</div>

<div class="calc-step">
<b>Detected Faces:</b>
{face_count}
</div>

<div class="calc-step">
<b>Embedding Dimension:</b>
{dimension}
</div>

<div class="calc-step">
<b>Embedding:</b><br>
E = [e₁, e₂, e₃, ..., eₙ]
</div>

<div class="calc-step">
<b>Embedding Norm:</b>
{norm:.6f}
</div>

<div class="calc-step">
<b>Model:</b>
FaceNet
</div>

</div>
""",
unsafe_allow_html=True
        )


        if (
            comparison_image is not None
            and
            facenet_result is not None
            and
            "error" not in facenet_result
        ):

            verified = facenet_result.get(
                "verified",
                False
            )

            distance = float(
                facenet_result.get(
                    "distance",
                    0
                )
            )

            threshold = float(
                facenet_result.get(
                    "threshold",
                    0
                )
            )

            similarity = max(
                0,
                min(
                    100,
                    (1 - distance) * 100
                )
            )

            result_text = (
                "MATCH — Same person likely"
                if verified
                else
                "NO MATCH — Different person likely"
            )

            st.markdown(
f"""
<div class="calculation">

<div class="calc-step">
<b>Cosine Distance:</b>
{distance:.6f}
</div>

<div class="calc-step">
<b>Model Threshold:</b>
{threshold:.6f}
</div>

<div class="calc-step">
<b>Verification:</b>
{result_text}
</div>

<div class="calc-step">
<b>Educational Similarity:</b>
{similarity:.2f}%
</div>

</div>
""",
unsafe_allow_html=True
            )

    else:

        st.info(
            "Run FaceNet to generate the actual embedding."
        )


# ============================================================
# STEP 05 — APPLICATION
# ============================================================

st.markdown(
"""
<div class="step-badge">
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

    "Template Matching":
        "Pattern-based visual search inside images.",

    "Viola-Jones Algorithm":
        "Classical real-time face detection using Haar features and cascade classifiers.",

    "DeepFace":
        "Deep-learning facial analysis including estimated age, gender, emotion and other facial attributes.",

    "FaceNet":
        "Face embedding generation and facial similarity comparison."
}


st.markdown(
f"""
<div class="card">

<div class="card-title">
{selected_operation}
</div>

<div class="card-text">
{applications[selected_operation]}
</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# STEP 06 — FINAL RESULT
# ============================================================

st.markdown(
"""
<div class="step-badge">
STEP 06
</div>

<div class="section-heading">
✨ Final Result
</div>

<div class="section-line"></div>
""",
unsafe_allow_html=True
)


if selected_operation == "Template Matching":

    if st.session_state.operation_ran:

        final_result = (
            f"{template_score * 100:.2f}% "
            "matching score"
        )

    else:

        final_result = (
            "Run Template Matching"
        )


elif selected_operation == "Viola-Jones Algorithm":

    if st.session_state.operation_ran:

        final_result = (
            f"{face_count} face(s) detected"
        )

    else:

        final_result = (
            "Run Viola-Jones"
        )


elif selected_operation == "DeepFace":

    if (
        deepface_result
        and
        "error" not in deepface_result
    ):

        action_value = (
            deepface_result.get(
                "dominant_" + deepface_action,
                deepface_result.get(
                    deepface_action,
                    "N/A"
                )
            )
        )

        final_result = (
            f"{deepface_action.title()}: "
            f"{action_value}"
        )

    else:

        final_result = (
            "Run DeepFace analysis"
        )


else:

    if (
        facenet_result
        and
        "error" not in facenet_result
    ):

        final_result = (
            "MATCH"
            if facenet_result.get(
                "verified",
                False
            )
            else
            "NO MATCH"
        )

    elif facenet_embedding is not None:

        final_result = (
            f"Embedding generated "
            f"({len(facenet_embedding)} dimensions)"
        )

    else:

        final_result = (
            "Run FaceNet"
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
Detection: {face_count} face(s)
</div>

<div class="result-value">
Image Size: {width} × {height}
</div>

<div class="result-value">
Total Pixels: {total_pixels:,}
</div>

<div class="result-value">
Pixel Coordinate:
({selected_x}, {selected_y})
</div>

<div class="result-value">
Pixel RGB:
({r}, {g}, {b})
</div>

<div class="result-value">
Grayscale Intensity:
{gray}
</div>

<div class="result-value">
Final Operation Result:
{final_result}
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
