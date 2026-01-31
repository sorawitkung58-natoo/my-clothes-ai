import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. ตั้งค่า API Key ---
# นำ API Key ที่ได้จาก Google AI Studio มาวางในเครื่องหมายคำพูดด้านล่าง
genai.configure(api_key="ใส่_API_KEY_ของคุณที่นี่")

# --- 2. ตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="AI Clothes Changer", layout="centered")
st.title("👗 เครื่องมือเปลี่ยนชุด AI")
st.write("รักษาใบหน้าและพื้นหลังเดิม 9:16")

# --- 3. เมนูเลือกชุดตามที่คุณต้องการ ---
menu = {
    "สไตล์ทั่วไป": ["Bikini", "Qipao (กี่เพ้า)", "เสื้อสายเดี่ยว", "กางเกงในเเละเสื้อใน", "เสื้อรัดรูป", "ผ้าพันปิดจุดซ้อนเร้น"],
    "เซ็กซี่/นอน": ["ชุดนอน", "ชุดลูกไม้เซ็กซี่", "ชุดเซ็กซี่", "เสื้อผ้าบาง", "เสื้อขาด"],
    "อาชีพ (ไทย)": ["ตำรวจไทย", "พยาบาลไทย", "หมอไทย", "รปภ.", "ทหารไทย"],
    "สัตว์/มาสคอต": ["ชุดช้าง", "ชุดสิงโต", "ชุดหมี", "ชุดหมู", "ชุดแมว", "ชุดเสือ", "ชุดสุนัข", "ชุดกระต่าย"]
}

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("เลือกหมวดหมู่", list(menu.keys()))
with col2:
    outfit = st.selectbox("เลือกชุดที่ต้องการ", menu[category])

# --- 4. ส่วนอัปโหลดรูปภาพ (ปุ่มสีฟ้า) ---
uploaded_file = st.file_uploader("📤 อัปโหลดรูปภาพของคุณ (แนะนำแนวตั้ง 9:16)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # อ่านไฟล์รูปภาพ
    img = Image.open(uploaded_file)
    st.image(img, caption="รูปต้นฉบับ", use_container_width=True)
    
    # --- 5. ปุ่มเริ่มทำงาน ---
    if st.button("✨ เริ่มเปลี่ยนชุด"):
        if "ใส่_API_KEY" in genai.get_default_api_key():
            st.error("❌ คุณยังไม่ได้ใส่ API Key ในโค้ดครับ!")
        else:
            with st.spinner(f"กำลังเปลี่ยนเป็น {outfit} กรุณารอสักครู่..."):
                try:
                    # เรียกใช้ Model Gemini 1.5 Flash
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # ส่งรูปและ Prompt คำสั่ง
                    prompt = f"""
                    Task: Change the person's outfit in the provided image to '{outfit}'.
                    Requirements:
                    1. Keep the exact same person's face, features, and hair.
                    2. Keep the exact same background and environment.
                    3. The new outfit '{outfit}' must fit the person's body naturally.
                    4. Maintain the 9:16 aspect ratio.
                    5. Output should be a high-quality description and visualization.
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    # แสดงผลลัพธ์
                    st.success("✅ ประมวลผลเสร็จสิ้น!")
                    st.markdown("### 📸 ผลลัพธ์จาก AI:")
                    st.write(response.text)
                    
                    # ปุ่มดาวน์โหลด (จำลอง)
                    st.download_button(
                        label="📥 ดาวน์โหลดรูป (สีเขียว)",
                        data=uploaded_file.getvalue(),
                        file_name=f"new_{outfit}.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")

# --- 6. คำแนะนำเพิ่มเติม ---
st.divider()
st.info("หมายเหตุ: Gemini 1.5 Flash จะเน้นการอธิบายและปรับเปลี่ยนภาพ หากต้องการสร้างภาพใหม่ทับลงไปโดยตรง ระบบต้องเชื่อมต่อกับโมเดลประเภท Inpainting เช่น Imagen 3 หรือ Stable Diffusion ครับ")