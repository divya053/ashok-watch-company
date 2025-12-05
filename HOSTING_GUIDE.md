# 🚀 Free Hosting Guide - Ashok Watch Company

This guide will help you host your website for **FREE** and set up the payment gateway.

---

## 📋 Prerequisites

1. A GitHub account (free): https://github.com
2. A Razorpay account (free): https://razorpay.com

---

## 💳 Step 1: Set Up Razorpay Payment Gateway

### 1.1 Create Razorpay Account
1. Go to https://razorpay.com
2. Click "Sign Up" and create a business account
3. Verify your email and phone number

### 1.2 Get API Keys
1. Log in to Razorpay Dashboard: https://dashboard.razorpay.com
2. Go to **Settings** → **API Keys**
3. Click **Generate Test Keys** (for testing)
4. Save your:
   - **Key ID** (starts with `rzp_test_`)
   - **Key Secret**

### 1.3 For Production (Live Payments)
1. Complete KYC verification in Razorpay dashboard
2. Switch to **Live Mode**
3. Generate **Live Keys** (starts with `rzp_live_`)

> ⚠️ **Important**: Use Test Keys during development. Switch to Live Keys only after testing!

---

## 🌐 Step 2: Upload Code to GitHub

### 2.1 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `ashok-watch-company`
3. Select **Private** (recommended)
4. Click **Create repository**

### 2.2 Upload Your Code
Open terminal in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit - Ashok Watch Company"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ashok-watch-company.git
git push -u origin main
```

---

## 🎯 Step 3: Deploy to Free Hosting

### Option A: Render.com (Recommended - Easiest)

1. **Sign Up**: Go to https://render.com and sign up with GitHub

2. **Create New Web Service**:
   - Click **New** → **Web Service**
   - Connect your GitHub repository
   - Select `ashok-watch-company`

3. **Configure Settings**:
   - **Name**: `ashok-watch-company`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Select **Free**

4. **Add Environment Variables**:
   Click **Environment** and add:
   ```
   RAZORPAY_KEY_ID = rzp_test_your_key_id
   RAZORPAY_KEY_SECRET = your_key_secret
   SECRET_KEY = any-random-secret-string
   ```

5. **Deploy**: Click **Create Web Service**

6. **Your website will be live at**: `https://ashok-watch-company.onrender.com`

> 💡 **Note**: Free tier may sleep after 15 mins of inactivity. First visit takes ~30 seconds to wake up.

---

### Option B: Railway.app

1. **Sign Up**: Go to https://railway.app and sign up with GitHub

2. **Create New Project**:
   - Click **New Project**
   - Select **Deploy from GitHub repo**
   - Choose your `ashok-watch-company` repository

3. **Add Environment Variables**:
   - Click on the deployed service
   - Go to **Variables** tab
   - Add:
   ```
   RAZORPAY_KEY_ID = rzp_test_your_key_id
   RAZORPAY_KEY_SECRET = your_key_secret
   SECRET_KEY = any-random-secret-string
   PORT = 5000
   ```

4. **Generate Domain**:
   - Go to **Settings** → **Networking**
   - Click **Generate Domain**

5. **Your website will be live at**: `https://ashok-watch-company.up.railway.app`

---

### Option C: PythonAnywhere

1. **Sign Up**: Go to https://www.pythonanywhere.com and create free account

2. **Upload Files**:
   - Go to **Files** tab
   - Upload all your project files

3. **Create Web App**:
   - Go to **Web** tab
   - Click **Add a new web app**
   - Select **Flask**
   - Set source code path to your folder

4. **Set Environment Variables**:
   Edit the WSGI configuration file and add:
   ```python
   import os
   os.environ['RAZORPAY_KEY_ID'] = 'rzp_test_your_key_id'
   os.environ['RAZORPAY_KEY_SECRET'] = 'your_key_secret'
   ```

5. **Your website will be live at**: `https://yourusername.pythonanywhere.com`

---

## 🔗 Step 4: Custom Domain (Optional)

### Get a Free Domain
- **Freenom**: https://freenom.com (Free .tk, .ml, .ga domains)
- **No-IP**: https://noip.com (Free subdomains)

### Connect Custom Domain on Render.com
1. Go to your Render service
2. Click **Settings** → **Custom Domains**
3. Add your domain
4. Update DNS records at your domain provider

---

## ✅ Step 5: Testing Your Website

### Test Razorpay Payments
Use these test card details:
- **Card Number**: `4111 1111 1111 1111`
- **Expiry**: Any future date (e.g., `12/25`)
- **CVV**: Any 3 digits (e.g., `123`)
- **OTP**: `1234` (if asked)

### Test UPI
- **UPI ID**: `success@razorpay` (for successful payment)
- **UPI ID**: `failure@razorpay` (for failed payment)

---

## 📱 Step 6: Go Live (Production)

When ready for real payments:

1. **Razorpay**:
   - Complete KYC in Razorpay dashboard
   - Switch to Live Mode
   - Generate Live API Keys
   - Update environment variables with Live Keys

2. **Update Environment Variables**:
   Replace test keys with live keys on your hosting platform.

---

## 🛠️ Troubleshooting

### Website not loading?
- Check if all files are uploaded correctly
- Verify environment variables are set
- Check deployment logs for errors

### Payments not working?
- Verify Razorpay API keys are correct
- Check browser console for errors
- Ensure you're using correct test/live keys

### Images not showing?
- Verify all images are in the `static` folder
- Check file names match exactly (case-sensitive)

---

## 📞 Support

- **Email**: ASHOKLALWANI.ASHU@GMAIL.COM
- **Phone**: +91 9828211241

---

## 🎉 Congratulations!

Your Ashok Watch Company website is now live with:
- ✅ Product catalog
- ✅ Shopping cart
- ✅ Razorpay payment gateway
- ✅ Cash on Delivery option
- ✅ Order management
- ✅ Free hosting!

Happy Selling! 🕐

