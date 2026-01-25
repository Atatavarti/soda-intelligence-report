import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="Soda Category Intelligence",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Brand colors
BRAND_COLORS = {
    'Coca-Cola': '#F40009', 'Pepsi': '#004B93', 'Dr Pepper': '#6B1C23',
    'Mountain Dew': '#A8CC3B', 'Sprite': '#00AF43', '7UP': '#00A550',
    'Fanta': '#FF8300', 'poppi': '#FFB6C1', 'OLIPOP': '#FF6B9D',
    'Diet Coke': '#B7B7B7', 'Coca-Cola Zero': '#000000', 'Zevia': '#00A86B',
    'Canada Dry': '#FFD700', 'Walmart Private Label': '#0071CE',
}

SODA_TYPE_COLORS = {
    'Traditional': '#E63946',
    'Diet': '#06A8B5',
    'Modern': '#06D6A0'
}

# Load data
@st.cache_data
def load_data():
    possible_paths = [
        'Master_Data_Final_Clean.xlsx',
        '/mnt/user-data/outputs/Master_Data_Final_Clean.xlsx',
        '../Master_Data_Final_Clean.xlsx',
    ]
    
    for path in possible_paths:
        try:
            df = pd.read_excel(path)
            return df
        except FileNotFoundError:
            continue
    
    st.error("Could not find Master_Data_Final_Clean.xlsx")
    st.stop()
    
df = load_data()

