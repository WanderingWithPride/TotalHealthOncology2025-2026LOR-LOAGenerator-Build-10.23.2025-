# 🚀 Deployment Guide - LOR/LOA Generator v2.0

**Step-by-Step Instructions for Production Deployment**

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All code is committed to git
- [ ] Tests pass locally (`pytest tests/ -v`)
- [ ] App runs locally (`streamlit run app.py`)
- [ ] Secrets are configured in `.streamlit/secrets.toml`
- [ ] Logo and signature files exist in `assets/`
- [ ] You have a GitHub account
- [ ] You have a Streamlit Cloud account (free)

---

## 📋 Deployment Steps

### Step 1: Prepare Your Repository

```bash
# Navigate to project root
cd /path/to/TotalHealthOncology2025-2026LOR-LOAGenerator-Build-10.23.2025-/

# Check current branch
git branch

# Ensure v2 directory is committed
git status

# If there are uncommitted changes:
git add v2/
git commit -m "Ready for production deployment"
git push
```

---

### Step 2: Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your repositories

---

### Step 3: Deploy Application

1. **Click "New app"** button
2. **Repository**: Select your GitHub repository
   - `WanderingWithPride/TotalHealthOncology2025-2026LOR-LOAGenerator-Build-10.23.2025-`

3. **Branch**: Select your branch
   - `main` or your feature branch

4. **Main file path**: Enter the path to app.py
   - `v2/app.py`

5. **App URL**: Choose a unique subdomain
   - Suggestion: `totalhealthoncology-lor-loa`

---

### Step 4: Configure Secrets

**CRITICAL**: This is the most important step!

1. Click **"Advanced settings"**
2. Scroll to **"Secrets"** section
3. Copy the ENTIRE contents of your local `.streamlit/secrets.toml`
4. Paste into the secrets text box

**Your secrets should look like this:**

```toml
# Main application password
password = "YourMainPasswordHere"

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

# Add-ons pricing 2025
[add_ons_2025]
program_ad_full = {label = "Program Guide Full Page Ad", price = 2000}
charging_stations = {label = "In-Person Charging Station", price = 2000}
wifi_sponsorship = {label = "Wi-Fi Network Sponsorship", price = 3000}
platform_banner = {label = "Platform Banner Ad", price = 2000}
email_banner = {label = "Email Banner Ad", price = 2500}
registration_banner = {label = "Registration Banner Ad", price = 2000}
networking_reception = {label = "In-Person Networking Reception", price = 3500}
networking_activity = {label = "Networking Activity / Excursion", price = 3500}
advisory_board = {label = "Advisory Board (3-hour)", price = 30000}
non_cme_session = {label = "Non-CME/CE Session (45 min)", price = 50000}

# Add-ons pricing 2026
[add_ons_2026]
program_ad_full = {label = "Program Guide Full Page Ad", price = 2000}
charging_stations = {label = "In-Person Charging Station", price = 3000}
wifi_sponsorship = {label = "Wi-Fi Network Sponsorship", price = 3000}
platform_banner = {label = "Platform Banner Ad", price = 2000}
email_banner = {label = "Email Banner Ad", price = 2500}
registration_banner = {label = "Registration Banner Ad", price = 2000}
networking_reception = {label = "In-Person Networking Reception", price = 3500}
networking_activity = {label = "Networking Activity / Excursion", price = 3500}
advisory_board = {label = "Advisory Board (3-hour)", price = 30000}
non_cme_session = {label = "Non-CME/CE Session (45 min)", price = 50000}
```

5. Click **"Save"**

---

### Step 5: Deploy!

1. Click **"Deploy!"** button
2. Wait 2-3 minutes for deployment
3. Watch the logs for any errors

**Expected output:**
```
Preparing system...
Spinning up manager process...
Installing Python dependencies...
✅ Your app is live!
```

---

### Step 6: Test Your Deployment

1. Click on the URL provided (e.g., `https://totalhealthoncology-lor-loa.streamlit.app`)
2. Test login with all three passwords:
   - Main password
   - Sarah's password (`Sarah2025!`)
   - Allison's password (`Allison2025`)
3. Generate a test LOR
4. Generate a test LOA
5. Download DOCX and PDF to verify they work
6. Check activity log

---

## 🔒 Security Checklist

After deployment:

- [ ] Verify secrets are not visible in app
- [ ] Test password protection works
- [ ] Confirm `.gitignore` is protecting `secrets.toml`
- [ ] Verify `letter_generation_log.json` is not in git
- [ ] Check that sensitive pricing is not in public code
- [ ] Ensure only authorized users have passwords

---

## 🔄 Updating Your Deployed App

### Code Changes

```bash
# Make changes to your code
# Test locally first!

# Commit and push
git add v2/
git commit -m "Update: [description of changes]"
git push

# Streamlit Cloud will auto-detect and redeploy (1-2 minutes)
```

### Secrets/Pricing Changes

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click **"Settings"** → **"Secrets"**
4. Edit the secrets
5. Click **"Save"**
6. App will automatically restart

---

## ⚠️ Important Notes

### Repository Privacy

**Your GitHub repository should be PRIVATE** because:
- Even though secrets are protected, you don't want to share your codebase
- Keeps your business logic confidential
- Prevents unauthorized forks/copies

To make repository private:
1. Go to GitHub repository
2. Click **Settings** → **General**
3. Scroll to **Danger Zone**
4. Click **"Change visibility"** → **"Make private"**

### Password Expiration

The app has a 48-hour password expiration built in. Users will need to re-enter their password every 48 hours for security.

### Revoking Access

**To immediately revoke someone's access:**

1. Go to Streamlit Cloud secrets
2. Change their password
3. Click Save
4. They will be locked out on next session

### Backup Your Secrets

**CRITICAL**: Save a copy of your secrets.toml somewhere safe (NOT in git):
- Password manager
- Encrypted cloud storage
- Secure local backup

If you lose your secrets, you'll need to reconfigure everything!

---

## 🐛 Common Deployment Issues

### Issue: "Module not found"

**Solution**: Check that `requirements.txt` is in `v2/` directory and all dependencies are listed.

### Issue: "Secrets not configured"

**Solution**:
1. Double-check secrets are saved in Streamlit Cloud
2. Ensure no syntax errors in TOML format
3. Restart the app

### Issue: "File not found: assets/TH Logo.png"

**Solution**:
1. Ensure `assets/` directory is committed to git
2. Verify logo file exists in repository
3. Check file name matches exactly (case-sensitive)

### Issue: App keeps restarting

**Solution**:
1. Check app logs for errors
2. Verify all dependencies are compatible
3. Check for infinite loops or errors on startup

---

## 📞 Getting Help

### Streamlit Cloud Support
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Internal Support
- Contact Sarah Louden (CEO)
- Review README.md for technical details
- Check SECURITY_GUIDE.md for security questions

---

## ✨ Success!

Once deployed, you'll have:

- ✅ Professional web app accessible from anywhere
- ✅ Secure multi-tier authentication
- ✅ Automatic document generation
- ✅ Activity logging and analytics
- ✅ Easy updates via git push
- ✅ Free hosting on Streamlit Cloud

**Share your app URL with the team and start generating letters!** 🎉

---

**Deployed and ready to go? Congratulations!** 🚀

Your team can now access the LOR/LOA Generator from anywhere with a web browser. No installation required!
