import streamlit as st
import streamlit.components.v1 as components
import html, base64, io, json
from datetime import datetime
from urllib.parse import quote_plus
from PIL import Image, ImageOps

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

PALETTES = {
    "Rose & Gold": ("#be185d", "#d97706"),
    "Purple & Lavender": ("#6d28d9", "#c4b5fd"),
    "Navy & Coral": ("#1e3a8a", "#f97316"),
    "Forest & Gold": ("#166534", "#d4a72c"),
    "Black & Gold": ("#111111", "#d4af37"),
    "Teal & Pink": ("#0f766e", "#ec4899"),
}

LAYOUTS = {"Modern": "l-modern", "Elegant": "l-elegant", "Bold": "l-bold"}


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def mix(a, b, t):
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex(tuple(ra[i] * (1 - t) + rb[i] * t for i in range(3)))


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def on_color(h):
    return "#111111" if lum(h) > 0.18 else "#ffffff"


def readable(h, dark_mode):
    for _ in range(8):
        if dark_mode and lum(h) < 0.25:
            h = mix(h, "#ffffff", 0.2)
        elif (not dark_mode) and lum(h) > 0.3:
            h = mix(h, "#000000", 0.2)
        else:
            break
    return h


TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<script type="application/ld+json">__JSONLD__</script>
<style>
:root{--p:__CP__;--s:__CS__;--pt:__CPT__;--stx:__CST__;--onp:__CONP__;--ons:__CONS__;--dk:__CDK__;--bg:__CBG__;--tx:__CTX__;--card:__CCARD__;--soft:__CSOFT__;--bd:__CBD__}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.65;padding-bottom:72px}
nav{position:sticky;top:0;z-index:10;background:var(--bg);box-shadow:0 2px 12px rgba(0,0,0,.14);display:flex;justify-content:space-between;align-items:center;padding:12px 18px}
.logo{font-weight:800;color:var(--pt);font-size:1.05rem}
nav .links a{margin-left:16px;color:var(--tx);text-decoration:none;font-size:.92rem}
.btn{display:inline-block;padding:13px 28px;border-radius:40px;text-decoration:none;font-weight:700;margin:6px}
.btn-main{background:var(--s);color:var(--ons)}
.btn-alt{border:2px solid #fff;color:#fff}
header.hero{min-height:78vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:#fff;padding:50px 20px;background-size:cover;background-position:center;border-bottom:6px solid var(--s)}
header.hero h1{font-size:2.6rem;line-height:1.15;margin-bottom:12px;max-width:760px;text-shadow:0 2px 12px rgba(0,0,0,.35)}
header.hero p{font-size:1.15rem;margin-bottom:22px;max-width:620px;text-shadow:0 2px 12px rgba(0,0,0,.35)}
.wrap{max-width:1000px;margin:auto;padding:60px 20px}
.alt{background:var(--soft)}
h2{color:var(--pt);font-size:1.8rem;margin-bottom:26px;text-align:center}
h2::after{content:"";display:block;width:64px;height:4px;border-radius:4px;margin:10px auto 0;background:linear-gradient(90deg,var(--p),var(--s))}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:22px;box-shadow:0 4px 18px rgba(0,0,0,.07);display:flex;justify-content:space-between;gap:12px;align-items:center}
.card b{font-size:1.05rem}
.price{color:var(--stx);font-weight:800;white-space:nowrap}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.gallery img{width:100%;height:230px;object-fit:cover;border-radius:14px}
.review{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:22px;box-shadow:0 4px 18px rgba(0,0,0,.07);display:block}
.review p{font-style:italic;margin-bottom:10px}
.review span{color:var(--stx);font-weight:700}
.stars{color:#f59e0b;letter-spacing:2px;margin-bottom:8px}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}
.hours div{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--bd)}
.info p{margin-bottom:10px}
.info a{color:var(--stx);font-weight:700;text-decoration:none}
.about{text-align:center;max-width:720px;margin:auto;font-size:1.08rem}
footer{background:var(--dk);color:#eee;text-align:center;padding:34px 20px}
footer a{color:#fff;margin:0 8px}
.bar{position:fixed;bottom:0;left:0;right:0;display:flex;gap:10px;padding:10px 12px;background:var(--bg);box-shadow:0 -3px 14px rgba(0,0,0,.18);z-index:20}
.bar a{flex:1;text-align:center;padding:13px;border-radius:30px;text-decoration:none;font-weight:700}
.bar .a1{background:var(--p);color:var(--onp)}
.bar .a2{border:2px solid var(--stx);color:var(--stx)}

.l-elegant{font-family:Georgia,"Times New Roman",serif}
.l-elegant h1,.l-elegant h2{font-weight:400;letter-spacing:.14em;text-transform:uppercase}
.l-elegant header.hero{min-height:62vh}
.l-elegant .grid{grid-template-columns:1fr;max-width:640px;margin:auto}
.l-elegant .card{background:transparent;box-shadow:none;border:0;border-bottom:1px dotted var(--bd);border-radius:0;padding:14px 4px}
.l-elegant .review{box-shadow:none;border-radius:4px}
.l-elegant .gallery img{border-radius:2px}
.l-elegant .btn{border-radius:2px;letter-spacing:.08em;text-transform:uppercase;font-size:.9rem}

.l-bold header.hero{align-items:flex-start;text-align:left;padding:60px 8%}
.l-bold header.hero h1{font-size:3.2rem;font-weight:900;text-transform:uppercase;letter-spacing:-.5px}
.l-bold h2{text-align:left;text-transform:uppercase;font-weight:900}
.l-bold h2::after{margin-left:0;width:90px}
.l-bold .about{text-align:left;margin:0}
.l-bold .card{border-left:6px solid var(--s);border-radius:6px}
.l-bold .review{border-radius:6px;border-left:6px solid var(--s)}
.l-bold .gallery img{border-radius:4px}
.l-bold .btn{border-radius:6px}

@media(max-width:600px){nav .links{display:none}header.hero h1{font-size:2rem}.l-bold header.hero h1{font-size:2.3rem}}
@media(min-width:900px){.bar{display:none}body{padding-bottom:0}}
</style></head>
<body class="__BODYCLASS__">
<nav><div class="logo">__NAME__</div><div class="links">__NAVLINKS__</div></nav>
<header class="hero" style="__HEROSTYLE__">
<h1>__NAME__</h1><p>__TAGLINE__</p>
<div>__HEROBTNS__</div>
</header>
<div class="wrap" id="about"><h2>About us</h2><p class="about">__ABOUT__</p></div>
__SERVICES__
__GALLERY__
__REVIEWS__
<div class="alt" id="contact"><div class="wrap"><h2>Visit us</h2>
<div class="two">
<div class="info">__CONTACT__</div>
<div class="hours">__HOURS__</div>
</div></div></div>
<footer><p>&copy; __YEAR__ __NAME__. All rights reserved.</p><p style="margin-top:8px">__SOCIAL__</p></footer>
<div class="bar">__BAR__</div>
</body></html>"""


def img_to_data_uri(file, max_px=1400):
    img = Image.open(file)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def safe_url(u):
    u = (u or "").strip()
    if u.startswith(("http://", "https://")):
        return html.escape(u, quote=True)
    return ""


def build_site(d, hero_uri, gallery_uris):
    esc = html.escape
    raw_name = d["name"].strip() or "Your Business"
    name = esc(raw_name)
    city_raw = d["city"].strip()
    address_raw = d["address"].strip()
    full_addr = ", ".join(x for x in [address_raw, city_raw] if x)

    # Colours
    if d["palette"] == "Custom":
        p, s = d["custom_p"], d["custom_s"]
    else:
        p, s = PALETTES[d["palette"]]
    dark_mode = d["dark"]
    p_text = readable(p, dark_mode)
    s_text = readable(s, dark_mode)
    if dark_mode:
        bg, tx, card, soft, bd = "#0f0f16", "#ececf4", "#1a1a24", "#151520", "#2a2a38"
    else:
        bg, tx, card, soft, bd = "#ffffff", "#1f1f29", "#ffffff", mix(p, "#ffffff", 0.93), "#e5e5ee"
    dk = mix(p, "#000000", 0.55)

    phone_raw = d["phone"].strip()
    phone = esc(phone_raw)
    phone_link = "".join(c for c in phone_raw if c.isdigit() or c == "+")
    email_raw = d["email"].strip()

    default_tag = f"{d['biz_type']} in {city_raw}" if city_raw else d["biz_type"]
    tagline = esc(d["tagline"].strip() or default_tag)
    about = esc(
        d["about"].strip()
        or f"Welcome to {raw_name}, a trusted {d['biz_type'].lower()}"
        + (f" in {city_raw}" if city_raw else "")
        + ". We are proud to serve our community with quality and care."
    )

    book = safe_url(d["booking_url"])
    nav_links = ['<a href="#about">About</a>']
    hero_btns = ""
    bar = ""
    if book:
        hero_btns += f'<a class="btn btn-main" href="{book}">Book now</a>'
        bar += f'<a class="a1" href="{book}">Book now</a>'
    if phone_link:
        hero_btns += f'<a class="btn btn-alt" href="tel:{phone_link}">Call {phone}</a>'
        bar += f'<a class="a2" href="tel:{phone_link}">Call now</a>'
    if not hero_btns:
        hero_btns = '<a class="btn btn-main" href="#contact">Contact us</a>'
        bar = '<a class="a1" href="#contact">Contact us</a>'

    # Services
    services = []
    for line in d["services"].splitlines():
        line = line.strip()
        if not line:
            continue
        if " - " in line:
            n, pr = line.split(" - ", 1)
        else:
            n, pr = line, ""
        services.append((esc(n.strip()), esc(pr.strip())))
    services_html = ""
    if services:
        nav_links.append('<a href="#services">Services</a>')
        cards = "".join(
            f'<div class="card"><b>{n}</b><span class="price">{pr}</span></div>'
            for n, pr in services
        )
        services_html = (
            f'<div class="alt" id="services"><div class="wrap"><h2>Our services</h2>'
            f'<div class="grid">{cards}</div></div></div>'
        )

    # Gallery
    gallery_html = ""
    if gallery_uris:
        nav_links.append('<a href="#gallery">Gallery</a>')
        imgs = "".join(
            f'<img src="{u}" alt="{name} photo {i + 1}" loading="lazy">'
            for i, u in enumerate(gallery_uris)
        )
        gallery_html = (
            f'<div class="wrap" id="gallery"><h2>Gallery</h2>'
            f'<div class="gallery">{imgs}</div></div>'
        )

    # Reviews
    reviews = []
    for line in d["reviews"].splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            who, txt = line.split(":", 1)
        else:
            who, txt = "Happy client", line
        reviews.append((esc(who.strip()), esc(txt.strip())))
    reviews_html = ""
    if reviews:
        nav_links.append('<a href="#reviews">Reviews</a>')
        cards = "".join(
            f'<div class="review"><div class="stars">★★★★★</div><p>“{t}”</p><span>{w}</span></div>'
            for w, t in reviews
        )
        reviews_html = (
            f'<div class="alt" id="reviews"><div class="wrap"><h2>What clients say</h2>'
            f'<div class="grid">{cards}</div></div></div>'
        )

    nav_links.append('<a href="#contact">Contact</a>')

    # Hours
    hours_rows = ""
    for line in d["hours"].splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            day, t = line.split(":", 1)
            hours_rows += f"<div><b>{esc(day.strip())}</b><span>{esc(t.strip())}</span></div>"
        else:
            hours_rows += f"<div><span>{esc(line)}</span></div>"
    hours_html = ("<h3 style='margin-bottom:10px'>Opening hours</h3>" + hours_rows) if hours_rows else ""

    # Contact
    contact = ""
    if full_addr:
        maps = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(full_addr)
        contact += f'<p>📍 {esc(full_addr)}<br><a href="{maps}">Get directions</a></p>'
    if phone_link:
        contact += f'<p>📞 <a href="tel:{phone_link}">{phone}</a></p>'
    if email_raw:
        contact += f'<p>✉️ <a href="mailto:{esc(email_raw, quote=True)}">{esc(email_raw)}</a></p>'

    # Social
    social = ""
    ig = safe_url(d["instagram"])
    fb = safe_url(d["facebook"])
    if ig:
        social += f'<a href="{ig}">Instagram</a>'
    if fb:
        social += f'<a href="{fb}">Facebook</a>'

    if hero_uri:
        hero_style = (
            "background-image:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.55)),"
            f"url('{hero_uri}')"
        )
    else:
        hero_style = (
            "background:radial-gradient(circle at 88% 12%,var(--s),transparent 42%),"
            "linear-gradient(135deg,var(--dk),var(--p))"
        )

    ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": raw_name,
        "description": d["tagline"].strip() or default_tag,
        "telephone": phone_raw,
        "address": full_addr,
    }
    ld = {k: v for k, v in ld.items() if v}
    jsonld = json.dumps(ld).replace("<", "\\u003c")

    title = f"{raw_name} | {default_tag}"
    page = TEMPLATE
    repl = {
        "__TITLE__": esc(title),
        "__DESC__": esc(d["tagline"].strip() or default_tag, quote=True),
        "__JSONLD__": jsonld,
        "__CPT__": p_text,
        "__CST__": s_text,
        "__CONP__": on_color(p),
        "__CONS__": on_color(s),
        "__CDK__": dk,
        "__CBG__": bg,
        "__CTX__": tx,
        "__CCARD__": card,
        "__CSOFT__": soft,
        "__CBD__": bd,
        "__CP__": p,
        "__CS__": s,
        "__BODYCLASS__": LAYOUTS[d["layout"]],
        "__NAVLINKS__": "".join(nav_links),
        "__HEROSTYLE__": hero_style,
        "__HEROBTNS__": hero_btns,
        "__ABOUT__": about,
        "__SERVICES__": services_html,
        "__GALLERY__": gallery_html,
        "__REVIEWS__": reviews_html,
        "__CONTACT__": contact,
        "__HOURS__": hours_html,
        "__SOCIAL__": social,
        "__BAR__": bar,
        "__YEAR__": str(datetime.now().year),
        "__TAGLINE__": tagline,
        "__NAME__": name,
    }
    for k, v in repl.items():
        page = page.replace(k, v)
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
        '<div class="card">Turn a text idea into a finished video. Coming later.</div>',
        unsafe_allow_html=True,
    )

with tab3:
    st.header("AI Website Builder")
    st.markdown(
        '<div class="card">Fill in the details, pick a design, add photos, tap '
        "Generate, preview the site, then download it. Only use photos the "
        "business owner gave you or that are yours.</div>",
        unsafe_allow_html=True,
    )

    with st.form("site_form"):
        st.subheader("Design")
        layout = st.selectbox("Layout", list(LAYOUTS.keys()))
        palette = st.selectbox("Colour palette", list(PALETTES.keys()) + ["Custom"])
        custom_p = st.color_picker("Custom main colour (used if palette = Custom)", "#be185d")
        custom_s = st.color_picker("Custom second colour (used if palette = Custom)", "#d97706")
        dark = st.checkbox("Dark mode website")

        st.subheader("Business details")
        name = st.text_input("Business name *", placeholder="Rose Beauty Salon")
        biz_type = st.selectbox(
            "Business type",
            ["Beauty salon", "Nail salon", "Barber shop", "Restaurant",
             "Cafe", "Online store", "Portfolio", "Other business"],
        )
        tagline = st.text_input(
            "Tagline (short line under the name)",
            placeholder="Beautiful nails, made with care",
        )
        city = st.text_input("City", placeholder="Melbourne")
        address = st.text_input("Street address", placeholder="12 Example Street")
        phone = st.text_input("Phone number", placeholder="+61 400 000 000")
        email = st.text_input("Email (optional)")
        about = st.text_area("About the business (optional)")
        services = st.text_area(
            "Services with prices (one per line, use  -  between name and price)",
            placeholder="Gel manicure - $45\nPedicure - $60\nAcrylic full set - $70",
        )
        hours = st.text_area(
            "Opening hours (one per line)",
            placeholder="Mon-Fri: 9am-6pm\nSat: 10am-4pm\nSun: Closed",
        )
        reviews = st.text_area(
            "Real client reviews (optional, one per line, like  Sarah: Loved it!)"
        )
        booking_url = st.text_input("Booking link (optional, starts with https://)")
        instagram = st.text_input("Instagram link (optional)")
        facebook = st.text_input("Facebook link (optional)")
        hero_file = st.file_uploader(
            "Main banner photo (optional)", type=["jpg", "jpeg", "png", "webp"]
        )
        gallery_files = st.file_uploader(
            "Gallery photos (optional, up to 6)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
        )
        submitted = st.form_submit_button("Generate website")

    if submitted:
        if not name.strip():
            st.warning("Please type the business name first.")
        else:
            try:
                hero_uri = img_to_data_uri(hero_file) if hero_file else ""
                gallery_uris = [img_to_data_uri(f) for f in (gallery_files or [])[:6]]
                data = dict(
                    layout=layout, palette=palette, custom_p=custom_p,
                    custom_s=custom_s, dark=dark, name=name, biz_type=biz_type,
                    tagline=tagline, city=city, address=address, phone=phone,
                    email=email, about=about, services=services, hours=hours,
                    reviews=reviews, booking_url=booking_url,
                    instagram=instagram, facebook=facebook,
                )
                st.session_state["site"] = build_site(data, hero_uri, gallery_uris)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    if "site" in st.session_state:
        st.subheader("Preview")
        components.html(st.session_state["site"], height=800, scrolling=True)
        st.download_button(
            "Download website (index.html)",
            data=st.session_state["site"],
            file_name="index.html",
            mime="text/html",
        )
