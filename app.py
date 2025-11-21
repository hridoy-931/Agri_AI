# ==============================================================
#  CROP DISEASE DETECTION SYSTEM – STREAMLIT UI (COMPLETE)
# ==============================================================
#  pip install streamlit requests pillow reportlab qrcode[pil]
#  Run with: streamlit run app.py
# ==============================================================

import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import qrcode

# Import your existing classes (assuming they're in the same file or imported)
# from your_module import CropDiseaseDetectionSystem, Config

class Config:
    OPENROUTER_API_KEY = "use your own openrouter api key "
    SERPER_API_KEY      = "use your own api"
    APP_NAME = "Crop Disease Detection System"

# ==============================================================
#  PDF GENERATION FUNCTION
# ==============================================================
def generate_pdf_report(res: dict, pdf_path: str):
    """Generate comprehensive PDF report with all treatment options"""
    try:
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.8*inch, bottomMargin=0.8*inch)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=18, spaceAfter=30, alignment=1,
                                     textColor=colors.HexColor("#2E8B57"))
        story.append(Paragraph("CROP DISEASE DIAGNOSIS REPORT", title_style))
        story.append(Spacer(1, 12))

        ident = res.get("disease_identification", {})
        expl  = res.get("disease_explanation", {})
        summ  = res.get("final_summary", {})

        if not ident.get("disease_detected"):
            story.append(Paragraph("<b>RESULT:</b> Healthy Plant", styles["Normal"]))
            story.append(Spacer(1, 12))
            doc.build(story)
            return True

        # Summary Table
        tbl_data = [
            ["Disease", ident.get("disease_name","?")],
            ["Crop",    ident.get("crop_type","?")],
            ["Confidence", f"{ident.get('confidence_score',0)}%"],
            ["Severity", ident.get("severity","?").title()],
            ["Date", res.get("date_human","?")]
        ]
        tbl = Table(tbl_data, colWidths=[2*inch, 3*inch])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#228B22")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.lightgrey)
        ]))
        story.append(tbl)
        story.append(Spacer(1, 20))

        # Simple Summary
        if expl.get("simple_summary"):
            story.append(Paragraph("<b>Simple Summary:</b>", styles["Heading3"]))
            story.append(Paragraph(expl["simple_summary"], styles["Normal"]))
            story.append(Spacer(1, 12))

        # Immediate Action
        if summ.get("immediate_action_required"):
            story.append(Paragraph("<b>IMMEDIATE ACTION:</b>", styles["Heading3"]))
            story.append(Paragraph(summ["immediate_action_required"], styles["Normal"]))
            story.append(Spacer(1, 12))

        # ALL TREATMENT OPTIONS
        research = res.get("treatment_research", {})
        treatments = research.get("treatments", [])

        if treatments:
            story.append(Paragraph("<b>Recommended Treatment Options:</b>", styles["Heading3"]))
            story.append(Spacer(1, 8))

            for t in treatments:
                name = t.get("product_name", "Unknown Treatment")
                dosage = t.get("dosage", "See label")
                apply = t.get("application_method", "Spray")
                freq = t.get("frequency", "Every 7-10 days")
                safety = t.get("safety_precautions", "Wear gloves")
                active = t.get("active_ingredient", "")

                bullet_text = f"<b>{name}</b>"
                if active:
                    bullet_text += f" ({active})"
                bullet_text += f"<br/>• <b>Dosage:</b> {dosage}<br/>• <b>Apply:</b> {apply}<br/>• <b>Every:</b> {freq}<br/>• <b>Safety:</b> {safety}"

                story.append(Paragraph(f"• {bullet_text}", styles["Normal"]))
                story.append(Spacer(1, 6))
            story.append(Spacer(1, 10))

        # Step-by-Step
        instr = res.get("treatment_instructions", {})
        if "error" not in instr and instr.get("preparation_steps"):
            story.append(Paragraph("<b>Step-by-Step Application (Recommended):</b>", styles["Heading3"]))
            for step in instr.get("preparation_steps", []) + instr.get("application_steps", []):
                t = step.get("title", "")
                i = step.get("instruction", "")
                story.append(Paragraph(f"• <b>{t}:</b> {i}", styles["Normal"]))
            story.append(Spacer(1, 8))

        # Prevention
        if summ.get("prevention_for_future"):
            story.append(Paragraph("<b>Prevention for Future:</b>", styles["Heading3"]))
            for tip in summ["prevention_for_future"]:
                story.append(Paragraph(f"• {tip}", styles["Normal"]))
            story.append(Spacer(1, 12))

        # QR Code
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(f"Diagnosis ID: {res.get('diagnosis_id', 'N/A')}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"qr_{res.get('diagnosis_id', 'temp')}.png"
        img.save(qr_path)
        story.append(Paragraph("<b>Scan for Full Data:</b>", styles["Normal"]))
        story.append(RLImage(qr_path, width=1.2*inch, height=1.2*inch))
        story.append(Spacer(1, 12))
        story.append(Paragraph("AI Crop Doctor – OpenRouter + Serper", styles["Normal"]))

        doc.build(story)
        
        # Cleanup QR code
        if os.path.exists(qr_path):
            os.remove(qr_path)
        
        return True
    except Exception as e:
        st.error(f"PDF Generation Error: {str(e)}")
        return False

# ==============================================================
#  STREAMLIT PAGE CONFIG
# ==============================================================
st.set_page_config(
    page_title="Crop Disease Detection",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================
#  CUSTOM CSS
# ==============================================================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    .stAlert {
        border-radius: 10px;
    }
    h1 {
        color: #065f46;
    }
    h2 {
        color: #047857;
    }
    h3 {
        color: #059669;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================
#  SIDEBAR
# ==============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/plant-under-sun.png", width=80)
    st.title("🌾 Crop Disease Detection")
    st.markdown("---")
    
    st.markdown("### 🤖 AI System Info")
    st.info("""
    **5-Agent AI System:**
    1. 👁️ Visual Identifier
    2. 📚 Disease Explainer
    3. 🔬 Treatment Researcher
    4. 📋 Instructor
    5. 📊 Summarizer
    """)
    
    st.markdown("---")
    st.markdown("### 📊 System Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "95%+")
        st.metric("Crops", "50+")
    with col2:
        st.metric("Diseases", "200+")
        st.metric("Response", "<30s")
    
    st.markdown("---")
    st.markdown("### ℹ️ How to Use")
    st.markdown("""
    1. Upload crop image
    2. Wait for AI analysis
    3. Review diagnosis
    4. Download PDF report
    """)
    
    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("🔸 OpenRouter API")
    st.markdown("🔸 Serper Search")

# ==============================================================
#  MAIN CONTENT
# ==============================================================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🌱 Crop Disease Detection System")
    st.markdown("### AI-Powered Plant Health Analysis")

st.markdown("---")

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'uploaded_image_path' not in st.session_state:
    st.session_state.uploaded_image_path = None

# ==============================================================
#  FILE UPLOAD SECTION
# ==============================================================
st.markdown("## 📤 Upload Crop Image")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose an image of your crop",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="Upload a clear photo of the affected plant leaves or stems"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.uploaded_image_path = image_path
        
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
with col2:
    st.markdown("### 📋 Upload Guidelines")
    st.markdown("""
    ✅ **Good Images:**
    - Clear, focused shot
    - Good lighting
    - Close-up of symptoms
    - Multiple affected areas
    
    ❌ **Avoid:**
    - Blurry images
    - Poor lighting
    - Too far away
    - Multiple plants
    """)

# ==============================================================
#  ANALYZE BUTTON
# ==============================================================
if uploaded_file is not None:
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔬 Analyze Crop Disease", type="primary", use_container_width=True):
            with st.spinner("🤖 AI Agents analyzing your crop..."):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    "👁️ Visual identification in progress...",
                    "📚 Explaining disease characteristics...",
                    "🔬 Researching treatment options...",
                    "📋 Creating step-by-step instructions...",
                    "📊 Generating comprehensive summary..."
                ]
                
                for i, stage in enumerate(stages):
                    status_text.text(stage)
                    progress_bar.progress((i + 1) * 20)
                    time.sleep(1)
                
                # REPLACE THIS SECTION WITH YOUR ACTUAL SYSTEM CALL:
                # ==================================================
                # from your_module import CropDiseaseDetectionSystem
                # system = CropDiseaseDetectionSystem(Config.OPENROUTER_API_KEY, Config.SERPER_API_KEY)
                # result = system.run(image_path, want_treatment=True)
                # ==================================================
                
                # Demo result (replace with actual)
                result = {
                    "diagnosis_id": f"CROP_DIAG_{int(time.time())}",
                    "date_human": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "disease_identification": {
                        "disease_detected": True,
                        "disease_name": "Bacterial Blight",
                        "crop_type": "Rice",
                        "confidence_score": 92,
                        "severity": "moderate",
                        "visible_symptoms": [
                            "Yellow-brown lesions on leaf edges",
                            "Water-soaked appearance on leaves",
                            "Wilting of seedlings"
                        ],
                        "reasoning": "Multiple characteristic symptoms visible"
                    },
                    "disease_explanation": {
                        "simple_summary": "Bacterial blight is a serious disease affecting rice crops. It spreads rapidly in warm, humid conditions and can cause significant yield loss if not treated promptly.",
                        "what_causes_it": "Caused by Xanthomonas oryzae bacteria",
                        "how_it_spreads": "Spreads through water, wind, and contaminated tools",
                        "favorable_conditions": ["High humidity", "Warm temperatures (25-30°C)", "Heavy rainfall"],
                        "why_harmful": "Can reduce yield by 20-50% if left untreated"
                    },
                    "treatment_research": {
                        "treatments": [
                            {
                                "type": "chemical",
                                "product_name": "Copper Hydroxide",
                                "active_ingredient": "Copper hydroxide 77%",
                                "dosage": "2-3 g/L of water",
                                "application_method": "Foliar spray",
                                "timing": "Early morning or late evening",
                                "frequency": "Every 7-10 days",
                                "safety_precautions": "Wear protective gloves and mask",
                                "effectiveness": "high"
                            },
                            {
                                "type": "organic",
                                "product_name": "Neem Oil Solution",
                                "active_ingredient": "Azadirachtin 1500 ppm",
                                "dosage": "5 ml per liter",
                                "application_method": "Spray on both sides of leaves",
                                "timing": "Apply in early morning",
                                "frequency": "Every 5-7 days",
                                "safety_precautions": "Apply in early morning or evening",
                                "effectiveness": "medium"
                            },
                            {
                                "type": "chemical",
                                "product_name": "Streptomycin Sulfate",
                                "active_ingredient": "Streptomycin 20%",
                                "dosage": "1-2 g per 10L water",
                                "application_method": "Foliar spray",
                                "timing": "Early growth stage",
                                "frequency": "Every 10-14 days",
                                "safety_precautions": "Do not mix with alkaline substances",
                                "effectiveness": "high"
                            }
                        ]
                    },
                    "treatment_instructions": {
                        "selected_treatment": "Copper Hydroxide",
                        "why_chosen": "High effectiveness, widely available, cost-effective",
                        "preparation_steps": [
                            {"step_number": 1, "title": "Mix Solution", "instruction": "Dissolve 2-3g Copper Hydroxide in 1L clean water. Stir well until fully dissolved."},
                            {"step_number": 2, "title": "Prepare Equipment", "instruction": "Clean your sprayer thoroughly before use to avoid contamination."}
                        ],
                        "application_steps": [
                            {"step_number": 1, "title": "Remove Infected Leaves", "instruction": "Cut and dispose of heavily infected leaves first. Burn or bury them away from field."},
                            {"step_number": 2, "title": "Apply Spray", "instruction": "Spray entire plant early morning, covering both sides of leaves thoroughly."},
                            {"step_number": 3, "title": "Monitor Progress", "instruction": "Check plants after 3-4 days for improvement. Repeat application after 7-10 days."}
                        ]
                    },
                    "final_summary": {
                        "immediate_action_required": "Remove infected leaves immediately and apply copper-based treatment within 24 hours to prevent spread",
                        "prevention_for_future": [
                            "Use disease-resistant rice varieties",
                            "Maintain proper plant spacing (20cm between plants)",
                            "Avoid overhead irrigation during flowering",
                            "Practice crop rotation with non-host crops",
                            "Remove and destroy crop residue after harvest"
                        ]
                    }
                }
                
                st.session_state.analysis_result = result
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                st.rerun()

# ==============================================================
#  DISPLAY RESULTS
# ==============================================================
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    identification = result.get("disease_identification", {})
    explanation = result.get("disease_explanation", {})
    treatments = result.get("treatment_research", {})
    instructions = result.get("treatment_instructions", {})
    summary = result.get("final_summary", {})
    
    st.markdown("---")
    st.markdown("## 🔬 Analysis Results")
    
    if not identification.get("disease_detected"):
        st.success("✅ Good news! Your crop appears to be healthy!")
        st.balloons()
    else:
        # Disease Overview
        st.markdown("### 🦠 Disease Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Disease", identification.get("disease_name", "Unknown"))
        with col2:
            st.metric("Crop Type", identification.get("crop_type", "Unknown"))
        with col3:
            confidence = identification.get("confidence_score", 0)
            st.metric("Confidence", f"{confidence}%")
        with col4:
            severity = identification.get("severity", "unknown").title()
            severity_colors = {"Mild": "🟢", "Moderate": "🟡", "Severe": "🔴", "None": "⚪"}
            st.metric("Severity", f"{severity_colors.get(severity, '⚪')} {severity}")
        
        if explanation.get("simple_summary"):
            st.info(f"📝 **Summary:** {explanation['simple_summary']}")
        
        if summary.get("immediate_action_required"):
            st.error(f"🚨 **IMMEDIATE ACTION REQUIRED:**\n\n{summary['immediate_action_required']}")
        
        st.markdown("---")
        
        # Symptoms
        st.markdown("### 🔍 Visible Symptoms")
        symptoms = identification.get("visible_symptoms", [])
        if symptoms:
            for symptom in symptoms:
                st.markdown(f"✓ {symptom}")
        
        st.markdown("---")
        
        # Treatment Options
        st.markdown("### 💊 Treatment Options")
        
        treatment_list = treatments.get("treatments", [])
        if treatment_list:
            for idx, treatment in enumerate(treatment_list, 1):
                treatment_type = treatment.get("type", "unknown")
                
                with st.expander(f"{'🌿' if treatment_type == 'organic' else '⚗️'} Option {idx}: {treatment.get('product_name', 'Unknown')} ({treatment_type.title()})", expanded=(idx==1)):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Active Ingredient:** {treatment.get('active_ingredient', 'N/A')}")
                        st.markdown(f"**Dosage:** {treatment.get('dosage', 'N/A')}")
                        st.markdown(f"**Application:** {treatment.get('application_method', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**Timing:** {treatment.get('timing', 'N/A')}")
                        st.markdown(f"**Frequency:** {treatment.get('frequency', 'N/A')}")
                        effectiveness = treatment.get('effectiveness', 'unknown').upper()
                        eff_colors = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}
                        st.markdown(f"**Effectiveness:** {eff_colors.get(effectiveness, '⚪')} {effectiveness}")
                    
                    st.warning(f"⚠️ **Safety:** {treatment.get('safety_precautions', 'Follow label instructions')}")
        
        st.markdown("---")
        
        # Step-by-Step Instructions
        if instructions.get("preparation_steps"):
            st.markdown("### 📋 Step-by-Step Application Guide")
            st.markdown(f"**Recommended:** {instructions.get('selected_treatment', 'See treatments above')}")
            st.markdown(f"**Why:** {instructions.get('why_chosen', 'Most effective option')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔧 Preparation Steps")
                for step in instructions.get("preparation_steps", []):
                    st.markdown(f"**{step.get('step_number')}. {step.get('title')}**")
                    st.markdown(f"   {step.get('instruction')}")
            
            with col2:
                st.markdown("#### 🎯 Application Steps")
                for step in instructions.get("application_steps", []):
                    st.markdown(f"**{step.get('step_number')}. {step.get('title')}**")
                    st.markdown(f"   {step.get('instruction')}")
        
        st.markdown("---")
        
        # Prevention
        st.markdown("### 🛡️ Prevention for Future")
        prevention_tips = summary.get("prevention_for_future", [])
        if prevention_tips:
            cols = st.columns(2)
            for idx, tip in enumerate(prevention_tips):
                with cols[idx % 2]:
                    st.success(f"✓ {tip}")
        
        st.markdown("---")
        
        # Download Report Section
        st.markdown("### 📄 Download Report")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📥 Download PDF Report", type="primary", use_container_width=True):
                with st.spinner("📄 Generating PDF report..."):
                    # Generate PDF
                    pdf_filename = f"report_{result['diagnosis_id']}.pdf"
                    pdf_path = os.path.join("reports", pdf_filename)
                    
                    # Create reports directory if it doesn't exist
                    os.makedirs("reports", exist_ok=True)
                    
                    # Generate the PDF
                    success = generate_pdf_report(result, pdf_path)
                    
                    if success and os.path.exists(pdf_path):
                        st.success("✅ PDF report generated successfully!")
                        
                        # Read the PDF file
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        
                        # Offer download button
                        st.download_button(
                            label="💾 Click here to download PDF",
                            data=pdf_bytes,
                            file_name=pdf_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.info(f"📁 PDF also saved at: {pdf_path}")
                    else:
                        st.error("❌ Failed to generate PDF. Check console for errors.")
        
        with col2:
            # Save JSON
            json_data = json.dumps(result, indent=2)
            st.download_button(
                label="📊 Download JSON Data",
                data=json_data,
                file_name=f"diagnosis_{result['diagnosis_id']}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Analyze Another Image", use_container_width=True):
                st.session_state.analysis_result = None
                st.session_state.uploaded_image_path = None
                st.rerun()

# ==============================================================
#  FOOTER
# ==============================================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p><strong>Crop Disease Detection System</strong> | Powered by OpenRouter & Serper APIs</p>
        <p style='font-size: 12px;'>5-Agent AI System: Visual ID • Explainer • Researcher • Instructor • Summarizer</p>
    </div>
""", unsafe_allow_html=True)