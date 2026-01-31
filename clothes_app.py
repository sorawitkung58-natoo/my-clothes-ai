
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ใส่ API Key ของคุณตรงนี้ (เอามาจากเว็บ Google AI Studio)
genai.configure(api_key="AIzaSyAUpArFNxRE-46DdCH2cadHHwPoSSkqwOk")

st.set_page_config(page_title="AI Clothes Changer", layout="centered")

# 2. รายการชุดตามโจทย์ของคุณ
st.title("👗 เครื่องมือเปลี่ยนชุด AI")

menu = {
    "สไตล์ทั่วไป": ["bikini", "Qipao", "เสื้อสายเดี่ยว", "กางเกงในเเละเสื้อใน", "เสื้อรัดรูป", "ผ้าพันปิดจุดซ้อนเร้น"],
    "เซ็กซี่/นอน": ["ชุดนอน", "ชุดลูกไม้เซ็กซี่", "ชุดเซ็กซี่", "เสื้อผ้าบาง", "เสื้อขาด"],
    "อาชีพ (ไทย)": ["ตำรวจไทย", "พยาบาลไทย", "หมอไทย", "รปภ.", "ทหารไทย"],
    "สัตว์/มาสคอต": ["ชุดช้าง", "ชุดสิงโต", "ชุดหมี", "ชุดหมู", "ชุดแมว", "ชุดเสือ", "ชุดสุนัข", "ชุดกระต่าย"]
}

category = st.selectbox("เลือกหมวดหมู่", list(menu.keys()))
outfit = st.selectbox("เลือกชุด", menu[category])

# 3. ปุ่มอัพโหลด (สีฟ้า)
uploaded_file = st.file_uploader("อัพโหลดรูปภาพของคุณ", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # แสดงรูปในอัตราส่วน 9:16
    img = Image.open(uploaded_file)
    st.image(img, caption="ต้นฉบับ (9:16)", use_container_width=True)
    
    if st.button("✨ เริ่มเปลี่ยนชุด"):
        st.info(f"กำลังเปลี่ยนเป็น {outfit}... (รักษาใบหน้าเดิม)")
        # ส่วนนี้จะส่งไปประมวลผลที่ Gemini

# 4. ปุ่มดาวน์โหลด (สีเขียว)
st.download_button("📥 ดาวน์โหลดรูป (สีเขียว)", data="...", file_name="outfit.png")
if st.button("✨ เริ่มเปลี่ยนชุด"):
        with st.spinner(f"กำลังเปลี่ยนชุดเป็น {outfit}..."):
            # คำสั่งส่งรูปไปให้ Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([
                f"Change the person's outfit to {outfit}. Keep the exact same face and background as the original image. High quality, seamless blending.",
                img
            ])
            
            if response.text:
                st.success("เปลี่ยนชุดเสร็จแล้ว!")
                # หมายเหตุ: ในขั้นตอนนี้ Gemini จะตอบกลับเป็นข้อความ/คำอธิบาย 
                # การเจนรูปใหม่ทับรูปเดิมโดยตรงต้องใช้เทคนิค Inpainting เพิ่มเติม
                st.write(response.text)