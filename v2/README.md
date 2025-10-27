# 📄 LOR/LOA Generator v2.0

**Professional Healthcare Document Generation System**
Total Health Conferencing - Production-Ready Rebuild

---

## 🎯 Overview

Complete rebuild of the LOR/LOA generator with modern, modular architecture. Generates professional Letters of Request (LOR) and Letters of Agreement (LOA) for medical conference sponsorships.

### ✨ Key Features

- **Single Event Mode**: Generate LOR/LOA for individual conferences
- **Multi-Meeting Packages**: Combine multiple events into comprehensive sponsorships
- **Excel Bulk Mode**: Process spreadsheets to generate hundreds of letters
- **Professional Documents**: DOCX and PDF with branding, signatures, legal terms
- **Security**: Multi-tier authentication, input sanitization, audit logging
- **Smart Pricing**: Automatic calculations with 2025/2026 pricing, discounts, rounding

---

## 🏗️ Architecture

```
v2/
├── config/              # Configuration & data
│   ├── events.py       # 57+ events database
│   ├── pricing.py      # Booth tiers, add-ons, discounts
│   └── settings.py     # App settings, company info
│
├── core/                # Business logic
│   ├── models.py       # Data structures
│   ├── security.py     # Authentication & sanitization
│   ├── pricing_calc.py # Pricing engine
│   └── logger.py       # Audit trail
│
├── generators/          # Document generation
│   ├── base.py         # Abstract base classes
│   ├── docx_builder.py # DOCX creation
│   ├── pdf_builder.py  # PDF creation
│   ├── lor_generator.py # LOR documents
│   └── loa_generator.py # LOA documents
│
├── services/            # Business services
│   ├── event_matcher.py # Excel event matching
│   └── multi_meeting.py # Multi-meeting packages
│
├── tests/               # Unit tests
│   ├── test_pricing.py
│   └── test_event_matcher.py
│
├── assets/              # Logo and signature
├── .streamlit/          # Streamlit config
└── app.py               # Main application
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git

### Local Development

```bash
# Navigate to v2 directory
cd v2/

# Install dependencies
pip install -r requirements.txt

# Copy secrets template
cp .streamlit/secrets.toml.template .streamlit/secrets.toml

# Edit secrets.toml with your passwords and pricing
nano .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔐 Security Setup

### secrets.toml Configuration

Edit `.streamlit/secrets.toml` with your actual values:

```toml
# Main password
password = "YourSecurePassword"

# User passwords (revocable)
sarah_password = "Sarah2025!"
allison_password = "Allison2025"

# Booth pricing
[booth_prices]
standard_1d = 5000
standard_2d = 7500
platinum = 10000
best_of = 10000
premier = 15000

# Add-ons pricing (2025 vs 2026)
[add_ons_2025]
program_ad_full = {label = "Program Guide Full Page Ad", price = 2000}
# ... (see template for full list)
```

**CRITICAL**: Never commit `secrets.toml` to git! It's protected by `.gitignore`.

---

## 📦 Deployment to Streamlit Cloud

### Step 1: Prepare Repository

```bash
# Ensure all files are committed
git add v2/
git commit -m "Ready for deployment"
git push
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New App"**
4. Select your repository
5. Set **Main file path**: `v2/app.py`
6. Click **"Advanced Settings"** → **"Secrets"**

### Step 3: Add Secrets

Copy the ENTIRE contents of your local `.streamlit/secrets.toml` into the Streamlit Cloud secrets box.

### Step 4: Deploy

- Click **"Deploy!"**
- Wait 2-3 minutes for deployment
- Get your live URL: `https://your-app.streamlit.app`

---

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_pricing.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Manual Testing Checklist

- [ ] Login with all three passwords (main, Sarah, Allison)
- [ ] Generate single-event LOR with booth + add-ons
- [ ] Generate single-event LOA with booth + add-ons
- [ ] Test 10%, 15%, 20% discounts
- [ ] Test custom total override
- [ ] Create multi-meeting package (3+ events)
- [ ] Verify DOCX downloads and opens correctly
- [ ] Verify PDF downloads and displays correctly
- [ ] Check activity log shows recent generation
- [ ] Test 2025 vs 2026 pricing differences

---

## 📊 Features Comparison

| Feature | v1 (Original) | v2 (Rebuild) |
|---------|---------------|--------------|
| Lines of Code | 3,145 (1 file) | ~4,000 (20+ files) |
| Architecture | Monolithic | Modular |
| Type Hints | ❌ | ✅ |
| Unit Tests | ❌ | ✅ |
| Documentation | Limited | Comprehensive |
| Error Handling | Basic | Robust |
| Maintainability | Difficult | Easy |
| Expandability | Hard | Simple |

---

## 🔧 Maintenance

### Adding a New Event

Edit `config/events.py`:

```python
Event(
    meeting_name="2026 New Conference",
    meeting_date_long="December 15, 2026",
    venue="Hotel Name",
    city_state="City, State",
    default_tier="standard_1d",
    expected_attendance=50
)
```

### Updating Pricing

Edit `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets:

```toml
[booth_prices]
standard_1d = 5500  # Updated price
```

Restart the app to apply changes.

### Revoking User Access

**To revoke Sarah's access:**

1. Change `sarah_password` in secrets
2. Restart app

**To revoke Allison's access:**

1. Change `allison_password` in secrets
2. Restart app

---

## 🐛 Troubleshooting

### "Module not found" error

```bash
# Ensure you're in v2/ directory
cd v2/

# Reinstall dependencies
pip install -r requirements.txt
```

### "Logo not found" warning

- Check that `assets/TH Logo.png` exists
- Verify file path in `config/settings.py`

### "Secrets not configured" error

- Ensure `.streamlit/secrets.toml` exists locally
- For Streamlit Cloud, check secrets are properly configured

### Documents not generating

- Check browser console for errors
- Verify all required fields are filled
- Check logs: `letter_generation_log.json`

---

## 📞 Support

**Internal Questions:**
- Contact Sarah Louden (CEO)
- Check `DEPLOYMENT_READY.md` for detailed deployment steps
- Review `SECURITY_GUIDE.md` for security best practices

**Technical Issues:**
- Check error messages in Streamlit app
- Review unit test failures
- Examine `letter_generation_log.json` for generation history

---

## 📝 License

Proprietary - Total Health Conferencing
© 2025 Total Health Information Services, LLC.

---

## 🎉 Version History

### v2.0 (Current)
- Complete rebuild with modular architecture
- Type hints throughout
- Comprehensive unit tests
- Multi-meeting package support
- Enhanced security and logging
- Professional documentation

### v1.0 (Legacy)
- Original monolithic implementation
- Basic features functional
- Limited documentation
- Challenging to maintain

---

**Built with ❤️ for Total Health Conferencing**
