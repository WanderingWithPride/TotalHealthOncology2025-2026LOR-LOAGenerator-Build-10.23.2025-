# 📄 LOR/LOA Generator - Total Health Oncology

This is a Streamlit application designed to generate Letters of Request (LOR) and Letters of Agreement (LOA) for Total Health Oncology events. It supports single event and multi-meeting modes, dynamic pricing for booths and add-ons, and exports documents in DOCX and PDF formats.

## ✨ Features

-   **LOR & LOA Generation**: Create professional documents for various event types.
-   **Dynamic Pricing**: Configurable pricing for different booth tiers and add-ons (2025 & 2026).
-   **Multi-Meeting Mode**: Generate multiple letters from an Excel spreadsheet.
-   **Past Event Support**: Generate letters for historical events with a clear warning.
-   **Total Health Branding**: Consistent and readable UI/UX.
-   **Password Protection**: Secure access for your team.

## 🚀 Deployment to Streamlit Cloud

This application is designed for easy deployment to Streamlit Cloud, providing web access for your sales team.

### **1. Create a GitHub Repository**
-   Go to [github.com](https://github.com) and create a **private** repository named `lor-loa-generator`.

### **2. Upload Your Code**
-   Copy the following files into your new GitHub repository:
    -   `app.py` (the main application file)
    -   `requirements.txt` (Python dependencies)
    -   `.streamlit/config.toml` (Streamlit configuration for theming)
    -   `README.md` (this file)
-   Commit and push these files to your `main` branch.

### **3. Deploy to Streamlit Cloud**
-   Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
-   Click **"New App"**.
-   Select your `lor-loa-generator` repository.
-   Set the **Main file path** to `app.py`.
-   **Add a secret**: In the "Advanced settings" or "Secrets" section, add a secret named `password` with the value `TotalHealth2025!`. This is crucial for password protection.
-   Click **"Deploy!"**.

### **4. Access Your App**
-   Once deployed (usually 2-3 minutes), you will get a public URL (e.g., `https://your-app-name.streamlit.app`).
-   Share this URL with your sales team.
-   The password for access is `TotalHealth2025!`.

## 🔄 Updating the Application

To update the application after making changes (e.g., using Cursor AI locally):
1.  Save your changes to the local files (`app.py`, `requirements.txt`, etc.).
2.  Commit and push your changes to your GitHub repository:
    ```bash
    git add .
    git commit -m "Update: [Brief description of changes]"
    git push origin main
    ```
3.  Streamlit Cloud will automatically detect the changes and redeploy your application (takes 1-2 minutes).

## 🔑 Security & Access

-   The application is hosted on Streamlit Cloud with HTTPS encryption.
-   Access is restricted by a password (`TotalHealth2025!`) configured as a secret.
-   The GitHub repository should be **private** to control access to the source code.
