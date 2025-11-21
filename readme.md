
# Crop Disease Detection System  
**AI-Powered Plant Health Diagnosis with Professional PDF Reports**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)  
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B)  
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)  
![Status](https://img.shields.io/badge/Status-Active-success)

A complete 5-agent AI system that instantly identifies crop diseases from leaf photos, explains the problem in simple terms, researches real chemical & organic treatments, provides step-by-step application instructions, and generates ready-to-print PDF reports — all in under 30 seconds.

Built for farmers, extension workers, students, and agronomists.

---

### Key Features

- Upload any leaf/stem image (JPG, PNG, WebP)
- Accurate detection across **50+ crops** and **200+ diseases**
- Confidence score + severity level (Mild / Moderate / Severe)
- Multiple treatment options (chemical + certified organic)
- Detailed step-by-step application guide
- Long-term prevention recommendations
- Professional downloadable **PDF report** with QR code
- Full JSON export for records or integration
- Beautiful, mobile-friendly Streamlit interface

---

### Quick Start (Local)

```bash
git clone https://github.com/yourusername/crop-disease-detection-system.git
cd crop-disease-detection-system
pip install streamlit pillow reportlab qrcode[pil] requests
```

#### Required API Keys (free tiers available)

1. **OpenRouter** → https://openrouter.ai/keys  
2. **Serper.dev** → https://serper.dev

Edit `app.py` and replace:
```python
OPENROUTER_API_KEY = "your-openrouter-key-here"
SERPER_API_KEY      = "your-serper-key-here"
```

Then run:
```bash
streamlit run app.py
```

App will open at http://localhost:8501

---

### PDF Report Includes

- Diagnosis ID & date
- Disease name, crop, confidence, severity
- Visible symptoms checklist
- All recommended treatments (dosage, frequency, safety)
- Step-by-step preparation & spraying guide
- Prevention tips for next season
- Scannable QR code
- Clean, professional layout (ideal for field officers)

---

### Supported Crops (50+ and growing)

Rice, Wheat, Maize, Tomato, Potato, Cotton, Soybean, Chili, Grape, Apple, Citrus, Banana, Coffee, Cassava, Sugarcane, Sorghum, Beans, Cucumber, Eggplant, Cabbage, Okra, Pepper, and many more.

---

### Tech Stack

- Streamlit – UI  
- OpenRouter – Vision + reasoning (Claude, Gemini, Llama 3, etc.)  
- Serper.dev – Real-time treatment research  
- ReportLab + qrcode – PDF generation  
- PIL/Pillow – Image handling

---

### Roadmap

- [ ] Offline mode with local models  
- [ ] Mobile app (Android/iOS)  
- [ ] Multi-language support (Hindi, Spanish, French, etc.)  
- [ ] Farmer dashboard with history  
- [ ] Regional pesticide database integration

---

### Contributing

Contributions are welcome! Feel free to:
- Add regional diseases/treatments
- Improve the UI
- Translate to local languages
- Optimize performance

Just fork → make changes → open a Pull Request

---

### License

MIT License – see [LICENSE](LICENSE)

---

<div align="center">

**Early detection saves crops. Knowledge saves farmers.**

Star this repo if you find it helpful!  
Let's bring AI-powered plant doctors to every field

</div>
```

**Instructions:**
1. Open your project folder
2. Create a new file named exactly: `README.md`
3. Paste the entire content above
4. Replace `yourusername` with your actual GitHub username
5. Save → commit → push

Your GitHub repository will instantly look professional and polished! Done.
