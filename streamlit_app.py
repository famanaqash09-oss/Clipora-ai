import streamlit as st
import streamlit.components.v1 as components
import html

st.set_page_config(page_title="CLIPORA AI", page_icon="🎬", layout="wide")

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

SITE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NAME__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,Helvetica,sans-serif;color:#222;line-height:1.6}
header{background:__ACCENT__;color:#fff;padding:60px 20px;text-align:center}
header h1{font-size:2.2rem;margin-bottom:8px}
header p{opacity:.9}
.btn{display:inline-block;margin-top:20px;padding:12px 26px;background:#fff;color:__ACCENT__;border-radius:30px;text-decoration:none;font-weight:bold}
section{padding:40px 20px;max-width:800px;margin:auto}
h2{margin-bottom:16px;color:__ACCENT__}
ul{list-style:none;display:grid;gap:10px}
li{background:#f5f3fb;padding:14px 16px;border-radius:12px}
footer{background:#111;color:#ddd;text-align:center;padding:30px 20px}
</style></head><body>
<header><h1>__NAME__</h1><p>__TAGLINE__</p><a class="btn" href="tel:__PHONELINK__">Call __PHONE__</a></header>
<section><h2>About us</h2><p>__ABOUT__</p></section>
<section><h2>Our services</h2><ul>__SERVICES__</ul></section>
<section><h2>Visit us</h2><p>__CITY__</p><p>Phone: __PHONE__</p></section>
<footer>&copy; __NAME__. All rights reserved.</footer>
</body></html>"""

THEMES = {
    "Purple": "#6d28d9",
    "Blue": "#1d4ed8",
    "Green": "#15803d",
    "Rose": "#be185d",
}


def build_site(name, biz_type, city, phone, services_text, about, theme):
    name_s = html.escape(name.strip() or "Your Business")
    city_s = html.escape(city.strip() or "Your City")
    phone_s = html.escape(phone.strip() or "")
    phone_link = "".join(c for c in phone if c.isdigit() or c == "+")
    about_s = html.escape(
        about.strip()
        or f"Welcome to {name_s}, a trusted {biz_type.lower()} in {city_s}. "
        "We are proud to serve our community with quality and care."
    )
    items = [s.strip() for s in services_text.replace(",", "\n").split("\n")]
    items = [html.escape(s) for s in items if s]
    if not items:
        items = ["Ask us about our services"]
    services_html = "".join(f"<li>{s}</li>" for s in items)
    tagline = f"{html.escape(biz_type)} in {city_s}"

    page = SITE_TEMPLATE
    page = page.replace("__NAME__", name_s)
    page = page.replace("__TAGLINE__", tagline)
    page = page.replace("__ACCENT__", THEMES[theme])
    page = page.replace("__PHONELINK__", phone_link)
    page = page.replace("__PHONE__", phone_s)
    page = page.replace("__ABOUT__", about_s)
    page = page.replace("__SERVICES__", services_html)
    page = page.replace("__CITY__", city_s)
    return page


st.markdown('<div class="hero">CLIPORA AI</div>', unsafe_allow_html=True)
st.caption("Clip it. Create it. Build it.")

tab1, tab2, tab3 = st.tabs(
    ["✂️ AI Clipper", "🎥 AI Video Generator", "🌐 AI Website Builder"]
)

with tab1:
    st.header("AI Clipper")
    st.markdown(
        '<div class="card">Upload a video. Automatic clipping is added later.</div>',
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        "Upload your video", type=["mp4", "mov", "m4v", "webm"]
    )
    if uploaded is not None:
        size_mb = uploaded.size / (1024 * 1024)
        st.success(f"Received: {uploaded.name} ({size_mb:.1f} MB)")
        st.video(uploaded)

with tab2:
    st.header("AI Video Generator")
    st.markdown(
        '<div class="card">Turn a text idea into a finished video. '
        "Coming later.</div>",
        unsafe_allow_html=True,
    )

with tab3:
    st.header("AI Website Builder")
    st.markdown(
        '<div class="card">Fill in the details, tap Generate, preview the '
        "site, then download it.</div>",
        unsafe_allow_html=True,
    )

    name = st.text_input("Business name", placeholder="Rose Beauty Salon")
    biz_type = st.selectbox(
        "Business type",
        ["Restaurant", "Beauty salon", "Barber shop", "Online store",
         "Portfolio", "Other business"],
    )
    city = st.text_input("City", placeholder="London")
    phone = st.text_input("Phone number", placeholder="+44 7000 000000")
    services = st.text_area(
        "Services (one per line)",
        placeholder="Haircuts\nNails\nMakeup",
    )
    about = st.text_area("About the business (optional)")
    theme = st.selectbox("Colour", list(THEMES.keys()))

    if st.button("Generate website"):
        st.session_state["site"] = build_site(
            name, biz_type, city, phone, services, about, theme
        )

    if "site" in st.session_state:
        st.subheader("Preview")
        components.html(st.session_state["site"], height=700, scrolling=True)
        st.download_button(
            "Download website (index.html)",
            data=st.session_state["site"],
            file_name="index.html",
            mime="text/html",
        )
