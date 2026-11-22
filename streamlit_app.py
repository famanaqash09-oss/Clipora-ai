import streamlit as st

st.set_page_config(
    page_title="CLIPORA AI",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #05030a 0%, #14082b 55%, #1d0f3d 100%);
        color: #ece6ff;
    }
    h1, h2, h3 { color: #c9b8ff !important; }
    .hero {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #8b5cf6, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        background: rgba(139, 92, 246, 0.10);
        border: 1px solid rgba(196, 181, 253, 0.30);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hero">CLIPORA AI</div>', unsafe_allow_html=True)
st.caption("Clip it. Create it. Build it.")

tab1, tab2, tab3 = st.tabs(
    ["✂️ AI Clipper", "🎥 AI Video Generator", "🌐 AI Website Builder"]
)

with tab1:
    st.header("AI Clipper")
    st.markdown(
        '<div class="card">Upload a video. Automatic clipping is added in the next step.</div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload your video",
        type=["mp4", "mov", "m4v", "webm"],
    )

    if uploaded is not None:
        size_mb = uploaded.size / (1024 * 1024)
        st.success(f"Received: {uploaded.name} ({size_mb:.1f} MB)")
        st.video(uploaded)

with tab2:
    st.header("AI Video Generator")
    st.markdown(
        '<div class="card">Turn a text idea into a finished video. '
        "This tool is built in Phase 5.</div>",
        unsafe_allow_html=True,
    )

with tab3:
    st.header("AI Website Builder")
    st.markdown(
        '<div class="card">Describe a website and get one you can export. '
        "This tool is built in Phase 6.</div>",
        unsafe_allow_html=True,
    )
