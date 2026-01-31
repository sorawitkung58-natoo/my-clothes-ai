import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
import io

# --- 1. ตั้งค่า API Key (api_key=) ---
genai.configure(api_key="AIzaSyAxQYxaNDvmSF06N8h8cS4rhzJ4QUCB8io")

# --- 2. ตั้งค่าสายดาร์ก ปิดตัวกรองความปลอดภัยสูงสุด ---
safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# --- 3. หน้าตาแอป ---
st.set_page_config(page_title="AI Clothes Changer Pro", layout="centered")
st.title("👗 เครื่องมือเปลี่ยนชุด AI (Pro Mode)")
st.write("รักษาใบหน้าและพื้นหลังเดิม 9:16")

menu = {
    "สไตล์ทั่วไป": ["Bikini", "Qipao", "เสื้อสายเดี่ยว", "เสื้อรัดรูป"],
    "เซ็กซี่/แฟชั่น": ["ชุดนอนผ้าบาง", "ชุดลูกไม้เซ็กซี่", "ชุดเซ็กซี่", "เสื้อผ้าบาง", "เสื้อขาด"],
    "อาชีพ/สัตว์": ["พยาบาลไทย", "ตำรวจไทย", "ชุดหมี", "ชุดแมว", "ชุดเสือ"]
}

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("เลือกหมวดหมู่", list(menu.keys()))
with col2:
    outfit = st.selectbox("เลือกชุด", menu[category])

uploaded_file = st.file_uploader("📤 อัปโหลดรูปภาพของคุณ (9:16)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="รูปต้นฉบับ", use_container_width=True)
    
    if st.button("✨ เริ่มเปลี่ยนชุด"):
        with st.spinner(f"กำลังประมวลผลเป็น {outfit}..."):
            try:
                # เรียกใช้ Model
                model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
                
                # คำสั่งสั่ง AI แบบเน้นผลลัพธ์แฟชั่น
                prompt = f"Change the person's outfit in this 9:16 photo to '{outfit}'. Keep the face, hair, body shape, and background EXACTLY the same. High-quality fashion edit."
                
                response = model.generate_content([prompt, img])
                
                st.success("✅ ประมวลผลเสร็จสิ้น!")
                st.write(response.text) # AI จะอธิบายผลลัพธ์
                
            except Exception as e:
                st.error(f"ระบบขัดข้อง: {e}")
