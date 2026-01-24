# 🚀 Deployment Guide - Soda Intelligence Dashboard

## ✅ Files Ready for Deployment

Your deployment package includes:
- `app.py` - Main Streamlit application
- `Master_Data_Final_Clean.xlsx` - Data (889 products)
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `.streamlit/config.toml` - Streamlit configuration

---

## 🌟 OPTION 1: Streamlit Cloud (RECOMMENDED - FREE & EASIEST)

### Why Streamlit Cloud?
- ✅ **FREE** forever for public apps
- ✅ Deploy in 2 minutes
- ✅ Auto-updates from GitHub
- ✅ Custom domain support
- ✅ Built for Streamlit apps

### Steps:

**1. Push to GitHub**
```bash
# Create a new repo on GitHub (let's call it "soda-intelligence")
# Then push your code:

cd deployment_package
git init
git add .
git commit -m "Initial deployment"
git remote add origin https://github.com/YOUR_USERNAME/soda-intelligence.git
git push -u origin main
```

**2. Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Click "Sign in with GitHub"
- Click "New app"
- Fill in:
  - **Repository**: YOUR_USERNAME/soda-intelligence
  - **Branch**: main
  - **Main file path**: app.py
- Click "Deploy!"

**3. Done!**
Your app will be live at: `https://YOUR_USERNAME-soda-intelligence.streamlit.app`

### Custom Domain (Optional)
- Go to app settings
- Add your custom domain
- Update DNS CNAME record

---

## 🔥 OPTION 2: Vercel (Fast & Free)

### Steps:

**1. Create `vercel.json`**
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**2. Deploy**
```bash
npm i -g vercel
cd deployment_package
vercel
```

---

## 🐳 OPTION 3: Google Cloud Run (Professional)

### Steps:

**1. Create `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**2. Build & Deploy**
```bash
# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/soda-dashboard

# Deploy to Cloud Run
gcloud run deploy soda-dashboard \
  --image gcr.io/YOUR_PROJECT_ID/soda-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi
```

**Cost**: ~$0-5/month (depending on traffic)

---

## 🟣 OPTION 4: Heroku (Simple & Reliable)

### Steps:

**1. Create `Procfile`**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**2. Create `setup.sh`**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**3. Update `Procfile`**
```
web: sh setup.sh && streamlit run app.py
```

**4. Deploy**
```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
git push heroku main
```

**Cost**: ~$7/month (Eco Dyno)

---

## 💻 OPTION 5: Local Development

### Quick Start
```bash
cd deployment_package
pip install -r requirements.txt
streamlit run app.py
```

Open browser to: `http://localhost:8501`

---

## 🎯 Which Option to Choose?

| Platform | Best For | Cost | Difficulty |
|----------|----------|------|------------|
| **Streamlit Cloud** | Public portfolios | FREE | ⭐ Easy |
| **Vercel** | Fast deployment | FREE | ⭐⭐ Medium |
| **Google Cloud Run** | Professional apps | ~$0-5/mo | ⭐⭐⭐ Hard |
| **Heroku** | Quick prototypes | ~$7/mo | ⭐⭐ Medium |
| **Local** | Testing | FREE | ⭐ Easy |

### 🏆 For Your Portfolio: Choose Streamlit Cloud

**Why?**
1. Free forever
2. Professional URL: `username-soda-intelligence.streamlit.app`
3. Easy to share with recruiters
4. Can add custom domain later
5. Zero DevOps required

---

## 📝 After Deployment

### 1. Update Portfolio Link
Add to your resume:
```
Amazon Soda Intelligence Dashboard
Live Demo: https://your-app.streamlit.app
```

### 2. Create LinkedIn Post
```
🚀 Just launched my Amazon Soda Category Intelligence Dashboard!

Analyzed 889+ products across Amazon & Walmart to uncover:
• Modern sodas (poppi, OLIPOP) 6-8x over-indexed online
• PepsiCo's $1.95B poppi acquisition strategy
• Revenue-weighted pricing shows 2.4x premium for functional benefits

Built with Python (Streamlit, Plotly, Pandas) + strategic analysis

Live Demo: [your-link]

#DataAnalysis #ProductManagement #StrategyAnalytics
```

### 3. Add to GitHub README
Update with:
- Live demo link
- Screenshots
- Key insights
- Technical stack

---

## 🐛 Troubleshooting

**App won't start?**
- Check `requirements.txt` has all dependencies
- Verify `Master_Data_Final_Clean.xlsx` is in same folder
- Check Streamlit logs for errors

**Data not loading?**
- Ensure Excel file path is correct: `Master_Data_Final_Clean.xlsx`
- File must be in same directory as `app.py`

**Charts not showing?**
- Clear browser cache
- Check Plotly is in requirements.txt

---

## 📞 Need Help?

1. Check Streamlit docs: https://docs.streamlit.io
2. Streamlit community forum: https://discuss.streamlit.io
3. Test locally first with: `streamlit run app.py`

---

**Ready to deploy? Start with Streamlit Cloud - it's the easiest!** 🚀