# Title
st.markdown("""
<h1 style='text-align: center; color: #1e3a8a; font-size: 3em; font-weight: bold;'>
🥤 Soda Category Intelligence Dashboard
</h1>
<p style='text-align: center; color: #666; font-size: 1.2em; margin-bottom: 10px;'>
Amazon & Walmart Market Analysis | 889 Products
</p>
<p style='text-align: center; color: #999; font-size: 0.9em; margin-bottom: 30px;'>
by Archana Tatavarthi
</p>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📦 Amazon Analysis", "🔄 Walmart & Cross-Platform", "🌐 Online vs Offline Reality"])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab1:
    st.header("Project Overview")
    
    # Purpose
    st.subheader("Purpose")
    st.markdown("""
    This dashboard analyzes the US carbonated soft drink (CSD) market across three key categories: 
    **Traditional** (Coca-Cola, Pepsi, Dr Pepper), **Diet** (Diet Coke, Coke Zero), and **Modern** 
    (poppi, OLIPOP, Zevia). The analysis highlights emerging trends in functional sodas and compares 
    online versus offline market dynamics to understand channel-specific consumer behavior.
    """)
    
    st.markdown("---")
    
    # Methodology
    st.subheader("Methodology")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
            <h4 style='margin-top: 0;'>Amazon Analysis (436 Products)</h4>
            <p><strong>Revenue Estimation:</strong></p>
            <ul>
                <li>Based on "units sold last month" data (80% coverage)</li>
                <li>Type-specific multipliers applied</li>
                <li>Provides current velocity metrics</li>
            </ul>
            <p><strong>Velocity Score (0-100):</strong></p>
            <ul>
                <li><strong>Formula:</strong> 100 - (ln(BSR) × 10.857)</li>
                <li><strong>BSR</strong> = Best Sellers Rank (Amazon's hourly ranking)</li>
                <li><strong>Examples:</strong> BSR 1 = 100 velocity | BSR 10 = 75 | BSR 100 = 50</li>
                <li>Logarithmic scale captures diminishing returns</li>
            </ul>
            <p><strong>Coverage:</strong> 87% of products have BSR data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3;'>
            <h4 style='margin-top: 0;'>Walmart Analysis (453 Products)</h4>
            <p><strong>Revenue Proxy:</strong></p>
            <ul>
                <li><strong>Formula:</strong> Reviews × Price</li>
                <li>Historical popularity indicator</li>
                <li>NOT real-time velocity</li>
            </ul>
            <p><strong>Use Cases:</strong></p>
            <ul>
                <li>✅ Brand presence comparison</li>
                <li>✅ Relative ranking</li>
                <li>✅ Historical trends</li>
                <li>❌ NOT for current sales velocity</li>
                <li>❌ NOT for absolute revenue</li>
            </ul>
            <p><strong>Note:</strong> Walmart data complements Amazon but uses different metrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Scope
    st.subheader("Data Scope")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", "889", help="436 Amazon + 453 Walmart")
        
    with col2:
        amazon_revenue = df[df['Platform'] == 'Amazon']['estimated_monthly_revenue'].sum()
        st.metric("Amazon Monthly Revenue", f"${amazon_revenue/1e6:.2f}M")
    
    with col3:
        modern_pct = len(df[(df['Platform'] == 'Amazon') & (df['soda_type'] == 'Modern')]) / len(df[df['Platform'] == 'Amazon']) * 100
        st.metric("Modern % (Amazon)", f"{modern_pct:.0f}%", help="25% on Amazon vs 3-4% offline")
    
    # Category breakdown
    st.markdown("""
    <div style='background: #f5f5f5; padding: 20px; border-radius: 10px; margin-top: 20px;'>
        <h4 style='margin-top: 0;'>Soda Type Definitions:</h4>
        <ul>
            <li><strong>Traditional:</strong> Classic sodas (Coca-Cola, Pepsi, Dr Pepper, Mountain Dew, Sprite)</li>
            <li><strong>Diet:</strong> Zero/low-calorie variants (Diet Coke, Pepsi Zero, Coke Zero Sugar)</li>
            <li><strong>Modern:</strong> Functional/prebiotic sodas (poppi, OLIPOP, Zevia, Bloom Nutrition, Culture Pop)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Findings Summary
    st.subheader("Key Findings at a Glance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;'>
            <h4 style='margin-top: 0;'>Amazon Insights</h4>
            <ul>
                <li>poppi & OLIPOP control 67.5% of modern soda revenue</li>
                <li>Modern sodas: 2.4x price premium yet highest velocity</li>
                <li>Coca-Cola Company leads overall (36.6% parent share)</li>
                <li>PepsiCo doubled share post-poppi acquisition (8.8% → 17.8%)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
            <h4 style='margin-top: 0;'>Market Reality</h4>
            <ul>
                <li>Total US CSD market: $50-55B (offline-dominant)</li>
                <li>Modern sodas: 3-4% offline vs 25% on Amazon (6-8x over-index)</li>
                <li>Online represents ~5% of total CSD sales</li>
                <li>Traditional brands still dominate 95%+ of volume</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    **💡 Strategic Implication:** Amazon serves as a discovery and trial channel for modern sodas. 
    DTC brands over-index online due to search-driven discovery, review influence, and subscription behavior. 
    However, offline distribution (convenience stores, restaurants, vending) remains critical for scale.
    """)
    
    # Data sources
    st.markdown("---")
    st.markdown("""
    **📚 Data Sources:**
    - Market sizing: Mintel ($55.2B), Circana ($46.1B, $1.8B modern sodas)
    - Brand share: Beverage Digest, Gitnux
    - Product data: Amazon & Walmart web scraping (January 2026)
    """)

# ============================================================================
# TAB 2: AMAZON ANALYSIS (REORGANIZED)
# ============================================================================

with tab2:
    st.header("Amazon Soda Category Analysis")
    
    amazon_df = df[df['Platform'] == 'Amazon'].copy()
    amazon_filtered = amazon_df.copy()  # No filters - show all data
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", len(amazon_filtered))
    
    with col2:
        total_revenue = amazon_filtered['estimated_monthly_revenue'].sum()
        st.metric("Est. Monthly Revenue", f"${total_revenue/1e6:.2f}M")
    
    with col3:
        revenue_per_sku = total_revenue / len(amazon_filtered)
        st.metric("Revenue per SKU", f"${revenue_per_sku/1000:.1f}K",
                 help="Modern brands: $46K | Traditional: $10K avg")
    
    st.markdown("---")
    
    # SECTION 1: Revenue Distribution & Performance
    st.subheader("Revenue Distribution & Performance")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Top 10 Individual Brands - FIXED FORMATTING
        st.markdown("**Top 10 Individual Brands**")
        brand_revenue = amazon_filtered.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=brand_revenue.index,
            x=brand_revenue.values / 1000,  # Convert to K
            orientation='h',
            marker=dict(color=[BRAND_COLORS.get(brand, '#95E1D3') for brand in brand_revenue.index]),
            text=brand_revenue.values / 1000,  # Show in K
            texttemplate='$%{text:.0f}K',  # FIXED: Show K not M
            textposition='outside'
        ))
        fig.update_layout(
            xaxis_title="Revenue ($K)",
            yaxis_title="",
            height=400,
            showlegend=False,
            margin=dict(l=150, r=100, t=40, b=40)
        )
        fig.update_xaxes(showgrid=True, gridcolor='lightgray', range=[0, brand_revenue.max()/1000 * 1.15])  # Add 15% padding
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Parent Brand Revenue Share - NEW PIE CHART
        st.markdown("**Parent Company Market Share**")
        parent_revenue = amazon_filtered.groupby('parent_brand')['estimated_monthly_revenue'].sum().sort_values(ascending=False).head(5)
        
        fig = px.pie(
            values=parent_revenue.values,
            names=parent_revenue.index,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        fig.update_layout(showlegend=False, height=400, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Show percentages
        total_rev = parent_revenue.sum()
        for parent, rev in parent_revenue.items():
            pct = (rev / total_rev) * 100
            st.markdown(f"**{parent}:** {pct:.1f}%")
    
    st.markdown("""
    <div style='background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>💡 Brand vs Parent Company:</h4>
        <ul style='line-height: 2;'>
            <li><strong>Individual brands:</strong> Coca-Cola ($743K) similar to poppi ($742K)</li>
            <li><strong>Parent companies:</strong> Coca-Cola Company ($2.6M) much larger than PepsiCo ($1.7M)</li>
            <li><strong>Why?</strong> Coca-Cola Company owns 12+ brands (Diet Coke, Coke Zero, Sprite, Health-Ade, etc.) - excludes fountain/foodservice</li>
            <li>🔥 <strong>Recent Acquisition:</strong> poppi acquired by PepsiCo (2025) - doubled PepsiCo market share from 8.8% to 17.8%</li>
            <li><strong>OLIPOP remains independent</strong> - the last major standalone modern soda brand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SECTION 2: Brand Leaders within Each Soda Type
    st.subheader("Brand Leaders within Each Soda Type")
    
    st.info("**Insight:** Modern sodas command 2.4x premium pricing ($1.34/oz vs $0.57/oz traditional) yet maintain strong velocity, demonstrating consumers' willingness to pay more for functional benefits like prebiotics and adaptogens.")
    
    col1, col2, col3 = st.columns(3)
    
    # Modern Brands
    with col1:
        modern_df = amazon_filtered[amazon_filtered['soda_type'] == 'Modern']
        modern_total = modern_df['estimated_monthly_revenue'].sum()
        modern_brands = modern_df.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False)
        
        # Group smaller brands as "Others"
        top_brands = modern_brands.head(4)
        others = modern_brands.iloc[4:].sum()
        
        if others > 0:
            plot_data = pd.concat([top_brands, pd.Series({'Others': others})])
        else:
            plot_data = top_brands
        
        fig = px.pie(
            values=plot_data.values,
            names=plot_data.index,
            title="Modern Soda Brands",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
        fig.update_layout(showlegend=False, height=300, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Total Modern Revenue", f"${modern_total/1e6:.2f}M")
    
    # Traditional Brands
    with col2:
        trad_df = amazon_filtered[amazon_filtered['soda_type'] == 'Traditional']
        trad_total = trad_df['estimated_monthly_revenue'].sum()
        trad_brands = trad_df.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False)
        
        # Group smaller brands as "Others"
        top_brands = trad_brands.head(5)
        others = trad_brands.iloc[5:].sum()
        
        if others > 0:
            plot_data = pd.concat([top_brands, pd.Series({'Others': others})])
        else:
            plot_data = top_brands
        
        fig = px.pie(
            values=plot_data.values,
            names=plot_data.index,
            title="Traditional Soda Brands",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
        fig.update_layout(showlegend=False, height=300, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Total Traditional Revenue", f"${trad_total/1e6:.2f}M")
    
    # Diet Brands
    with col3:
        diet_df = amazon_filtered[amazon_filtered['soda_type'] == 'Diet']
        diet_total = diet_df['estimated_monthly_revenue'].sum()
        diet_brands = diet_df.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False)
        
        # Group smaller brands as "Others"
        top_brands = diet_brands.head(5)
        others = diet_brands.iloc[5:].sum()
        
        if others > 0:
            plot_data = pd.concat([top_brands, pd.Series({'Others': others})])
        else:
            plot_data = top_brands
        
        fig = px.pie(
            values=plot_data.values,
            names=plot_data.index,
            title="Diet Soda Brands",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
        fig.update_layout(showlegend=False, height=300, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Total Diet Revenue", f"${diet_total/1e6:.2f}M")
    
    st.success("""
    **Key Takeaways:**
    - **Modern:** poppi & OLIPOP together control 67.5% of modern soda revenue on Amazon
    - **Traditional:** Coca-Cola leads at 25.5%, with Dr Pepper (9.9%) and Mountain Dew (9.5%) close behind
    - **Diet:** Diet Coke & Coke Zero dominate with 55.6% combined share
    """)
    
    st.markdown("---")
    
    # SECTION 3: Parent Brand Deep Dive
    st.markdown("<div id='parent-brand-dive'></div>", unsafe_allow_html=True)
    st.subheader("Parent Brand Deep Dive")
    
    st.info("💡 **Note:** Changing the selection will refresh the page. Your selection will persist.")
    
    parent_revenue = amazon_filtered.groupby('parent_brand')['estimated_monthly_revenue'].sum().sort_values(ascending=False)
    top_parents = parent_revenue.head(10).index.tolist()
    
    selected_parent = st.selectbox(
        "Select Parent Brand:",
        options=top_parents,
        key='parent_brand_selector',
        help="Analyze sub-brand performance within parent company"
    )
    
    parent_df = amazon_filtered[amazon_filtered['parent_brand'] == selected_parent]
    parent_total_revenue = parent_df['estimated_monthly_revenue'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total SKUs", len(parent_df))
    with col2:
        st.metric("Total Revenue", f"${parent_total_revenue/1e6:.2f}M")
    with col3:
        market_share = (parent_total_revenue / amazon_filtered['estimated_monthly_revenue'].sum() * 100)
        st.metric("Market Share", f"{market_share:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sub-Brand Revenue Breakdown**")
        subbrand_revenue = parent_df.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False).head(5)
        
        fig = px.pie(
            values=subbrand_revenue.values,
            names=subbrand_revenue.index,
            color=subbrand_revenue.index,
            color_discrete_map=BRAND_COLORS
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        fig.update_layout(showlegend=False, height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Top 5 SKUs by Revenue**")
        top_skus = parent_df.nlargest(5, 'estimated_monthly_revenue')[
            ['brand_clean', 'title', 'estimated_monthly_revenue', 'velocity_score', 'pack_size']
        ]
        
        for idx, row in top_skus.iterrows():
            title_short = row['title'][:40] + '...' if len(row['title']) > 40 else row['title']
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{row['brand_clean']}** - {title_short}")
            with col_b:
                st.markdown(f"${row['estimated_monthly_revenue']/1000:.0f}K")
    
    st.markdown("---")
    
    # SECTION 4: Soda Type Analysis - MODIFIED (Velocity + Price)
    st.subheader("Soda Type Performance: Velocity & Pricing")
    
    type_analysis = amazon_filtered.groupby('soda_type').agg({
        'velocity_score': 'mean',
        'estimated_monthly_revenue': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Velocity Score by Type - NEW CHART
        st.markdown("**Average Velocity Score by Type**")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=type_analysis['soda_type'],
            y=type_analysis['velocity_score'],
            marker_color=[SODA_TYPE_COLORS[t] for t in type_analysis['soda_type']],
            text=type_analysis['velocity_score'].apply(lambda x: f'{x:.1f}'),
            textposition='outside'
        ))
        fig.update_layout(
            xaxis_title="Soda Type",
            yaxis_title="Avg Velocity Score",
            height=300,
            showlegend=False,
            margin=dict(t=40, b=50)
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', range=[0, 50])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue-weighted price per oz
        st.markdown("**Avg Price per Oz by Type (Revenue-Weighted)**")
        type_price_oz_data = []
        for soda_type in ['Modern', 'Traditional', 'Diet']:
            type_df = amazon_filtered[(amazon_filtered['soda_type'] == soda_type) & 
                                     (amazon_filtered['price_per_oz'].notna()) & 
                                     (amazon_filtered['estimated_monthly_revenue'].notna())]
            if len(type_df) > 0:
                total_revenue = type_df['estimated_monthly_revenue'].sum()
                weighted_price_oz = (type_df['price_per_oz'] * type_df['estimated_monthly_revenue']).sum() / total_revenue
                type_price_oz_data.append({'soda_type': soda_type, 'price_per_oz': weighted_price_oz})
        
        type_price_oz = pd.DataFrame(type_price_oz_data).sort_values('price_per_oz', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=type_price_oz['soda_type'],
            y=type_price_oz['price_per_oz'],
            marker_color=[SODA_TYPE_COLORS[t] for t in type_price_oz['soda_type']],
            text=type_price_oz['price_per_oz'].apply(lambda x: f'${x:.2f}/oz'),
            textposition='outside'
        ))
        fig.update_layout(
            xaxis_title="Soda Type",
            yaxis_title="Price per Oz ($)",
            height=300,
            showlegend=False,
            margin=dict(t=40, b=50)
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', range=[0, 1.6])
        st.plotly_chart(fig, use_container_width=True)
    
    # Combined Insight Box - NEW
    st.success("""
    **🎯 Modern Soda Performance Paradox:**
    
    Modern sodas combine premium positioning with superior performance:
    - **Highest velocity score:** 45.6 (vs 36.2 traditional, 41.8 diet)
    - **Premium pricing:** $1.34/oz (2.4x traditional at $0.57/oz, 2.7x diet at $0.50/oz)
    - **Smaller trial packs:** 3.7 avg pack size (vs 6.2 traditional)
    
    **Key Insight:** Consumers willing to pay significantly more for functional benefits like prebiotics and adaptogens, 
    proving modern sodas have achieved product-market fit despite substantial price premium. High velocity + high price = 
    strong value proposition and brand loyalty.
    """)
    
    st.markdown("---")

    # SECTION 5: High Velocity & Surprising Winners
    st.subheader("High-Velocity Products & Market Surprises")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Top 10 Highest Velocity Products**")
        high_velocity = amazon_filtered.nlargest(10, 'velocity_score')[
            ['brand_clean', 'title', 'velocity_score', 'soda_type']
        ]
        
        for idx, row in high_velocity.iterrows():
            title_short = row['title'][:45] + '...' if len(row['title']) > 45 else row['title']
            col_a, col_b, col_c = st.columns([2, 1, 1])
            with col_a:
                st.markdown(f"{title_short}")
            with col_b:
                type_color = SODA_TYPE_COLORS[row['soda_type']]
                st.markdown(f"<span style='background-color: {type_color}; padding: 2px 8px; border-radius: 4px; color: white;'>{row['soda_type']}</span>", unsafe_allow_html=True)
            with col_c:
                st.markdown(f"**{row['velocity_score']:.1f}**")
    
    with col2:
        st.markdown("**🎯 Key Observation**")
        
        modern_in_top10 = len(high_velocity[high_velocity['soda_type'] == 'Modern'])
        
        st.markdown(f"""
        <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 5px solid #4caf50;'>
            <p style='margin: 0; font-size: 14px;'><strong>{modern_in_top10}/10 top velocity products are Modern sodas!</strong></p>
            <br>
            <p style='margin: 0; font-size: 13px;'>Modern brands dominate high-velocity segment</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Surprising Winners
    st.subheader("Surprising Market Dynamics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Brands Outperforming Pepsi ($309K)**")
        
        surprising_brands = [
            ('poppi', 742, 140),
            ('OLIPOP', 713, 131),
            ('Diet Coke', 683, 121),
            ('Coca-Cola Zero', 510, 65),
            ('Dr Pepper', 440, 43),
        ]
        
        for brand, revenue, vs_pepsi in surprising_brands:
            st.markdown(f"**{brand}:** ${revenue}K ({vs_pepsi:+.0f}% vs Pepsi)")
    
    with col2:
        st.markdown("**⚡ Bloom Nutrition: SKU Efficiency Leader**")
        st.markdown("""
        **Revenue:** $233K with just 2 SKUs
        
        **Revenue per SKU:** $116K
        - Bloom: $116K/SKU
        - poppi: $46K/SKU  
        - OLIPOP: $32K/SKU
        
        Proves wellness + influencer marketing can drive massive performance.
        """)
    
    st.success("""
    **Key Takeaway:** On Amazon, brand size doesn't guarantee success. Modern brands with strong product-market fit 
    can outperform traditional giants through search discovery and review influence.
    """)

# ============================================================================
# TAB 3: WALMART & CROSS-PLATFORM (KEEP AS IS FROM ORIGINAL)
# ============================================================================

with tab3:
    st.header("Walmart Analysis")
    
    walmart_df = df[df['Platform'] == 'Walmart'].copy()
    walmart_filtered = walmart_df.copy()  # No filters - show all data
    
    # Key Metrics
    st.markdown("### Walmart Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", len(walmart_filtered))
    
    with col2:
        total_proxy = walmart_filtered['revenue_proxy'].sum()
        st.metric("Revenue Proxy", f"${total_proxy/1e6:.2f}M", 
                 help="Reviews × Price (historical indicator)")
    
    with col3:
        avg_price = walmart_filtered['price'].mean()
        st.metric("Avg Price", f"${avg_price:.2f}")
    
    st.markdown("---")
    
    # Distribution Analysis
    st.subheader("Product Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Type distribution
        type_dist = walmart_filtered.groupby('soda_type')['asin'].count()
        
        fig = px.pie(
            values=type_dist.values,
            names=type_dist.index,
            title="Product Count by Type",
            color=type_dist.index,
            color_discrete_map=SODA_TYPE_COLORS
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pack size distribution
        pack_dist = walmart_filtered.groupby('pack_size')['asin'].count().sort_values(ascending=False).head(6)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{int(p)}-pack" for p in pack_dist.index],
            y=pack_dist.values,
            marker_color='#4ECDC4'
        ))
        fig.update_layout(
            title="Pack Size Distribution",
            xaxis_title="Pack Size",
            yaxis_title="Product Count",
            height=300,
            showlegend=False
        )
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Revenue Proxy Leaders
    st.subheader("Revenue Proxy Leaders")
    
    st.info("""
    **Formula Explained:** `Reviews × Price` = Historical popularity indicator
    - High reviews + High price = Strong lifetime performance
    - Use for relative comparisons, NOT absolute revenue
    """)
    
    top_proxy = walmart_filtered.nlargest(10, 'revenue_proxy')[
        ['brand_clean', 'title', 'review_count', 'price', 'revenue_proxy']
    ]
    
    for idx, row in top_proxy.iterrows():
        col_a, col_b, col_c = st.columns([3, 2, 1])
        with col_a:
            title_short = row['title'][:50] + '...' if len(row['title']) > 50 else row['title']
            st.markdown(f"**{row['brand_clean']}** - {title_short}")
        with col_b:
            st.markdown(f"{int(row['review_count']):,} reviews × ${row['price']:.2f}")
        with col_c:
            st.markdown(f"**${row['revenue_proxy']/1000:.0f}K**")
    
    st.markdown("---")
    
    # Private Label Analysis
    st.subheader("Walmart Private Label vs Branded")
    
    # Calculate private label stats
    walmart_filtered['is_private'] = walmart_filtered['brand_clean'].apply(
        lambda x: any(brand.lower() in str(x).lower() for brand in ['great value', 'sam', 'member']) if pd.notna(x) else False
    )
    
    private_df = walmart_filtered[walmart_filtered['is_private'] == True]
    branded_df = walmart_filtered[walmart_filtered['is_private'] == False]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        private_count = len(private_df)
        total_count = len(walmart_filtered)
        st.metric("Private Label SKUs", f"{private_count} ({private_count/total_count*100:.1f}%)")
    
    with col2:
        private_proxy = private_df['revenue_proxy'].sum()
        total_proxy = walmart_filtered['revenue_proxy'].sum()
        st.metric("Private Label Revenue Proxy", f"${private_proxy/1e6:.2f}M ({private_proxy/total_proxy*100:.1f}%)")
    
    with col3:
        price_discount = (1 - private_df['price'].mean() / branded_df['price'].mean()) * 100
        st.metric("Avg Price Discount", f"{price_discount:.0f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top Private Label Products:**")
        top_private = private_df.nlargest(5, 'revenue_proxy')[['title', 'price', 'review_count', 'revenue_proxy']]
        for idx, row in top_private.iterrows():
            title_clean = row['title'].replace('Great Value', 'GV').replace('Soda Pop', '')[:45]
            st.markdown(f"• **{title_clean}** - ${row['price']:.2f} ({int(row['review_count'])} reviews)")
    
    with col2:
        st.markdown("**Key Insights:**")
        st.markdown(f"""
        - **Dr Thunder** (GV's Dr Pepper) leads private label sales
        - **Mountain Lightning** (GV's Mountain Dew) #2
        - **64% cheaper** than branded equivalents on average
        - **Strong review counts** (3K-5K reviews) = loyal customer base
        - Private label captures **<2%** revenue proxy despite 6% SKUs
        - Branded sodas maintain dominance even at premium prices
        """)
    
    st.info("""
    **Private Label Strategy:** Walmart focuses on copycat flavors (Dr Thunder = Dr Pepper, Mountain Lightning = Mountain Dew) 
    at steep discounts (64%). Despite low price, private label only captures 1.6% revenue proxy, showing strong brand loyalty 
    for traditional sodas even on value-focused platform.
    """)
    
    # Cross-Platform Comparison Section
    st.markdown("---")
    st.markdown("## 🔄 Cross-Platform Comparison")
    
    st.subheader("💵 Price Comparison: Amazon vs Walmart")
    
    # Brand price comparison
    brands_both_platforms = []
    for brand in df['brand_clean'].unique():
        amazon_brand = amazon_df[amazon_df['brand_clean'] == brand]
        walmart_brand = walmart_df[walmart_df['brand_clean'] == brand]
        
        if len(amazon_brand) > 0 and len(walmart_brand) > 0:
            brands_both_platforms.append({
                'brand': brand,
                'amazon_price': amazon_brand['price'].mean(),
                'walmart_price': walmart_brand['price'].mean()
            })
    
    if brands_both_platforms:
        comparison_df = pd.DataFrame(brands_both_platforms).sort_values('amazon_price', ascending=False).head(8)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Amazon',
            y=comparison_df['brand'],
            x=comparison_df['amazon_price'],
            orientation='h',
            marker_color='#FF9800',
            text=comparison_df['amazon_price'].apply(lambda x: f'${x:.2f}'),
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Walmart',
            y=comparison_df['brand'],
            x=comparison_df['walmart_price'],
            orientation='h',
            marker_color='#0071CE',
            text=comparison_df['walmart_price'].apply(lambda x: f'${x:.2f}'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Average Price by Brand: Amazon vs Walmart",
            xaxis_title="Average Price ($)",
            height=400,
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_yaxes(title="Brand")
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        st.plotly_chart(fig, use_container_width=True)
    
    # Platform summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;'>
            <h4>🏪 Platform Differences</h4>
            <ul>
                <li><strong>Walmart:</strong> 37% bulk packs (grocery stocking)</li>
                <li><strong>Amazon:</strong> 27% bulk packs (variety focus)</li>
                <li><strong>Price gap:</strong> Walmart 50-60% cheaper</li>
                <li><strong>Behavior:</strong> Essentials vs Discovery</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
            <h4>⚠️ Use Cases</h4>
            <ul>
                <li><strong>Good for:</strong> Brand presence, relative ranking</li>
                <li><strong>Good for:</strong> Historical popularity trends</li>
                <li><strong>Not for:</strong> Current velocity estimates</li>
                <li><strong>Not for:</strong> Absolute revenue comparison</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# TAB 4: ONLINE VS OFFLINE REALITY
# ============================================================================

with tab4:
    st.header("Online vs Offline Reality")
    
    # Section 1: Market Size Comparison
    st.subheader("Market Context: Online vs Offline Distribution")
    
    st.info("""
    **Key Context:** 
    - **Total US CSD Market**: ~$50-55B annually (CSD = Carbonated Soft Drinks: all fizzy sodas)
    - **Online CSD Sales**: ~5% of total market (~$2.5-2.8B)
    - **This Dashboard**: Tracks ~$86M annually in Amazon ASINs (436 products = sample of Amazon soda category)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Offline CSD Market (Dominant)**")
        st.markdown("""
        **Total Market Size:** ~$50B annually
        - Represents ~95% of total CSD sales
        
        **Modern Soda Share:** 3-4% ($1.8B)
        - Growing 83% YoY
        - Still niche in traditional retail
        
        **Category Breakdown:**
        - Coca-Cola brands: ~45%
        - PepsiCo brands: ~26%
        - Keurig Dr Pepper: ~21%
        - **Modern sodas: 3-4%**
        - Others: ~4-5%
        
        **Distribution Channels:**
        - Convenience stores, gas stations
        - Restaurants, fast food (fountain)
        - Grocery stores, supermarkets
        - Vending machines, stadiums
        
        *Sources: Circana, Beverage Digest*
        """)
    
    with col2:
        st.markdown("### **Amazon Sample (This Dashboard)**")
        st.markdown("""
        **Tracked Revenue:** ~$86M annually
        - 436 Amazon products analyzed
        - Subset of Amazon's total soda sales
        - Amazon itself = small % of total market
        
        **Modern Soda Share:** 25% (of tracked ASINs)
        - **6-8x OVER-INDEXED** vs offline
        - Shows online shopping behavior
        - NOT representative of total market
        
        **Category Breakdown (Our Data):**
        - Traditional: 44%
        - Diet: 31%
        - **Modern: 25%** ⚠️
        
        **Why Over-Index Happens:**
        - Search-driven product discovery
        - Subscription/auto-replenish behavior
        - Review-influenced purchasing
        - DTC brand strategy (Amazon-first)
        - Higher price tolerance online
        
        **The Math:**
        - Offline modern share: 3.5%
        - Amazon modern share: 25%
        - Over-index: 25 ÷ 3.5 = **7x**
        """)
    
    st.success("""
    **🎯 Key Takeaway:** Modern sodas capture 25% of our tracked Amazon sample but only 3-4% of the total offline market. 
    This 6-8x over-representation reveals Amazon as a discovery and trial channel for premium/functional beverages, 
    NOT a predictor of offline market share. Amazon amplifies certain brands due to platform dynamics (search, reviews, DTC strategy), 
    but 95%+ of soda sales still happen offline where traditional brands dominate.
    """)
    
    st.markdown("---")
    
    # Section 2: Why Modern Brands Over-Index on Amazon
    st.subheader("Why Modern Sodas Dominate Amazon (But Not Offline)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;'>
            <h4>✅ Amazon Advantages for Modern Brands</h4>
            <ul>
                <li><strong>Search Discovery:</strong> "Healthy soda" "prebiotic soda" → Modern brands rank #1</li>
                <li><strong>Review Influence:</strong> 4.5-star ratings drive conversions</li>
                <li><strong>Subscription Model:</strong> 15-20% subscribe & save adoption</li>
                <li><strong>DTC Strategy:</strong> Modern brands prioritize Amazon (higher margins)</li>
                <li><strong>No Shelf Space Battle:</strong> Equal visibility vs Coke/Pepsi</li>
                <li><strong>Content Rich:</strong> Product descriptions educate on benefits</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
            <h4>⚠️ Offline Challenges for Modern Brands</h4>
            <ul>
                <li><strong>Limited Distribution:</strong> Not in gas stations, vending machines</li>
                <li><strong>Shelf Space Battle:</strong> Coke/Pepsi control 70%+ of space</li>
                <li><strong>Impulse Purchase:</strong> Traditional sodas dominate point-of-sale</li>
                <li><strong>Price Perception:</strong> $2.50/can seems expensive next to $1 Coke</li>
                <li><strong>Brand Awareness:</strong> Low recognition outside health-conscious demo</li>
                <li><strong>Restaurant/Fountain:</strong> Zero presence in foodservice</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section 3: Strategic Implications
    st.subheader("Strategic Implications & M&A Context")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2196f3 0%, #03a9f4 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h4 style='margin-top: 0; color: white;'>🎯 Why PepsiCo Paid $1.95B for poppi</h4>
        <p style='margin: 0; font-size: 15px; line-height: 1.8;'>
            PepsiCo wasn't buying current market share (3-4% offline). They were buying:<br>
            <br>
            1️⃣ <strong>Online Dominance:</strong> poppi owns Amazon discovery (25% tracked share)<br>
            2️⃣ <strong>Offline Potential:</strong> Expand poppi to PepsiCo's massive distribution network<br>
            3️⃣ <strong>Consumer Trend:</strong> Gen Z/Millennials shifting to functional beverages<br>
            4️⃣ <strong>Growth Trajectory:</strong> Modern soda market growing 83% YoY (Circana)<br>
            5️⃣ <strong>Competitive Response:</strong> Coca-Cola launched Simply Pop; PepsiCo needed modern play<br>
            <br>
            <strong>The Playbook:</strong> Win Online → Leverage CPG Distribution → Scale Offline
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**The Acquisition Strategy**")
        st.markdown("""
        - **Buy:** PepsiCo acquired poppi ($1.95B, 2025)
        - **Build:** Coca-Cola launched Simply Pop (Feb 2024)
        - **Battle:** Both giants competing in modern soda space
        - **Target:** OLIPOP remains independent (next acquisition target?)
        """)
    
    with col2:
        st.markdown("**Expected Impact**")
        st.markdown("""
        - PepsiCo can 10x poppi distribution overnight
        - Walmart, Target, 7-Eleven shelf space secured
        - Fountain/foodservice potential unlocked
        - Modern sodas could reach 10-15% offline in 5 years
        """)
    
    st.info("""
    **💡 Lesson for Operators:** Amazon performance signals consumer demand but doesn't guarantee offline success. 
    Modern brands need traditional CPG muscle (distribution, relationships, capital) to scale offline. 
    This explains why acquisitions (poppi) or partnerships become necessary for category growth.
    """)
    
    st.markdown("---")
    
    # Final Summary
    st.subheader("Summary: Online vs Offline Dynamics")
    
    st.markdown("""
    <div style='background: #f5f5f5; padding: 25px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>🔑 Key Points to Remember:</h4>
        <ol style='line-height: 2;'>
            <li><strong>Amazon ≠ Total Market:</strong> This dashboard shows 436 Amazon products, not the $50-55B CSD market</li>
            <li><strong>Online = 5% of Sales:</strong> 95% of sodas sold offline (convenience, restaurants, vending)</li>
            <li><strong>Modern Sodas Over-Index 6-8x Online:</strong> 25% Amazon vs 3-4% offline</li>
            <li><strong>Different Consumer Behaviors:</strong> Online = discovery/trial, Offline = habit/impulse</li>
            <li><strong>M&A Driven by Online Signals:</strong> Amazon success validates consumer demand, justifies acquisitions</li>
            <li><strong>Distribution Still King:</strong> Modern brands need traditional CPG muscle to scale offline</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    *Data Sources: Circana ($1.8B modern sodas, 83% growth), Beverage Digest (brand shares)*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 40px;'>
    <p style='font-size: 14px; margin-bottom: 10px;'>
        <strong>Created by Archana Tatavarthi</strong> | 
        <a href='https://www.linkedin.com/in/archana-tatavarti/' target='_blank' style='color: #0077b5; text-decoration: none;'>LinkedIn</a>
    </p>
    <p style='color: #999; font-size: 12px;'>
        Data: 889 products (Amazon + Walmart) | Methodology: BSR-based velocity scoring + Revenue-weighted metrics
    </p>
</div>
""", unsafe_allow_html=True)
