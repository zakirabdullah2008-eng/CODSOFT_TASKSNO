import streamlit as st
import torch
from PIL import Image
from torchvision import models, transforms
from transformers import BlipProcessor, BlipForConditionalGeneration

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Image Captioning",
    page_icon="🖼️",
    layout="centered"
)

# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 30px;
}

.caption-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #cccccc;
    margin-top: 20px;
    font-size: 20px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #cccccc;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Load ResNet50 Feature Extractor
# ---------------------------------------------------------

@st.cache_resource
def load_resnet():

    weights = models.ResNet50_Weights.DEFAULT

    model = models.resnet50(weights=weights)

    # Remove the final classification layer
    feature_extractor = torch.nn.Sequential(
        *list(model.children())[:-1]
    )

    feature_extractor.eval()

    preprocess = weights.transforms()

    return feature_extractor, preprocess


# ---------------------------------------------------------
# Load BLIP Captioning Model
# ---------------------------------------------------------

@st.cache_resource
def load_caption_model():

    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model.eval()

    return processor, model


# ---------------------------------------------------------
# Generate Caption
# ---------------------------------------------------------

def generate_caption(image, processor, model):

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        output = model.generate(
            **inputs,
            max_new_tokens=40,
            num_beams=5
        )

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption


# ---------------------------------------------------------
# Extract ResNet Features
# ---------------------------------------------------------

def extract_features(image, feature_extractor, preprocess):

    image_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():

        features = feature_extractor(image_tensor)

    return features


# ---------------------------------------------------------
# Application Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🖼️ AI Image Captioning</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate natural-language descriptions from images using AI'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("🤖 About")

    st.write(
        "This application combines computer vision "
        "and natural language processing to generate "
        "captions for images."
    )

    st.divider()

    st.subheader("🧠 Technologies")

    st.write("• ResNet50")
    st.write("• BLIP Transformer")
    st.write("• PyTorch")
    st.write("• Hugging Face Transformers")
    st.write("• Streamlit")

    st.divider()

    st.subheader("🔄 Workflow")

    st.write(
        "Image → Visual Processing → "
        "AI Caption Generation → Caption"
    )


# ---------------------------------------------------------
# Image Upload
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png", "webp"]
)


# ---------------------------------------------------------
# Main Application
# ---------------------------------------------------------

if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file).convert("RGB")

        st.subheader("🖼️ Uploaded Image")

        st.image(
            image,
            use_container_width=True
        )

        st.divider()

        if st.button(
            "✨ Generate Caption",
            use_container_width=True
        ):

            with st.spinner(
                "Loading AI models and analyzing the image..."
            ):

                # Load ResNet
                feature_extractor, preprocess = load_resnet()

                # Extract visual features
                features = extract_features(
                    image,
                    feature_extractor,
                    preprocess
                )

                # Load caption model
                processor, caption_model = load_caption_model()

                # Generate caption
                caption = generate_caption(
                    image,
                    processor,
                    caption_model
                )

            st.success("Caption generated successfully!")

            st.markdown(
                f"""
                <div class="caption-box">
                    <b>🤖 Generated Caption:</b><br><br>
                    {caption}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            st.subheader("🔬 AI Processing")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Feature Vector Size",
                    str(features.shape[-1])
                )

            with col2:
                st.metric(
                    "Model",
                    "BLIP Transformer"
                )

            st.info(
                "ResNet50 is used as the computer-vision "
                "feature extractor, while the pretrained "
                "BLIP Transformer generates the natural-language "
                "caption."
            )

    except Exception as e:

        st.error(
            "Unable to process this image. "
            "Please try another image."
        )

        st.caption(f"Error: {e}")

else:

    st.info(
        "👆 Upload an image above to generate an AI caption."
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Task 3 — AI Image Captioning | "
    "Computer Vision + Natural Language Processing"
)
