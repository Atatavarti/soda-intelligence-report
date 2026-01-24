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
    'Traditional': '#FF6B6B',
    'Diet': '#4ECDC4',
    'Modern': '#95E1D3'
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

# Title with dark blue color
st.markdown("""
<h1 style='text-align: center; color: #1e3a8a; font-size: 3em; font-weight: bold;'>
🥤 Soda Category Intelligence Dashboard
</h1>
<p style='text-align: center; color: #666; font-size: 1.2em; margin-bottom: 30px;'>
Amazon & Walmart Market Analysis | 914 Products
</p>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📦 Amazon Analysis", "🔄 Walmart & Cross-Platform", "🌐 Online vs Offline Reality"])

# ============================================================================
# TAB 1: AMAZON ANALYSIS
# ============================================================================

with tab1:
    st.header("Amazon Soda Category Analysis")
    
    # Soda Type Definitions
    st.markdown("""
    <div style='background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 20px;'>
        <p style='margin: 0; font-size: 14px;'><strong>📚 Category Definitions:</strong></p>
        <ul style='margin: 5px 0 0 0; padding-left: 20px; font-size: 13px;'>
            <li><strong>Traditional:</strong> Classic sodas (Coca-Cola, Pepsi, Dr Pepper, Mountain Dew, Sprite)</li>
            <li><strong>Diet:</strong> Zero/low-calorie variants (Diet Coke, Pepsi Zero, Coke Zero Sugar)</li>
            <li><strong>Modern:</strong> Health-focused functional sodas (poppi, OLIPOP, Zevia - prebiotics, adaptogens, low sugar)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Methodology
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h3 style='margin-top: 0; color: white;'>📊 METHODOLOGY</h3>
        <ul style='margin-bottom: 0; line-height: 1.8;'>
            <li><strong>Revenue:</strong> Based on actual "units sold last month" (80% coverage) + type-specific multipliers</li>
            <li><strong>Velocity Score (0-100):</strong> Logarithmic BSR conversion
                <ul>
                    <li><strong>Formula:</strong> 100 - (ln(BSR) × 10.857)</li>
                    <li><strong>BSR</strong> = Amazon Best Sellers Rank (updated hourly, lower = better)</li>
                    <li><strong>Examples:</strong> BSR 1 = 100 velocity | BSR 10 = 75 | BSR 100 = 50 | BSR 1,000 = 25</li>
                    <li><strong>Why log scale:</strong> Captures diminishing returns - difference between rank 1-10 matters more than 1000-1010</li>
                </ul>
            </li>
            <li><strong>Coverage:</strong> 96.5% products, 87% have BSR data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    amazon_df = df[df['Platform'] == 'Amazon'].copy()
    
    # Filters
    st.sidebar.header("🎯 Amazon Filters")
    amazon_types = st.sidebar.multiselect(
        "Soda Type",
        options=['Traditional', 'Diet', 'Modern'],
        default=['Traditional', 'Diet', 'Modern'],
        key='amazon_types'
    )
    
    amazon_filtered = amazon_df[amazon_df['soda_type'].isin(amazon_types)]
    
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
    
    # Section 1: Revenue Distribution & Performance
    st.subheader("📊 Revenue Distribution & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        type_revenue = amazon_filtered.groupby('soda_type')['estimated_monthly_revenue'].sum().reset_index()
        
        fig = px.pie(
            type_revenue,
            values='estimated_monthly_revenue',
            names='soda_type',
            color='soda_type',
            color_discrete_map=SODA_TYPE_COLORS,
            hole=0.5,
            title="Revenue Share by Soda Type"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
        fig.update_layout(showlegend=False, height=350, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        brand_revenue = amazon_filtered.groupby('brand_clean')['estimated_monthly_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        
        fig = px.bar(
            brand_revenue,
            x='estimated_monthly_revenue',
            y='brand_clean',
            orientation='h',
            color='brand_clean',
            color_discrete_map=BRAND_COLORS,
            title="Top 10 Individual Brands"
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            xaxis_title="Revenue ($M)",
            yaxis_title="",
            height=350,
            margin=dict(t=40)
        )
        fig.update_traces(texttemplate='$%{x:.2f}M', textposition='outside')
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **💡 Brand vs Parent Company:**
    - **Individual brands:** Coca-Cola ($743K) ≈ poppi ($742K) - similar size
    - **Parent companies:** Coca-Cola Company ($3.46M) >> PepsiCo ($1.47M)
    - **Why?** Coca-Cola Company owns 12 brands (Diet Coke, Coke Zero, Health-Ade kombucha, Sprite, etc.)
    - **🚨 Recent Acquisition:** poppi acquired by PepsiCo (2025) - doubled PepsiCo's market share from 8.8% → 17.8%!
    - **OLIPOP remains independent** - the last major standalone modern soda brand
    """)
    
    st.markdown("---")
    
    # Section 2: Soda Type Deep Dive
    st.subheader("🔬 Soda Type Analysis: Pack Size & Pricing")
    
    type_analysis = amazon_filtered.groupby('soda_type').agg({
        'pack_size': 'mean',
        'price': 'mean',
        'velocity_score': 'mean',
        'estimated_monthly_revenue': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=type_analysis['soda_type'],
            y=type_analysis['pack_size'],
            marker_color=[SODA_TYPE_COLORS[t] for t in type_analysis['soda_type']],
            text=type_analysis['pack_size'].apply(lambda x: f'{x:.1f}'),
            textposition='outside',
            name='Avg Pack Size'
        ))
        fig.update_layout(
            title="Avg Pack Size by Type",
            xaxis_title="Soda Type",
            yaxis_title="Avg Pack Size",
            height=300,
            showlegend=False,
            margin=dict(t=50, b=50)
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', range=[0, 8])
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Modern:** Smaller packs (3.5) = trial focus\n\n**Traditional/Diet:** Larger (6.3) = bulk")
    
    with col2:
        # Revenue-weighted price per oz for accuracy
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
            textposition='outside',
            name='Price per Oz'
        ))
        fig.update_layout(
            title="Avg Price per Oz by Type (Revenue-Weighted)",
            xaxis_title="Soda Type",
            yaxis_title="Price per Oz ($)",
            height=300,
            showlegend=False,
            margin=dict(t=50, b=50)
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', range=[0, 1.6])
        st.plotly_chart(fig, use_container_width=True)
        
        modern_price = type_price_oz[type_price_oz['soda_type'] == 'Modern']['price_per_oz'].values[0] if len(type_price_oz[type_price_oz['soda_type'] == 'Modern']) > 0 else 0
        trad_price = type_price_oz[type_price_oz['soda_type'] == 'Traditional']['price_per_oz'].values[0] if len(type_price_oz[type_price_oz['soda_type'] == 'Traditional']) > 0 else 0
        diet_price = type_price_oz[type_price_oz['soda_type'] == 'Diet']['price_per_oz'].values[0] if len(type_price_oz[type_price_oz['soda_type'] == 'Diet']) > 0 else 0
        
        st.info(f"**Modern:** ${modern_price:.2f}/oz\n\n**Traditional:** ${trad_price:.2f}/oz\n\n**Diet:** ${diet_price:.2f}/oz\n\n*Revenue-weighted for accuracy*")
    
    st.markdown("---")
    
    # Section 3: Parent Brand Deep Dive
    st.markdown("<div id='parent-brand-dive'></div>", unsafe_allow_html=True)
    st.subheader("🏢 Parent Brand Deep Dive")
    
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
    
    # Section 4: Brand Share within Soda Types
    st.subheader("🏆 Brand Leaders within Each Soda Type")
    
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
    
    # Section 5: HIGH VELOCITY & FLAVOR INSIGHTS
    st.subheader("🚀 High-Velocity Products & Flavor Analysis")
    
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
            <p style='margin: 0; font-size: 13px;'>Modern brands dominate high-velocity segment with innovative flavors like Apple Cider, Crisp Apple</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Flavor analysis
    st.markdown("**🍎 Flavor Performance Analysis**")
    
    flavor_data = {
        'Cola': {'skus': 61, 'velocity': 44.6, 'revenue': 3034},
        'Apple': {'skus': 22, 'velocity': 53.6, 'revenue': 870},
        'Cherry': {'skus': 36, 'velocity': 43.1, 'revenue': 479},
        'Orange': {'skus': 34, 'velocity': 38.0, 'revenue': 545},
        'Root Beer': {'skus': 27, 'velocity': 40.5, 'revenue': 353},
    }
    
    flavor_df = pd.DataFrame(flavor_data).T.reset_index()
    flavor_df.columns = ['Flavor', 'SKUs', 'Avg Velocity', 'Revenue ($K)']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=flavor_df['Avg Velocity'],
        y=flavor_df['Revenue ($K)'],
        mode='markers+text',
        marker=dict(size=flavor_df['SKUs']*2, color=flavor_df['Avg Velocity'], 
                   colorscale='Viridis', showscale=True),
        text=flavor_df['Flavor'],
        textposition='top center',
        textfont=dict(size=11, color='black')
    ))
    fig.update_layout(
        title="Flavor Performance: Velocity vs Revenue (bubble size = SKU count)",
        xaxis_title="Average Velocity Score",
        yaxis_title="Total Revenue ($K)",
        height=350
    )
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**🏆 Apple flavor wins on velocity (53.6)** - driven by poppi & OLIPOP's Apple Cider variants. **Cola dominates revenue** with 61 SKUs.")
    
    st.markdown("---")
    
    # Section 5.5: SURPRISING MARKET DYNAMICS
    st.subheader("🎯 Surprising Market Dynamics: Unexpected Winners")
    
    st.markdown("""
    <div style='background: #fff9c4; padding: 20px; border-radius: 10px; border-left: 5px solid #fbc02d; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>💡 Brands That Challenge Conventional Wisdom</h4>
        <p style='margin: 0; font-size: 14px;'>
            Amazon's data reveals surprising performance patterns that contradict offline market dynamics.
            These insights show how online discovery changes the competitive landscape.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚀 Brands Outperforming Pepsi ($309K)**")
        
        surprising_brands = [
            ('poppi', 742, 140),
            ('OLIPOP', 713, 131),
            ('Diet Coke', 683, 121),
            ('Health-Ade', 614, 99),
            ('Coca-Cola Zero', 510, 65),
            ('Dr Pepper', 440, 43),
            ('sodastream', 313, 1)
        ]
        
        for brand, revenue, vs_pepsi in surprising_brands:
            st.markdown(f"**{brand}:** ${revenue}K ({vs_pepsi:+.0f}% vs Pepsi)")
    
    with col2:
        st.markdown("**⚡ Bloom Nutrition: The Stealth Performer**")
        st.markdown("""
        **Revenue:** $233K (with just 2 SKUs!)
        
        **Revenue per SKU:** $116K
        - poppi: $46K per SKU
        - OLIPOP: $32K per SKU
        - **Bloom: $116K per SKU** (2.5x poppi!)
        
        **Avg Velocity:** 57.1 (higher than poppi/OLIPOP)
        
        **Why It Matters:** Bloom shows extreme SKU efficiency. 
        Single product hitting $233K proves wellness + influencer 
        marketing can drive massive Amazon performance.
        """)
    
    st.success("""
    **🔥 Key Takeaway:** On Amazon, brand size doesn't guarantee success. poppi & OLIPOP EACH outsell Pepsi by 2x+. 
    Bloom Nutrition with 2 SKUs generates 75% of Pepsi's revenue (20 SKUs). Discovery-led platforms reward 
    product-market fit over distribution muscle.
    """)
    
    st.markdown("---")
    
    # Section 6: MODERN VS TRADITIONAL SHOWDOWN
    st.subheader("⚡ PepsiCo's Strategic Play: Acquiring Modern Soda Leader")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #004B93 0%, #95e1d3 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h3 style='margin-top: 0; color: white;'>🚨 MAJOR M&A MOVE: PEPSICO ACQUIRES POPPI (2025)</h3>
        <p style='margin: 0; font-size: 18px; line-height: 1.8;'>
            <strong>Before:</strong> PepsiCo = $731K (8.8% market share)<br>
            <strong>After:</strong> PepsiCo + poppi = $1,473K (17.8% market share)<br>
            <br>
            <strong>Impact:</strong> PepsiCo DOUBLED its market share by acquiring the #1 modern soda brand!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Traditional Portfolio (PepsiCo)**")
        pepsico_trad = {
            'Pepsi': 309,
            'Mountain Dew': 286,
            '7UP': 88,
            'Starry': 33
        }
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(pepsico_trad.keys()),
            y=list(pepsico_trad.values()),
            marker_color=['#004B93', '#A8CC3B', '#00A550', '#FFD700'],
            text=[f'${v}K' for v in pepsico_trad.values()],
            textposition='outside',
            name='Traditional Brands'
        ))
        fig.update_layout(
            title="PepsiCo Traditional Brands",
            yaxis_title="Revenue ($K)",
            height=300,
            showlegend=False
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"**Traditional Total: ${sum(pepsico_trad.values())}K**")
    
    with col2:
        st.markdown("**Modern Addition (poppi)**")
        
        # Show poppi dominance
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['poppi'],
            y=[742],
            marker_color='#FFB6C1',
            text=['$742K'],
            textposition='outside',
            name='Modern Brand'
        ))
        fig.update_layout(
            title="poppi (Acquired 2025)",
            yaxis_title="Revenue ($K)",
            height=300,
            showlegend=False
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', range=[0, 950])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"**poppi alone = $742K** (bigger than Pepsi brand!)")
    
    st.success("""
    **Why This Acquisition Makes Sense (Amazon Data Context):**
    - ✅ **On Amazon:** poppi ($742K) > Pepsi brand ($309K) - modern wins online
    - ✅ **Strategic gap:** PepsiCo weak in fast-growing online/modern category
    - ✅ **Distribution play:** Buy online dominance + offline expansion potential
    - ✅ **Future-proofing:** Gen Z/Millennials prefer functional beverages
    - ⚠️ **Reality check:** Modern = 25% Amazon vs 3-4% total market - PepsiCo buying growth trajectory
    """)
    
    st.warning("""
    **Strategic Implication:**
    - **OLIPOP ($713K) now the ONLY independent modern soda leader**
    - **Both PepsiCo (poppi) and Coca-Cola (Simply Pop, launched Feb 2024) now have modern sodas**
    - Modern soda category consolidating: Big CPG acquiring or launching own brands
    - OLIPOP remains independent but faces competition from both giants
    - Opportunity for niche modern brands, but market increasingly competitive
    """)

# ============================================================================
# TAB 2: WALMART & CROSS-PLATFORM ANALYSIS
# ============================================================================

with tab2:
    st.header("🔄 Walmart & Cross-Platform Comparison")
    
    # Methodology
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff9800 0%, #ff5722 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h3 style='margin-top: 0; color: white;'>📊 WALMART METHODOLOGY</h3>
        <ul style='margin-bottom: 0; line-height: 1.8;'>
            <li><strong>Revenue Proxy:</strong> Review Count × Price
                <ul>
                    <li><strong>Assumption:</strong> Review count proportional to lifetime sales</li>
                    <li><strong>NOT actual revenue</strong> - relative popularity indicator only</li>
                    <li><strong>Coverage:</strong> 84.6% of products</li>
                </ul>
            </li>
            <li><strong>Platform Context:</strong> Same-day grocery delivery (40% singles, 37% bulk packs)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    walmart_df = df[df['Platform'] == 'Walmart'].copy()
    
    # Filters
    st.sidebar.header("🎯 Walmart Filters")
    walmart_types = st.sidebar.multiselect(
        "Soda Type",
        options=['Traditional', 'Diet', 'Modern'],
        default=['Traditional', 'Diet', 'Modern'],
        key='walmart_types'
    )
    
    walmart_filtered = walmart_df[walmart_df['soda_type'].isin(walmart_types)]
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", len(walmart_filtered))
    
    with col2:
        total_proxy = walmart_filtered['revenue_proxy'].sum()
        st.metric("Revenue Proxy", f"${total_proxy/1e6:.1f}M",
                 help="Reviews × Price - NOT actual revenue")
    
    with col3:
        top_brand_proxy = walmart_filtered.groupby('brand_clean')['revenue_proxy'].sum().sort_values(ascending=False).iloc[0]
        top_brand = walmart_filtered.groupby('brand_clean')['revenue_proxy'].sum().sort_values(ascending=False).index[0]
        st.metric("Top Brand", top_brand, 
                 delta=f"${top_brand_proxy/1000:.0f}K proxy")
    
    st.markdown("---")
    
    # Distribution
    st.subheader("📊 Product Distribution & Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        type_count = walmart_filtered['soda_type'].value_counts().reset_index()
        type_count.columns = ['soda_type', 'count']
        
        fig = px.pie(
            type_count,
            values='count',
            names='soda_type',
            color='soda_type',
            color_discrete_map=SODA_TYPE_COLORS,
            hole=0.5,
            title="Product Count by Type"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
        fig.update_layout(showlegend=False, height=350, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        brand_proxy = walmart_filtered.groupby('brand_clean')['revenue_proxy'].sum().sort_values(ascending=False).head(10).reset_index()
        
        fig = px.bar(
            brand_proxy,
            x='revenue_proxy',
            y='brand_clean',
            orientation='h',
            color='brand_clean',
            color_discrete_map=BRAND_COLORS,
            title="Top 10 Brands by Revenue Proxy"
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            xaxis_title="Revenue Proxy ($)",
            yaxis_title="",
            height=350,
            margin=dict(t=40)
        )
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Revenue Proxy Leaders
    st.subheader("💰 Revenue Proxy Leaders")
    
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
    
    # Insights
    st.subheader("🔍 Key Insights")
    
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
                <li><strong>✅ Good for:</strong> Brand presence, relative ranking</li>
                <li><strong>✅ Good for:</strong> Historical popularity trends</li>
                <li><strong>❌ Not for:</strong> Current velocity estimates</li>
                <li><strong>❌ Not for:</strong> Absolute revenue comparison</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Private Label Analysis
    st.subheader("🏷️ Walmart Private Label vs Branded")
    
    # Calculate private label stats
    private_label_brands = ['Great Value', 'Sam\\\'s Choice', 'Member\\\'s Mark']
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
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h3 style='margin-top: 0; color: white;'>⚠️ COMPARISON FRAMEWORK</h3>
        <ul style='margin-bottom: 0; line-height: 1.8;'>
            <li>Amazon = Actual revenue data | Walmart = Popularity proxy</li>
            <li>Different delivery models drive different behaviors</li>
            <li>Price differences reflect platform positioning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Platform Comparison
    st.subheader("🔄 Platform Business Model Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📦 Amazon (1-2 Day Delivery)**
        - Stock-up, convenience buying
        - 56% singles (trial/variety)
        - 27% bulk packs (12+)
        - Higher prices ($23 avg Traditional)
        - Focus: Product discovery, variety
        """)
    
    with col2:
        st.markdown("""
        **🏪 Walmart (Same-Day Grocery)**
        - Grocery pantry stocking
        - 40% singles (immediate consumption)
        - 37% bulk packs (pantry staples)
        - Lower prices ($9 avg Traditional)
        - Focus: Essentials, value
        """)
    
    # Price Comparison
    st.subheader("💵 Price Positioning by Type")
    
    price_comparison = []
    for soda_type in ['Traditional', 'Diet', 'Modern']:
        amazon_price = df[(df['Platform'] == 'Amazon') & (df['soda_type'] == soda_type)]['price'].mean()
        walmart_price = df[(df['Platform'] == 'Walmart') & (df['soda_type'] == soda_type)]['price'].mean()
        
        price_comparison.append({
            'Type': soda_type,
            'Amazon': amazon_price,
            'Walmart': walmart_price,
            'Gap %': ((walmart_price - amazon_price) / amazon_price * 100)
        })
    
    price_df = pd.DataFrame(price_comparison)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Amazon', x=price_df['Type'], y=price_df['Amazon'], 
                        marker_color='#FF9900', text=price_df['Amazon'].apply(lambda x: f'${x:.2f}'),
                        textposition='outside'))
    fig.add_trace(go.Bar(name='Walmart', x=price_df['Type'], y=price_df['Walmart'], 
                        marker_color='#0071CE', text=price_df['Walmart'].apply(lambda x: f'${x:.2f}'),
                        textposition='outside'))
    
    fig.update_layout(barmode='group', height=400, 
                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title="Average Price ($)", showgrid=True, gridcolor='lightgray')
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategic Summary
    st.subheader("🎯 Strategic Takeaways")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%); padding: 25px; border-radius: 10px; color: white;'>
        <h4 style='margin-top: 0; color: white;'>💡 TOP 5 INSIGHTS</h4>
        <ol style='margin-bottom: 0; line-height: 2; font-size: 16px;'>
            <li><strong>PepsiCo's Bold Move:</strong> poppi acquisition doubles market share (8.8% → 17.8%) - strategic response to modern soda trend</li>
            <li><strong>OLIPOP Last Independent:</strong> Only major modern soda brand not owned by big CPG - potential acquisition target</li>
            <li><strong>Flavor Innovation Wins:</strong> Apple flavors have 53.6 velocity (highest) - poppi/OLIPOP's Apple Cider dominance</li>
            <li><strong>Pack Size Strategy:</strong> 12-packs have 44.8 velocity vs 38.2 for singles - promote bulk for higher turns!</li>
            <li><strong>Platform Specialization:</strong> Amazon = Discovery/Trial (56% singles) | Walmart = Value/Essentials (37% bulk)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: ONLINE VS OFFLINE REALITY
# ============================================================================

with tab3:
    st.header("🌐 Online vs Offline Reality")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h3 style='margin-top: 0; color: white;'>⚠️ CRITICAL CONTEXT: This Dashboard Shows Amazon ASINs, NOT Total Market</h3>
        <p style='margin: 0; font-size: 16px; line-height: 1.8;'>
            Modern sodas appear to be 25% of the market in this dashboard. <br>
            <strong>Reality: Modern sodas are ~3-4% of the $50-55B US CSD market ($1.8B, Circana 2024).</strong><br>
            <br>
            This dashboard reveals <strong>Amazon-specific consumer behavior</strong> - where modern brands over-index ~6-8x.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Market Size Comparison
    st.subheader("📊 Total Market vs Amazon Reality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Total US CSD Market (2024)**")
        st.markdown("""
        **Market Size:** $50-55 Billion (CSD only)
        - Mintel estimate: $55.2B
        - Circana: $46.1B (52-week data)
        - Industry consensus: $45-50B range
        
        **Category Breakdown (Parent Companies):**
        - Coca-Cola brands: ~45% (Coke, Sprite, Diet Coke, etc.)
        - PepsiCo brands: ~26% (Pepsi, Mountain Dew, etc.)
        - Keurig Dr Pepper: ~21% (Dr Pepper, 7UP, etc.)
        - **Modern sodas: ~3-4%** ($1.8B, Circana)
        - Others: ~4-5%
        
        **Distribution:**
        - Convenience stores, vending machines
        - Restaurants, fast food, stadiums
        - Grocery stores (impulse purchases)
        
        *Sources: Mintel, Circana, Beverage Digest*
        """)
    
    with col2:
        st.markdown("### **Amazon Soda (Tracked ASINs)**")
        st.markdown("""
        **Estimated Annual:** ~$100M
        - This dashboard: $8.3M monthly × 12
        - Represents tracked ASINs, not total Amazon soda
        
        **Category Breakdown (Our Data):**
        - Traditional: 44%
        - Diet: 31%
        - **Modern: 25%** ⚠️ **6-8x over-index!**
        
        **Calculation:**
        - Offline: 3-4% modern
        - Amazon: 25% modern
        - Over-index: 25% ÷ 3.5% = ~7x
        
        **Distribution:**
        - Search-driven discovery
        - Subscription auto-replenish
        - Review-based decision making
        """)
    
    st.success(r"""
    **Key Insight:** Modern sodas capture 25% of tracked Amazon ASINs but approximately 3-4% of total offline CSD market. 
    This represents a 6 to 8 times over-representation, revealing how DTC brands dominate online discovery channels while remaining niche offline.
    """)
    
    st.markdown("---")
    
    # Section 2: Why Modern Brands Over-Index on Amazon
    st.subheader("🎯 Why Modern Sodas Dominate Amazon (But Not Offline)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;'>
            <h4>Amazon Advantages for Modern Brands</h4>
            <ul>
                <li><strong>DTC Origins:</strong> poppi & OLIPOP started online, perfected Amazon playbook early</li>
                <li><strong>Discovery-Led:</strong> Shoppers actively search "healthy soda", "prebiotic", "gut health"</li>
                <li><strong>Subscription Model:</strong> Auto-replenish works for functional beverages (daily use)</li>
                <li><strong>Review Social Proof:</strong> Health claims + 4.5-star ratings = strong conversion</li>
                <li><strong>Target Demographic:</strong> Health-conscious, higher income, digitally native</li>
                <li><strong>Product Education:</strong> Amazon A+ Content explains prebiotics, ingredients</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #f44336;'>
            <h4>Offline Challenges for Modern Brands</h4>
            <ul>
                <li><strong>Limited Distribution:</strong> Not in most convenience stores, gas stations, vending machines</li>
                <li><strong>Price Point:</strong> $3-4 per can vs $1-2 for traditional (impulse barrier)</li>
                <li><strong>Brand Unfamiliarity:</strong> Shoppers don\'t know to look for poppi in store</li>
                <li><strong>Shelf Space:</strong> Traditional brands control prime real estate (eye-level, endcaps)</li>
                <li><strong>Foodservice Gap:</strong> Not in restaurants, movie theaters, stadiums</li>
                <li><strong>Education Needed:</strong> Prebiotic requires explanation - hard in retail</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("---")
    
    # Section 4: Strategic Implications
    st.subheader("💡 Strategic Implications & M&A Context")
    
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
            5️⃣ <strong>Competitive Response:</strong> Coca-Cola owns Health-Ade; PepsiCo needed modern play<br>
            <br>
            <strong>The Playbook:</strong> Win Online → Leverage CPG Distribution → Scale Offline
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Modern Soda Market Size:**
        - 2024: $1.8B (Circana)
        - 2023: ~$1.0B
        - **Growth: 83% YoY**
        
        **Key Players (Within Modern Category):**
        - poppi: 38% share (now PepsiCo)
        - OLIPOP: 33% share (independent)
        - Zevia: 12% share
        - Others: 17%
        
        *Source: Beverage Industry (Circana data)*
        """)
    
    with col2:
        st.markdown("""
        **What's Next:**
        - ✅ PepsiCo acquired poppi ($1.95B, 2025)
        - ✅ Coca-Cola launched Simply Pop (Feb 2024)
        - 🎯 OLIPOP = last major independent (33% share)
        - 📈 Category now has 2 CPG giants competing
        - 🚀 Expect innovation race between PepsiCo & Coke
        - 💡 Smaller brands (Zevia, Culture Pop) face pressure
        """)
    
    st.warning("""
    **Investment Thesis:** Big CPG companies are paying premium multiples (poppi: 4-5x revenue) 
    because they see modern sodas as the future. Total market may be only 3-4% today ($1.8B), but trajectory is clear: 
    younger consumers want functional, lower-sugar, gut-health beverages. 83% YoY growth proves category momentum. 
    Amazon data is a leading indicator of where offline is heading.
    """)
    
    st.markdown("---")
    
    # Section 5: Data Sources & Methodology
    st.subheader("📚 Data Sources & Methodology")
    
    st.markdown("""
    **This Dashboard:**
    - **Amazon:** 460 products, BSR-based velocity, actual "units sold" data
    - **Walmart:** 454 products, review-based popularity proxy
    - **Coverage:** 96.5% revenue estimation confidence
    - **Time Period:** Data collected Jan 2026
    
    **Market Data Sources:**
    - Grand View Research: Prebiotic soda market sizing
    - Euromonitor International: Digestive health soft drinks category
    - Statista: US carbonated soft drinks market
    - Circana: Channel performance data
    - Beverage Industry publications
    - Company press releases (poppi, OLIPOP, Coca-Cola, PepsiCo)
    
    **Limitations:**
    - Amazon data ≠ total market
    - Walmart proxy ≠ actual sales
    - No foodservice/vending machine data
    - Regional variations not captured
    - Single snapshot in time (not trend analysis)
    """)
    
    st.success("""
    **Bottom Line:** This dashboard excels at showing **online channel dynamics** and **modern brand performance** 
    in e-commerce. Modern sodas are 3-4% of the $50-55B offline CSD market but 25% of tracked Amazon ASINs (~6-8x over-index). 
    Use it to understand Amazon-specific behavior and emerging consumer trends, NOT to estimate total US soda market dynamics.
    
    *Data Sources: Mintel ($55.2B CSD), Circana ($1.8B modern sodas, 83% growth), Beverage Digest (brand shares)*
    """)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 14px;'>
Data: 914 products (460 Amazon, 454 Walmart) | Methodology: BSR-based velocity + Revenue proxy
</p>
""", unsafe_allow_html=True)
