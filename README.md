# Amazon Soda Category Intelligence Dashboard

A comprehensive analysis tool for the US soda market, comparing modern sodas (poppi, OLIPOP) vs traditional brands across Amazon and Walmart.

## 📊 What This Dashboard Shows

- **Amazon Analysis**: Revenue, velocity scores, brand performance, surprising winners
- **Walmart & Cross-Platform**: Price comparison, market dynamics
- **Online vs Offline Reality**: How modern sodas over-index online (6-8x)

## 🚀 Quick Start

### Option 1: Streamlit Cloud (Recommended - Free)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Deploy from your GitHub repo:
   - Repository: `your-username/your-repo`
   - Branch: `main`
   - Main file: `streamlit_dashboard_v4.py`
5. Click "Deploy"

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run streamlit_dashboard_v4.py
```

The app will open at `http://localhost:8501`

### Option 3: Heroku Deployment

1. Create `Procfile`:
```
web: streamlit run streamlit_dashboard_v4.py --server.port=$PORT
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option 4: Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT-ID/soda-dashboard

# Deploy
gcloud run deploy soda-dashboard \
  --image gcr.io/PROJECT-ID/soda-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📁 Required Files

- `streamlit_dashboard_v4.py` - Main dashboard application
- `Master_Data_Final_Clean.xlsx` - Data file (889 products)
- `requirements.txt` - Python dependencies

## 🔑 Key Features

### Amazon Analysis
- Revenue estimation based on "units sold last month"
- Velocity scoring (BSR-based, 0-100 scale)
- Parent brand deep dive (PepsiCo, Coca-Cola, etc.)
- Brand leaders within each soda type

### Market Insights
- Modern sodas: 67.5% controlled by poppi + OLIPOP
- Traditional sodas: Coca-Cola leads at 25.5%
- Diet sodas: Diet Coke + Coke Zero at 55.6%
- Premium pricing: Modern sodas 2.4x more expensive

### Data Quality
- 889 total products (Amazon + Walmart)
- Removed: Energy drinks, sparkling water, kombucha
- Revenue-weighted metrics for accuracy
- Properly sourced market data (Circana, Mintel)

## 📊 Data Sources

- **US CSD Market**: Mintel ($55.2B), Circana ($46.1B)
- **Modern Soda Market**: Circana ($1.8B, 83% YoY growth)
- **Brand Share**: Beverage Digest, Gitnux
- **Amazon Data**: Scraped with revenue estimation

## 🎯 Use Cases

- **Brand Managers**: Competitive intelligence, pricing strategy
- **Investors**: Market sizing, growth trends, M&A context
- **Retailers**: Category management, assortment planning
- **Students/Analysts**: Portfolio project, market analysis

## 💡 Technical Notes

- Built with Streamlit for interactive exploration
- Plotly charts for professional visualizations
- Revenue-weighted averages for accurate insights
- BSR-to-velocity conversion: `100 - (ln(BSR) × 10.857)`

## 📝 Attribution

Created by Archana Tatavarthi as a portfolio project demonstrating:
- Data analysis and visualization
- Market research and competitive intelligence
- Strategic insights and business acumen

## 🔗 Links

- Portfolio: [Your Portfolio Link]
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub Repo]

## 📧 Contact

Questions or feedback? Reach out at [your-email]

---

**Last Updated**: January 2026
**Data Coverage**: 889 products across Amazon & Walmart
**Market Focus**: US Carbonated Soft Drinks (CSD)
