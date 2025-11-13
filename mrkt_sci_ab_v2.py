# Python version check
import sys
if sys.version_info < (3, 10):
    raise RuntimeError("Python 3.10 or higher is required. Current version: {}.{}.{}".format(
        sys.version_info.major, sys.version_info.minor, sys.version_info.micro
    ))

import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import math
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Marketing Science: A/B Testing Playbook",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Color Palette
GOOGLE_BLUE = "#4285F4"
GOOGLE_RED = "#EA4335"
GOOGLE_YELLOW = "#FBBC04"
GOOGLE_GREEN = "#34A853"
GOOGLE_BLUE_DARK = "#1967D2"
GOOGLE_BLUE_LIGHT = "#8AB4F8"
GOOGLE_GREY = "#5F6368"
GOOGLE_GREY_LIGHT = "#9AA0A6"
GOOGLE_LIGHT_GREY = "#E8EAED"
GOOGLE_BG = "#F8F9FA"
GOOGLE_WHITE = "#FFFFFF"

# Enhanced CSS with modern design
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    * {{
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6, .main-header, .phase-header, .section-title {{
        font-family: 'Google Sans', 'Roboto', sans-serif !important;
    }}
    
    /* Ensure proper spacing from Streamlit toolbar */
    .stApp {{
        padding-top: 1rem;
    }}
    
    header[data-testid="stHeader"] {{
        background-color: transparent;
    }}
    
    .main {{
        background: linear-gradient(135deg, {GOOGLE_BG} 0%, #FFFFFF 100%);
        padding: 0.75rem !important;
    }}
    
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }}
    
    /* Hero Header */
    .hero-header {{
        background: linear-gradient(135deg, {GOOGLE_BLUE} 0%, {GOOGLE_BLUE_DARK} 100%);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 12px;
        margin: 0.5rem 0 1rem 0;
        box-shadow: 0 8px 24px rgba(66, 133, 244, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .hero-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
    }}
    
    .hero-title {{
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .hero-subtitle {{
        font-size: 1rem;
        margin-top: 0.25rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }}
    
    /* Enhanced Navigation */
    .nav-container {{
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        position: sticky;
        top: 0.5rem;
        z-index: 100;
    }}
    
    .progress-bar {{
        height: 4px;
        background: {GOOGLE_LIGHT_GREY};
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {GOOGLE_BLUE} 0%, {GOOGLE_GREEN} 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
    }}
    
    /* Phase Header */
    .phase-header {{
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, {GOOGLE_BLUE} 0%, {GOOGLE_BLUE_DARK} 100%);
        margin: 1rem 0 1rem 0;
        padding: 1.25rem 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(66, 133, 244, 0.3);
        position: relative;
        overflow: hidden;
        animation: slideInLeft 0.6s ease-out;
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .phase-header::after {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 40%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1));
    }}
    
    /* Modern Card Design */
    .section-container {{
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.75rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .section-container:hover {{
        box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }}
    
    .section-title {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {GOOGLE_BLUE};
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid {GOOGLE_LIGHT_GREY};
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .section-subtitle {{
        font-size: 1.1rem;
        font-weight: 500;
        color: {GOOGLE_GREY};
        margin: 1rem 0 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Enhanced Metric Card */
    .metric-card {{
        background: linear-gradient(135deg, white 0%, {GOOGLE_BG} 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid {GOOGLE_BLUE};
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 80px;
        height: 80px;
        background: radial-gradient(circle, rgba(66, 133, 244, 0.1) 0%, transparent 70%);
        transform: translate(30%, -30%);
    }}
    
    .metric-card:hover {{
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateX(4px);
        border-left-width: 6px;
    }}
    
    .metric-card h4 {{
        color: {GOOGLE_BLUE};
        font-size: 1.2rem;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }}
    
    /* Info Boxes with Icons */
    .info-box {{
        background: linear-gradient(135deg, rgba(66, 133, 244, 0.08) 0%, rgba(66, 133, 244, 0.03) 100%);
        border-left: 4px solid {GOOGLE_BLUE};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        box-shadow: 0 2px 6px rgba(66, 133, 244, 0.1);
        transition: all 0.3s ease;
    }}
    
    .info-box:hover {{
        box-shadow: 0 3px 10px rgba(66, 133, 244, 0.15);
        transform: translateX(2px);
    }}
    
    .success-box {{
        background: linear-gradient(135deg, rgba(52, 168, 83, 0.08) 0%, rgba(52, 168, 83, 0.03) 100%);
        border-left: 4px solid {GOOGLE_GREEN};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        box-shadow: 0 2px 6px rgba(52, 168, 83, 0.1);
        transition: all 0.3s ease;
    }}
    
    .success-box:hover {{
        box-shadow: 0 3px 10px rgba(52, 168, 83, 0.15);
        transform: translateX(2px);
    }}
    
    .warning-box {{
        background: linear-gradient(135deg, rgba(251, 188, 4, 0.08) 0%, rgba(251, 188, 4, 0.03) 100%);
        border-left: 4px solid {GOOGLE_YELLOW};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        box-shadow: 0 2px 6px rgba(251, 188, 4, 0.1);
        transition: all 0.3s ease;
    }}
    
    .warning-box:hover {{
        box-shadow: 0 3px 10px rgba(251, 188, 4, 0.15);
        transform: translateX(2px);
    }}
    
    .danger-box {{
        background: linear-gradient(135deg, rgba(234, 67, 53, 0.08) 0%, rgba(234, 67, 53, 0.03) 100%);
        border-left: 4px solid {GOOGLE_RED};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        box-shadow: 0 2px 6px rgba(234, 67, 53, 0.1);
        transition: all 0.3s ease;
    }}
    
    .danger-box:hover {{
        box-shadow: 0 3px 10px rgba(234, 67, 53, 0.15);
        transform: translateX(2px);
    }}
    
    /* Enhanced Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {GOOGLE_BLUE} 0%, {GOOGLE_BLUE_DARK} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .stButton>button:hover {{
        box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        transform: translateY(-2px);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* Navigation Buttons */
    button[key^="nav_btn_"] {{
        background: {GOOGLE_WHITE} !important;
        color: {GOOGLE_GREY} !important;
        border: 2px solid {GOOGLE_LIGHT_GREY} !important;
        border-radius: 10px !important;
        padding: 0.6rem 0.4rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        min-height: 60px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.15rem !important;
        line-height: 1.2 !important;
    }}
    
    button[key^="nav_btn_"]:hover {{
        background: #E8F0FE !important;
        color: {GOOGLE_BLUE} !important;
        border-color: {GOOGLE_BLUE_LIGHT} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.2) !important;
    }}
    
    /* Metric Badges */
    .metric-badge {{
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .badge-awareness {{ 
        background: linear-gradient(135deg, {GOOGLE_YELLOW} 0%, #F9AB00 100%); 
        color: #3C4043; 
    }}
    .badge-consideration {{ 
        background: linear-gradient(135deg, {GOOGLE_BLUE} 0%, {GOOGLE_BLUE_DARK} 100%); 
        color: white; 
    }}
    .badge-conversion {{ 
        background: linear-gradient(135deg, {GOOGLE_GREEN} 0%, #0F9D58 100%); 
        color: white; 
    }}
    .badge-retention {{ 
        background: linear-gradient(135deg, {GOOGLE_RED} 0%, #C5221F 100%); 
        color: white; 
    }}
    
    /* Enhanced Expander */
    .streamlit-expanderHeader {{
        background: {GOOGLE_BG};
        border-radius: 8px;
        font-weight: 500;
        color: {GOOGLE_GREY};
        padding: 0.75rem !important;
        transition: all 0.3s ease;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: #E8F0FE;
        color: {GOOGLE_BLUE};
    }}
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {{
        border-radius: 8px !important;
        border: 2px solid {GOOGLE_LIGHT_GREY} !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: {GOOGLE_BLUE} !important;
        box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1) !important;
    }}
    
    /* Metric Display */
    .stMetric {{
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }}
    
    .stMetric:hover {{
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: {GOOGLE_BG};
        border-radius: 12px;
        padding: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* Checkbox */
    .stCheckbox {{
        padding: 0.5rem;
        transition: all 0.3s ease;
    }}
    
    .stCheckbox:hover {{
        background: {GOOGLE_BG};
        border-radius: 6px;
    }}
    
    /* Dataframe */
    .dataframe {{
        border-radius: 8px !important;
        overflow: hidden !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {GOOGLE_BG};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {GOOGLE_GREY_LIGHT};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {GOOGLE_GREY};
    }}
    
    /* Responsive Typography */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 1.5rem;
        }}
        
        .section-title {{
            font-size: 1.2rem;
        }}
        
        button[key^="nav_btn_"] {{
            font-size: 0.8rem !important;
            padding: 0.5rem 0.25rem !important;
            min-height: 50px !important;
        }}
    }}
    
    /* Loading Animation */
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    .loading {{
        animation: shimmer 2s infinite;
        background: linear-gradient(to right, {GOOGLE_BG} 0%, {GOOGLE_LIGHT_GREY} 50%, {GOOGLE_BG} 100%);
        background-size: 1000px 100%;
    }}
</style>
""", unsafe_allow_html=True)

# Enhanced Marketing Metrics Dictionary (keeping your original data structure)
MARKETING_METRICS = {
    "Email Marketing": [
        {
            "name": "Open Rate",
            "description": "Percentage of recipients who opened the email",
            "formula": "Opens / Delivered Emails",
            "lifecycle": "Awareness",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "15-25%",
            "where_to_get_baseline": "ESP dashboard (Mailchimp, Klaviyo), Industry benchmarks (Mailchimp, Campaign Monitor reports)",
            "sample_size_consideration": "Low variance, medium sample needed",
            "industry_source": "Mailchimp Email Marketing Benchmarks 2024"
        },
        {
            "name": "Click-Through Rate (CTR)",
            "description": "Percentage of delivered emails that resulted in clicks",
            "formula": "Unique Clicks / Delivered Emails",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "2-5%",
            "where_to_get_baseline": "ESP analytics, Previous campaign data",
            "sample_size_consideration": "Lower rate = larger sample needed",
            "industry_source": "Campaign Monitor Email Marketing Benchmarks"
        },
        {
            "name": "Click-to-Open Rate (CTOR)",
            "description": "Percentage of email openers who clicked (measures content effectiveness)",
            "formula": "Unique Clicks / Unique Opens",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "10-20%",
            "where_to_get_baseline": "ESP dashboard, measures email content quality independent of subject line",
            "sample_size_consideration": "Conditional on opens, moderate sample",
            "industry_source": "Litmus State of Email Report"
        },
        {
            "name": "Conversion Rate",
            "description": "Percentage of recipients who completed desired action",
            "formula": "Conversions / Delivered Emails",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.5-3%",
            "where_to_get_baseline": "Google Analytics, CRM, Attribution platforms",
            "sample_size_consideration": "Low rate = very large sample needed",
            "industry_source": "eMarketer Email ROI Statistics"
        },
        {
            "name": "Unsubscribe Rate",
            "description": "Percentage of recipients who unsubscribed (guardrail metric)",
            "formula": "Unsubscribes / Delivered Emails",
            "lifecycle": "Retention",
            "distribution": "Binomial",
            "test": "Two-proportion z-test (guardrail)",
            "typical_range": "0.1-0.5%",
            "where_to_get_baseline": "ESP analytics, aim to stay below 0.5%",
            "sample_size_consideration": "Rare event, needs large sample",
            "industry_source": "CAN-SPAM compliance reports"
        },
        {
            "name": "Revenue per Email (RPE)",
            "description": "Average revenue generated per email sent",
            "formula": "Total Revenue / Delivered Emails",
            "lifecycle": "Conversion",
            "distribution": "Log-normal / Gamma",
            "test": "Mann-Whitney U or t-test with log transform",
            "typical_range": "$0.10-$2.00",
            "where_to_get_baseline": "E-commerce platform, Marketing attribution tools",
            "sample_size_consideration": "High variance due to outliers",
            "industry_source": "DMA Email ROI Report"
        }
    ],
    "Paid Search (PPC)": [
        {
            "name": "Click-Through Rate (CTR)",
            "description": "Percentage of ad impressions that resulted in clicks",
            "formula": "Clicks / Impressions",
            "lifecycle": "Awareness",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "2-5%",
            "where_to_get_baseline": "Google Ads, Microsoft Ads dashboards",
            "sample_size_consideration": "Depends on impression volume",
            "industry_source": "WordStream PPC Benchmarks"
        },
        {
            "name": "Conversion Rate",
            "description": "Percentage of clicks that converted",
            "formula": "Conversions / Clicks",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "2-10%",
            "where_to_get_baseline": "Ad platform conversion tracking, Google Analytics",
            "sample_size_consideration": "Critical metric, needs adequate power",
            "industry_source": "Google Ads Industry Benchmarks"
        },
        {
            "name": "Cost per Click (CPC)",
            "description": "Average cost paid for each click",
            "formula": "Total Spend / Total Clicks",
            "lifecycle": "Awareness",
            "distribution": "Normal or Gamma",
            "test": "Two-sample t-test",
            "typical_range": "$0.50-$5.00",
            "where_to_get_baseline": "Historical ad account data, Google Keyword Planner",
            "sample_size_consideration": "Moderate variance in most cases",
            "industry_source": "SEMrush CPC Trends Report"
        },
        {
            "name": "Cost per Acquisition (CPA)",
            "description": "Average cost to acquire one customer",
            "formula": "Total Spend / Conversions",
            "lifecycle": "Conversion",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "$10-$200",
            "where_to_get_baseline": "Ad platform reports, compare to Customer Lifetime Value",
            "sample_size_consideration": "High variance, sensitive to outliers",
            "industry_source": "Unbounce Conversion Benchmark Report"
        },
        {
            "name": "Return on Ad Spend (ROAS)",
            "description": "Revenue generated per dollar spent",
            "formula": "Revenue / Ad Spend",
            "lifecycle": "Conversion",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "2:1 to 10:1",
            "where_to_get_baseline": "Marketing attribution platforms, Target 4:1 as minimum",
            "sample_size_consideration": "Very high variance",
            "industry_source": "Nielsen Digital Ad Ratings"
        },
        {
            "name": "Quality Score",
            "description": "Platform's rating of ad quality (1-10 scale)",
            "formula": "Platform-calculated (Google/Bing)",
            "lifecycle": "Awareness",
            "distribution": "Discrete (1-10)",
            "test": "Mann-Whitney U test",
            "typical_range": "5-8",
            "where_to_get_baseline": "Google Ads interface, aim for 7+",
            "sample_size_consideration": "Ordinal data, use non-parametric",
            "industry_source": "Google Quality Score Guidelines"
        }
    ],
    "Display Advertising": [
        {
            "name": "Impressions",
            "description": "Number of times ad was displayed",
            "formula": "Count of ad displays",
            "lifecycle": "Awareness",
            "distribution": "Poisson (for counts)",
            "test": "Poisson rate test or t-test",
            "typical_range": "Varies widely",
            "where_to_get_baseline": "DV360, Google Display Network, programmatic platforms",
            "sample_size_consideration": "Usually have large volume",
            "industry_source": "IAB Display Advertising Guidelines"
        },
        {
            "name": "Click-Through Rate (CTR)",
            "description": "Percentage of impressions that resulted in clicks",
            "formula": "Clicks / Impressions",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.05-0.5%",
            "where_to_get_baseline": "Ad server data, historical campaigns",
            "sample_size_consideration": "Very low rate = huge sample needed",
            "industry_source": "Google Display Benchmarks Report"
        },
        {
            "name": "Viewability Rate",
            "description": "Percentage of impressions that were viewable (MRC standard)",
            "formula": "Viewable Impressions / Total Impressions",
            "lifecycle": "Awareness",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "50-70%",
            "where_to_get_baseline": "Ad verification tools (IAS, Moat, DoubleVerify)",
            "sample_size_consideration": "High rate = moderate sample",
            "industry_source": "MRC Viewability Standards"
        },
        {
            "name": "View-Through Conversion Rate",
            "description": "Conversions after viewing (not clicking) ad",
            "formula": "View-Through Conversions / Impressions",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.01-0.1%",
            "where_to_get_baseline": "Attribution platforms, campaign manager 360",
            "sample_size_consideration": "Extremely rare event",
            "industry_source": "Google Attribution Research"
        }
    ],
    "Social Media Advertising": [
        {
            "name": "Engagement Rate",
            "description": "Percentage of people who engaged with ad",
            "formula": "(Likes + Comments + Shares) / Impressions",
            "lifecycle": "Consideration",
            "distribution": "Binomial (simplified)",
            "test": "Two-proportion z-test",
            "typical_range": "1-5%",
            "where_to_get_baseline": "Platform insights (Meta, LinkedIn, TikTok ads managers)",
            "sample_size_consideration": "Platform-dependent variance",
            "industry_source": "Hootsuite Social Media Benchmarks"
        },
        {
            "name": "Click-Through Rate (CTR)",
            "description": "Percentage of impressions that resulted in clicks",
            "formula": "Clicks / Impressions",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.5-2%",
            "where_to_get_baseline": "Historical campaign data from ads manager",
            "sample_size_consideration": "Lower than search ads",
            "industry_source": "Wordstream Facebook Ads Benchmarks"
        },
        {
            "name": "Cost per Engagement (CPE)",
            "description": "Average cost per engagement action",
            "formula": "Total Spend / Total Engagements",
            "lifecycle": "Consideration",
            "distribution": "Gamma or Log-normal",
            "test": "Mann-Whitney U or t-test",
            "typical_range": "$0.05-$0.50",
            "where_to_get_baseline": "Platform historical data, industry CPE reports",
            "sample_size_consideration": "Moderate variance",
            "industry_source": "Socialbakers Advertising Benchmarks"
        },
        {
            "name": "Video Completion Rate (VCR)",
            "description": "Percentage who watched video to completion",
            "formula": "Completed Views / Total Views",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "15-40%",
            "where_to_get_baseline": "Video ad reports from platform, varies by length",
            "sample_size_consideration": "Length-dependent",
            "industry_source": "Wistia Video Marketing Statistics"
        },
        {
            "name": "Share Rate",
            "description": "Percentage of viewers who shared content",
            "formula": "Shares / Impressions",
            "lifecycle": "Awareness",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.1-1%",
            "where_to_get_baseline": "Historical organic + paid content performance",
            "sample_size_consideration": "Rare event, viral potential",
            "industry_source": "BuzzSumo Content Research"
        }
    ],
    "Video Advertising": [
        {
            "name": "Video Start Rate",
            "description": "Percentage of video impressions that started playing",
            "formula": "Video Starts / Impressions",
            "lifecycle": "Awareness",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "60-85%",
            "where_to_get_baseline": "Video ad platforms (YouTube, Meta, TikTok), IAB video standards",
            "sample_size_consideration": "Common event, moderate sample",
            "industry_source": "IAB Video Ad Standards"
        },
        {
            "name": "View-Through Rate (VTR)",
            "description": "Percentage of video starts watched to completion",
            "formula": "Completed Views / Video Starts",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "15-40%",
            "where_to_get_baseline": "Historical video campaign data, strongly depends on video length",
            "sample_size_consideration": "Varies significantly by video duration",
            "industry_source": "Wistia Video Benchmarks Report"
        },
        {
            "name": "Cost per View (CPV)",
            "description": "Average cost per completed video view",
            "formula": "Total Spend / Completed Views",
            "lifecycle": "Awareness",
            "distribution": "Gamma or Log-normal",
            "test": "Mann-Whitney U or t-test",
            "typical_range": "$0.10-$0.30",
            "where_to_get_baseline": "YouTube TrueView, Meta video ads historical data",
            "sample_size_consideration": "Moderate variance by placement",
            "industry_source": "YouTube Advertising Benchmarks"
        },
        {
            "name": "Video Engagement Rate",
            "description": "Interactions relative to views (likes, shares, comments)",
            "formula": "(Likes + Comments + Shares) / Video Views",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "2-8%",
            "where_to_get_baseline": "Platform analytics, varies by content quality and platform",
            "sample_size_consideration": "Higher on short-form platforms (TikTok, Reels)",
            "industry_source": "Tubular Labs Video Intelligence"
        },
        {
            "name": "Watch Time",
            "description": "Average seconds watched per view",
            "formula": "Total Watch Time / Total Views",
            "lifecycle": "Consideration",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "Varies by video length",
            "where_to_get_baseline": "YouTube Analytics, platform dashboards",
            "sample_size_consideration": "Right-skewed, some watch full video, most drop off early",
            "industry_source": "Wistia Engagement Graphs"
        },
        {
            "name": "Video Click-Through Rate",
            "description": "Percentage of views that resulted in clicks to destination",
            "formula": "Clicks / Video Views",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "0.5-2%",
            "where_to_get_baseline": "Video ad platform reports",
            "sample_size_consideration": "Lower than display CTR",
            "industry_source": "Google Video Ads Best Practices"
        }
    ],
    "Website / Landing Page": [
        {
            "name": "Bounce Rate",
            "description": "Percentage of visitors who left without interaction",
            "formula": "Single-Page Sessions / Total Sessions",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test (inverse interpretation)",
            "typical_range": "40-60%",
            "where_to_get_baseline": "Google Analytics, Adobe Analytics",
            "sample_size_consideration": "Common event, moderate sample",
            "industry_source": "Google Analytics Benchmarks"
        },
        {
            "name": "Conversion Rate",
            "description": "Percentage of visitors who completed goal",
            "formula": "Conversions / Visitors",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "1-5%",
            "where_to_get_baseline": "Historical website data, industry CRO reports",
            "sample_size_consideration": "Primary metric, needs good power",
            "industry_source": "Unbounce Landing Page Benchmark Report"
        },
        {
            "name": "Average Session Duration",
            "description": "Mean time visitors spend on site",
            "formula": "Total Session Duration / Sessions",
            "lifecycle": "Consideration",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "2-5 minutes",
            "where_to_get_baseline": "Google Analytics Behavior reports",
            "sample_size_consideration": "High variance, outliers common",
            "industry_source": "Contentsquare Digital Experience Benchmarks"
        },
        {
            "name": "Pages per Session",
            "description": "Average number of pages viewed per session",
            "formula": "Total Pageviews / Sessions",
            "lifecycle": "Consideration",
            "distribution": "Poisson or Negative Binomial",
            "test": "Mann-Whitney U or t-test",
            "typical_range": "2-4 pages",
            "where_to_get_baseline": "Google Analytics Audience reports",
            "sample_size_consideration": "Overdispersed count data",
            "industry_source": "GA4 Benchmarks by Industry"
        },
        {
            "name": "Form Completion Rate",
            "description": "Percentage who completed the form after starting",
            "formula": "Form Submissions / Form Starts",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "20-50%",
            "where_to_get_baseline": "Form analytics tools (Formstack, Typeform), heatmap analysis",
            "sample_size_consideration": "Depends on form complexity",
            "industry_source": "Formstack Form Conversion Report"
        }
    ],
    "E-commerce": [
        {
            "name": "Add-to-Cart Rate",
            "description": "Percentage of visitors who added items to cart",
            "formula": "Add-to-Carts / Visitors",
            "lifecycle": "Consideration",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "5-15%",
            "where_to_get_baseline": "E-commerce platform analytics (Shopify, GA4 Enhanced E-commerce)",
            "sample_size_consideration": "Moderate rate",
            "industry_source": "Shopify Commerce Trends Report"
        },
        {
            "name": "Cart Abandonment Rate",
            "description": "Percentage of carts not completed (guardrail metric)",
            "formula": "Abandoned Carts / Total Carts",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test (guardrail)",
            "typical_range": "60-80%",
            "where_to_get_baseline": "Historical e-commerce data, Baymard Institute research",
            "sample_size_consideration": "Common event",
            "industry_source": "Baymard Institute Cart Abandonment Research"
        },
        {
            "name": "Purchase Conversion Rate",
            "description": "Percentage of visitors who made a purchase",
            "formula": "Purchases / Visitors",
            "lifecycle": "Conversion",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "1-3%",
            "where_to_get_baseline": "Platform reports, compare to industry vertical",
            "sample_size_consideration": "Critical metric",
            "industry_source": "Adobe Digital Economy Index"
        },
        {
            "name": "Average Order Value (AOV)",
            "description": "Average revenue per order",
            "formula": "Total Revenue / Number of Orders",
            "lifecycle": "Conversion",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "$50-$200",
            "where_to_get_baseline": "Historical order data, segment by customer type",
            "sample_size_consideration": "High variance, outliers",
            "industry_source": "Shopify Benchmarks Report"
        },
        {
            "name": "Revenue per Visitor (RPV)",
            "description": "Average revenue generated per visitor",
            "formula": "Total Revenue / Total Visitors",
            "lifecycle": "Conversion",
            "distribution": "Zero-inflated (most are $0)",
            "test": "Mann-Whitney U test",
            "typical_range": "$0.50-$5.00",
            "where_to_get_baseline": "E-commerce analytics platforms",
            "sample_size_consideration": "Extreme outliers, zero-heavy",
            "industry_source": "Google Merchandise Store Benchmarks"
        },
        {
            "name": "Items per Order",
            "description": "Average number of items purchased per order",
            "formula": "Total Items / Number of Orders",
            "lifecycle": "Conversion",
            "distribution": "Poisson or Negative Binomial",
            "test": "Mann-Whitney U or t-test",
            "typical_range": "1.5-3.5",
            "where_to_get_baseline": "Order history data from e-commerce platform",
            "sample_size_consideration": "Overdispersed count",
            "industry_source": "BigCommerce E-commerce Analytics Guide"
        }
    ],
    "Customer Retention": [
        {
            "name": "Repeat Purchase Rate",
            "description": "Percentage of customers who make repeat purchase",
            "formula": "Repeat Customers / Total Customers",
            "lifecycle": "Retention",
            "distribution": "Binomial",
            "test": "Two-proportion z-test",
            "typical_range": "20-40%",
            "where_to_get_baseline": "CRM data, cohort analysis",
            "sample_size_consideration": "Needs long observation period",
            "industry_source": "Smile.io Retention Benchmarks"
        },
        {
            "name": "Churn Rate",
            "description": "Percentage of customers who stopped buying",
            "formula": "Churned Customers / Total Customers",
            "lifecycle": "Retention",
            "distribution": "Binomial",
            "test": "Two-proportion z-test or survival analysis",
            "typical_range": "5-10% monthly",
            "where_to_get_baseline": "Subscription management platforms, cohort retention analysis",
            "sample_size_consideration": "Time-dependent metric",
            "industry_source": "ProfitWell Retention Report"
        },
        {
            "name": "Customer Lifetime Value (CLV)",
            "description": "Total revenue expected from customer relationship",
            "formula": "Avg Purchase Value × Purchase Frequency × Avg Lifespan",
            "lifecycle": "Retention",
            "distribution": "Log-normal",
            "test": "Mann-Whitney U or log-transformed t-test",
            "typical_range": "$100-$1000",
            "where_to_get_baseline": "Historical cohort analysis, predictive models",
            "sample_size_consideration": "Very high variance, long timeframe",
            "industry_source": "Harvard Business Review CLV Calculator"
        },
        {
            "name": "Net Promoter Score (NPS)",
            "description": "Likelihood to recommend (0-10 scale)",
            "formula": "% Promoters (9-10) - % Detractors (0-6)",
            "lifecycle": "Retention",
            "distribution": "Ordinal/Discrete",
            "test": "Mann-Whitney U or proportions test",
            "typical_range": "-10 to +50",
            "where_to_get_baseline": "Survey platforms (Qualtrics, SurveyMonkey), compare to industry NPS",
            "sample_size_consideration": "Survey-based, response bias",
            "industry_source": "Bain & Company NPS Benchmarks"
        }
    ]
}

# Distribution explanations with practical applications (keeping your original)
DISTRIBUTIONS = {
    "Binomial": {
        "description": "Models success/failure outcomes (yes/no, clicked/didn't click)",
        "when_to_use": "Conversion rates, click-through rates, any binary outcome",
        "parameters": "n (trials), p (probability of success)",
        "example": "Out of 1000 emails, 250 were opened → p = 0.25",
        "variance_note": "Variance = n×p×(1-p). Lower for extreme probabilities (near 0 or 1)",
        "practical_application": "Use historical conversion rate distribution as Bayesian prior for campaign planning. If past CVR is 3% (Beta(300, 9700)), update with new data to forecast future performance.",
        "mmm_use": "Binary response models in MMM - did ad exposure lead to conversion? Logistic regression backbone."
    },
    "Normal": {
        "description": "Bell-curved distribution for continuous data",
        "when_to_use": "Large sample sizes, metrics influenced by many factors",
        "parameters": "μ (mean), σ (standard deviation)",
        "example": "Session duration when you have thousands of users",
        "variance_note": "Applies via Central Limit Theorem when n is large",
        "practical_application": "Model aggregated effects in MMM. Channel contributions often normally distributed around mean effect.",
        "mmm_use": "Standard assumption for error terms in linear MMM. Transform skewed data (log) to achieve normality for regression."
    },
    "Log-normal": {
        "description": "Right-skewed distribution (many small values, few large ones)",
        "when_to_use": "Revenue, time duration, anything that can't be negative with long tail",
        "parameters": "μ (log-scale mean), σ (log-scale std dev)",
        "example": "Order values: most are $20-50, but some are $500+",
        "variance_note": "High variance due to outliers. Log-transform before t-test or use non-parametric",
        "practical_application": "Model customer lifetime value distribution. Most customers worth $X, few 'whales' worth 10X. Use for revenue forecasting with realistic tail risk.",
        "mmm_use": "Revenue response curves in MMM. Diminishing returns (concave) or S-curves often emerge from log-normal channel effects."
    },
    "Poisson": {
        "description": "Models count data (events occurring in fixed interval)",
        "when_to_use": "Number of purchases per user, page views per session",
        "parameters": "λ (average rate)",
        "example": "Average of 3 page views per session",
        "variance_note": "Variance = mean. If variance >> mean, use Negative Binomial",
        "practical_application": "Model arrival rates for conversion events. If customers convert at rate λ per week, predict volume for capacity planning.",
        "mmm_use": "Count-based dependent variables in MMM (number of orders, store visits). Poisson regression for count outcomes."
    },
    "Negative Binomial": {
        "description": "Overdispersed count data (variance > mean)",
        "when_to_use": "Page views, items per order when there's high variability",
        "parameters": "r (successes), p (probability)",
        "example": "Most users view 2 pages, but some view 20+",
        "variance_note": "Handles overdispersion better than Poisson",
        "practical_application": "Model conversion counts with high variance. Accounts for unobserved heterogeneity in customer behavior.",
        "mmm_use": "Alternative to Poisson in MMM when conversion counts show overdispersion. Common in e-commerce with repeat purchase."
    },
    "Gamma": {
        "description": "Continuous positive values with right skew",
        "when_to_use": "Costs, time to conversion, positive continuous metrics",
        "parameters": "shape (k), scale (θ)",
        "example": "Cost per click ranging from $0.50 to $10",
        "variance_note": "More flexible than log-normal for certain skewed data",
        "practical_application": "Model time-to-conversion, customer acquisition cost distributions. Shape parameter captures variation in conversion speed.",
        "mmm_use": "Gamma GLM for positive continuous outcomes in MMM (revenue, cost). Allows asymmetric response to marketing spend."
    },
    "Beta": {
        "description": "Distribution for probabilities and proportions (bounded 0-1)",
        "when_to_use": "Prior distributions for conversion rates, click rates",
        "parameters": "α (successes), β (failures)",
        "example": "Historical CVR of 3% with 300 conversions, 9700 non-conversions → Beta(300, 9700)",
        "variance_note": "Variance decreases as α + β increases (more data = more certainty)",
        "practical_application": "Bayesian A/B testing. Start with Beta prior from historical data, update with test data to get posterior distribution. Quantify probability one variant is better.",
        "mmm_use": "Priors for conversion probability parameters in Bayesian MMM. Especially useful with limited data or hierarchical models."
    }
}

# Statistical tests explained (keeping your original)
STATISTICAL_TESTS = {
    "Two-proportion z-test": {
        "use_case": "Comparing conversion rates, CTR, or any binary metric between two groups",
        "assumptions": ["Independent samples", "n×p ≥ 5 and n×(1-p) ≥ 5 for both groups"],
        "formula": "z = (p₁ - p₂) / √(p̄(1-p̄)(1/n₁ + 1/n₂))",
        "null_hypothesis": "H₀: p₁ = p₂",
        "example": "Control CVR = 5%, Treatment CVR = 5.5%",
        "practical_note": "Most common marketing test. If sample size requirements not met, use Fisher's exact test."
    },
    "Two-sample t-test": {
        "use_case": "Comparing means of continuous metrics (revenue, time, costs)",
        "assumptions": ["Independent samples", "Approximately normal distribution (or large n)", "Equal variances (or use Welch's t-test)"],
        "formula": "t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)",
        "null_hypothesis": "H₀: μ₁ = μ₂",
        "example": "Average session duration: Control = 3.2 min, Treatment = 3.5 min",
        "practical_note": "Check normality with QQ-plot. If skewed, use Mann-Whitney or log-transform first."
    },
    "Mann-Whitney U test": {
        "use_case": "Non-parametric alternative when data is skewed or assumptions violated",
        "assumptions": ["Independent samples", "Ordinal or continuous data"],
        "formula": "Based on rank sums",
        "null_hypothesis": "H₀: Distributions are equal",
        "example": "Revenue per user (highly skewed with outliers)",
        "practical_note": "Default choice for revenue, AOV, and any metric with extreme outliers. More robust than t-test."
    },
    "Log-transformed t-test": {
        "use_case": "When data is log-normally distributed (revenue, AOV)",
        "assumptions": ["Data must be positive", "Log-transformed data is approximately normal"],
        "formula": "Take log of all values, then apply t-test",
        "null_hypothesis": "H₀: Geometric means are equal",
        "example": "Order values: log(AOV) then compare",
        "practical_note": "Tests geometric mean difference. Interpret as % change rather than absolute. Add $1 if zeros present."
    },
    "Chi-square test": {
        "use_case": "Comparing categorical distributions or contingency tables",
        "assumptions": ["Independent observations", "Expected frequency ≥ 5 in each cell"],
        "formula": "χ² = Σ(Observed - Expected)² / Expected",
        "null_hypothesis": "H₀: Variables are independent",
        "example": "Comparing device type distribution (mobile/desktop/tablet) between groups",
        "practical_note": "Use for randomization checks (A/A test) and detecting sample ratio mismatch."
    }
}

# Initialize session state
if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = {}

def render_hero():
    """Render enhanced hero header"""
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-title">🔬 Marketing Science: A/B Testing Playbook</div>
        <div class="hero-subtitle">
            Design, execute, and analyze marketing experiments with statistical rigor
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar(current_step, total_steps=6):
    """Render progress bar"""
    progress = ((current_step + 1) / total_steps) * 100
    st.markdown(f"""
    <div class="nav-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render enhanced navigation"""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0
    
    workflow_steps = [
        ("🎯", "Objective", "Define your goal"),
        ("📊", "Metrics", "Choose KPIs"),
        ("🔬", "Design", "Sample size"),
        ("🚀", "Launch", "Implementation"),
        ("📈", "Analyze", "Results"),
        ("✅", "Decide", "Take action")
    ]
    
    active_idx = st.session_state.current_tab
    
    # Progress bar
    render_progress_bar(active_idx)
    
    # Navigation buttons
    nav_cols = st.columns(len(workflow_steps))
    
    for idx, (col, (icon, step, desc)) in enumerate(zip(nav_cols, workflow_steps)):
        with col:
            button_label = f"{icon}\n{step}"
            if st.button(button_label, key=f"nav_btn_{idx}", use_container_width=True, help=desc):
                st.session_state.current_tab = idx
                st.rerun()
    
    # Active state styling
    st.markdown(f"""
    <style>
    button[key="nav_btn_{active_idx}"] {{
        background: linear-gradient(135deg, {GOOGLE_BLUE} 0%, {GOOGLE_BLUE_DARK} 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: 2px solid {GOOGLE_BLUE_DARK} !important;
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def main():
    render_hero()
    render_navigation()
    
    # Sidebar summary
    if st.session_state.experiment_data.get('sample_size_per_group'):
        with st.sidebar:
            st.markdown("### 🎯 Experiment Snapshot")
            st.metric("Sample/Group", f"{st.session_state.experiment_data['sample_size_per_group']:,}")
            st.metric("Duration", f"{st.session_state.experiment_data.get('duration_days', 0)} days")
            st.metric("Channel", st.session_state.experiment_data.get('channel', 'N/A'))
    
    # Display content based on current tab
    if st.session_state.current_tab == 0:
        tab_business_objective()
    elif st.session_state.current_tab == 1:
        tab_define_metrics()
    elif st.session_state.current_tab == 2:
        tab_design_experiment()
    elif st.session_state.current_tab == 3:
        tab_implementation()
    elif st.session_state.current_tab == 4:
        tab_analysis()
    elif st.session_state.current_tab == 5:
        tab_decision()

def tab_business_objective():
    st.markdown('<p class="phase-header">🎯 Phase 1: Business Objective</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Before designing your experiment, establish proper context, hypothesis, and metric definitions. 
    This foundational phase prevents costly mistakes and ensures alignment across teams.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Business Objective with enhanced visual
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">1️⃣ What is the Business Objective?</div>
    <p style="color: {GOOGLE_GREY_LIGHT}; margin-bottom: 1rem; font-size: 0.9rem;">
    Select which phase of the customer lifecycle you want to optimize
    </p>
    """, unsafe_allow_html=True)
    
    # Create enhanced S-Curve chart
    lifecycle_phases = ["Awareness", "Acquisition", "Activation", "Engagement", "Resurrection", "Retention"]
    phase_colors = [GOOGLE_BLUE, GOOGLE_BLUE_DARK, GOOGLE_GREEN, GOOGLE_YELLOW, GOOGLE_RED, GOOGLE_GREEN]
    
    x_curve = np.linspace(0, 10, 200)
    y_curve = 1 / (1 + np.exp(-(x_curve - 5)))
    
    phase_positions = np.linspace(1, 9, len(lifecycle_phases))
    phase_y_positions = 1 / (1 + np.exp(-(phase_positions - 5)))
    
    fig = go.Figure()
    
    # Enhanced S-curve
    fig.add_trace(go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        line=dict(color=GOOGLE_BLUE, width=5),
        name='Customer Lifecycle',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Phase markers with descriptions
    phase_descriptions = {
        "Awareness": "User becomes aware of your product",
        "Acquisition": "User signs up or makes first purchase",
        "Activation": "User experiences core value proposition",
        "Engagement": "User actively uses the product regularly",
        "Resurrection": "Re-engaging dormant users",
        "Retention": "User continues to use product over time"
    }
    
    for i, (phase, color, x_pos, y_pos) in enumerate(zip(lifecycle_phases, phase_colors, phase_positions, phase_y_positions)):
        description = phase_descriptions.get(phase, "")
        
        # Add animated markers
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[y_pos],
            mode='markers',
            marker=dict(
                size=40,
                color=color,
                line=dict(width=4, color='white'),
                symbol='circle',
                opacity=0.95
            ),
            name=phase,
            customdata=[phase],
            showlegend=False,
            hovertemplate=f"<b>{phase}</b><br>{description}<extra></extra>",
        ))
        
        # Add labels
        label_y = y_pos + 0.15 if y_pos < 0.5 else y_pos - 0.15
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[label_y],
            mode='text',
            text=[phase],
            textfont=dict(size=12, color=color, family='Google Sans, Arial Black'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title=dict(
            text="<b>Customer Lifecycle Journey</b>",
            font=dict(size=18, color=GOOGLE_GREY, family='Google Sans'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-0.5, 10.5]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-0.2, 1.3]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=20),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Campaign Ideas (keeping your original structure but with enhanced styling)
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">2️⃣ Campaign Ideas by Business Objective</div>
    <p style="color: {GOOGLE_GREY_LIGHT}; margin-bottom: 1rem; font-size: 0.9rem;">
    Explore recommended campaigns across all marketing channels for your chosen objective
    </p>
    """, unsafe_allow_html=True)
    
    # Complete lifecycle hypotheses with all campaigns
    lifecycle_hypotheses = {
        "Awareness": {
            "color": GOOGLE_BLUE,
            "campaigns": [
                {
                    "name": "Branded Search Campaigns",
                    "channel": "🔍 Paid Search",
                    "hypothesis": "If we run branded search campaigns, then brand recall will increase by 40%, because repeated exposure increases familiarity",
                    "design": "Geo-holdout test with matched DMAs. Track brand recall via surveys",
                    "metrics": "Brand Recall, Search Volume, Website Traffic",
                    "duration": "4 weeks"
                },
                {
                    "name": "YouTube Pre-Roll Awareness Campaign",
                    "channel": "📹 Video",
                    "hypothesis": "If we run 15-second pre-roll ads on YouTube, then brand awareness will increase by 50%, because video creates emotional connection",
                    "design": "Brand lift study with exposed/control groups. Track completion rate and recall",
                    "metrics": "Brand Awareness Lift, Ad Recall, Completion Rate",
                    "duration": "3-4 weeks"
                },
                {
                    "name": "Podcast Sponsorships",
                    "channel": "🎙️ Podcast",
                    "hypothesis": "If we sponsor high-traffic industry podcasts, then new user traffic will increase by 50%, because podcast listeners trust host recommendations",
                    "design": "Use unique promo codes per episode. Sequential rollout with synthetic control",
                    "metrics": "New User Traffic, Promo Code Redemption, Brand Searches",
                    "duration": "8 weeks"
                },
                {
                    "name": "Social Media Brand Campaign",
                    "channel": "📱 Social Media",
                    "hypothesis": "If we run brand awareness campaigns on Instagram/Facebook, then reach will increase by 60%, because social media offers precise targeting",
                    "design": "Campaign with brand lift study. Test different creative formats (video vs carousel)",
                    "metrics": "Reach, Brand Awareness Lift, Engagement Rate",
                    "duration": "4 weeks"
                },
                {
                    "name": "Display Network Brand Campaign",
                    "channel": "🖼️ Display",
                    "hypothesis": "If we run display campaigns on premium publishers, then brand consideration will increase by 35%, because contextual relevance builds trust",
                    "design": "Frequency-capped campaign with brand lift measurement. A/B test static vs animated",
                    "metrics": "Brand Lift, Viewability, Frequency, Consideration",
                    "duration": "3 weeks"
                },
                {
                    "name": "CTV/OTT Awareness Campaign",
                    "channel": "📺 CTV/OTT",
                    "hypothesis": "If we run CTV ads during primetime, then unaided awareness will increase by 45%, because TV environment commands attention",
                    "design": "Geo-split test with brand tracking surveys. Test 15s vs 30s creative",
                    "metrics": "Unaided Awareness, Ad Recall, Reach, Frequency",
                    "duration": "8 weeks"
                },
                {
                    "name": "Influencer Brand Partnerships",
                    "channel": "👥 Influencer",
                    "hypothesis": "If we partner with macro-influencers for brand campaigns, then reach will increase by 40%, because influencers amplify message",
                    "design": "Track reach, engagement, and brand mention volume. Use unique tracking links",
                    "metrics": "Reach, Engagement Rate, Brand Mentions, Traffic",
                    "duration": "6-8 weeks"
                }
            ]
        },
        "Acquisition": {
            "color": GOOGLE_BLUE_DARK,
            "campaigns": [
                {
                    "name": "Search Conversion Campaigns",
                    "channel": "🔍 Paid Search",
                    "hypothesis": "If we optimize landing pages to match ad copy, then conversion rate will increase by 35%, because message consistency reduces friction",
                    "design": "A/B test matched vs generic landing pages. Track conversion rate, bounce rate, time on page",
                    "metrics": "Conversion Rate, CPA, Quality Score, Bounce Rate",
                    "duration": "3-4 weeks"
                },
                {
                    "name": "Email Sign-up Campaigns",
                    "channel": "📧 Email",
                    "hypothesis": "If we offer lead magnet (free guide) vs direct sign-up, then conversion will increase by 45%, because value exchange reduces hesitation",
                    "design": "A/B test two landing page variants. Track sign-up rate, email quality score",
                    "metrics": "Sign-up Rate, Email Open Rate, Lead Quality",
                    "duration": "2 weeks"
                },
                {
                    "name": "Social Media Lead Gen",
                    "channel": "📱 Social Media",
                    "hypothesis": "If we use lead forms on Facebook/Instagram vs landing page, then cost per lead will decrease by 30%, because in-platform forms reduce friction",
                    "design": "Campaign split test. Half traffic to lead forms, half to landing page",
                    "metrics": "Cost per Lead, Lead Quality, Conversion Rate",
                    "duration": "4 weeks"
                },
                {
                    "name": "Display Retargeting",
                    "channel": "🖼️ Display",
                    "hypothesis": "If we retarget site visitors within 7 days with offer, then conversion rate will be 40% higher, because recent visitors have stronger intent",
                    "design": "Test different retargeting windows (1-7 days vs 8-30 days) with matched creative",
                    "metrics": "Conversion Rate, ROAS, Frequency",
                    "duration": "4 weeks"
                },
                {
                    "name": "YouTube Direct Response",
                    "channel": "📹 Video",
                    "hypothesis": "If we run TrueView for Action ads, then cost per acquisition will be competitive with search, because video builds trust before click",
                    "design": "Compare CPA from YouTube vs Search campaigns with same budget allocation",
                    "metrics": "CPA, Conversion Rate, View Rate, CTR",
                    "duration": "6 weeks"
                },
                {
                    "name": "Influencer Affiliate Program",
                    "channel": "👥 Influencer",
                    "hypothesis": "If we offer affiliate commissions to micro-influencers, then customer acquisition cost will be 50% lower, because authentic recommendations convert better",
                    "design": "Track conversions via unique affiliate links. Compare CAC vs paid channels",
                    "metrics": "CAC, Conversion Rate, Customer LTV",
                    "duration": "8-12 weeks"
                }
            ]
        },
        "Activation": {
            "color": GOOGLE_GREEN,
            "campaigns": [
                {
                    "name": "Onboarding Email Series",
                    "channel": "📧 Email",
                    "hypothesis": "If we send personalized onboarding emails, then activation rate will increase by 32%, because relevant content matches user context",
                    "design": "Multi-variant test across signup sources. Personalized vs generic emails",
                    "metrics": "7-day Activation Rate, Email Open Rate, Feature Adoption",
                    "duration": "3 weeks"
                },
                {
                    "name": "In-App Tutorial Campaign",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we implement interactive product tour, then time-to-first-value will decrease by 40%, because guided onboarding reduces learning curve",
                    "design": "RCT on new users. Interactive tour vs standard documentation",
                    "metrics": "Time to First Value, Day 1 Retention, Feature Completion",
                    "duration": "4 weeks"
                },
                {
                    "name": "Social Proof in Onboarding",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we show user success stories during onboarding, then completion rate will increase by 25%, because social proof increases confidence",
                    "design": "A/B test with/without success stories in onboarding flow",
                    "metrics": "Onboarding Completion Rate, Time to Activate, Drop-off Points",
                    "duration": "2-3 weeks"
                },
                {
                    "name": "Push Notification Activation Series",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we send 3 strategic push notifications in first 48 hours, then Day 7 activation will increase by 28%, because timely prompts drive action",
                    "design": "Test notification cadence and timing. Track opt-in rate and activation",
                    "metrics": "Day 7 Activation, Notification CTR, App Opens",
                    "duration": "3 weeks"
                }
            ]
        },
        "Engagement": {
            "color": GOOGLE_YELLOW,
            "campaigns": [
                {
                    "name": "Personalized Content Email",
                    "channel": "📧 Email",
                    "hypothesis": "If we send weekly personalized content emails, then weekly active users will increase by 30%, because relevant content drives return visits",
                    "design": "A/B test personalized vs generic content. Track open, click, and return rate",
                    "metrics": "WAU, Email CTR, Return Visit Rate",
                    "duration": "6 weeks"
                },
                {
                    "name": "Social Engagement Campaign",
                    "channel": "📱 Social Media",
                    "hypothesis": "If we feature user content and run engagement contests, then community participation will increase by 45%, because recognition motivates contribution",
                    "design": "Weekly UGC features + monthly contests. Track participation and sentiment",
                    "metrics": "UGC Submissions, Engagement Rate, Community Growth",
                    "duration": "8 weeks"
                },
                {
                    "name": "In-App Gamification",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we add streak rewards and progress tracking, then DAU will increase by 38%, because gamification creates habit loops",
                    "design": "Cohort RCT. Streaks vs no streaks. Track DAU, streak length, burnout",
                    "metrics": "DAU, WAU, Session Length, Feature Usage",
                    "duration": "60 days"
                },
                {
                    "name": "Push Notification Re-engagement",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we send personalized activity notifications, then inactive user reactivation will increase by 35%, because timely reminders prompt return",
                    "design": "Test notification triggers and personalization. Track reactivation rate",
                    "metrics": "Reactivation Rate, Notification CTR, 7-day Retention",
                    "duration": "4 weeks"
                }
            ]
        },
        "Resurrection": {
            "color": GOOGLE_RED,
            "campaigns": [
                {
                    "name": "Win-Back Email Campaign",
                    "channel": "📧 Email",
                    "hypothesis": "If we send personalized win-back emails with new features, then reactivation rate will increase by 25%, because value updates remind users why they joined",
                    "design": "A/B/C test: Generic vs New Features vs Personalized. Target 30-90 day dormant users",
                    "metrics": "14-day Reactivation Rate, Email Open Rate, Re-engagement",
                    "duration": "4 weeks"
                },
                {
                    "name": "Comeback Offer Campaign",
                    "channel": "📧 Email",
                    "hypothesis": "If we offer special discounts to churned users, then resurrection rate will increase by 48%, because financial incentive overcomes inertia",
                    "design": "Test discount levels (10%, 25%, 50%) vs control. Track reactivation and LTV",
                    "metrics": "Reactivation Rate, Offer Redemption, Post-Return LTV",
                    "duration": "6 weeks"
                },
                {
                    "name": "Retargeting Display Ads",
                    "channel": "🖼️ Display",
                    "hypothesis": "If we retarget dormant users showing their abandoned work, then return rate will increase by 35%, because reminding of invested effort triggers completion",
                    "design": "Intent-to-treat design. Retargeting campaign vs control. Track return and completion",
                    "metrics": "Return Rate, Completion Rate, Cost per Reactivation",
                    "duration": "6 weeks"
                },
                {
                    "name": "Social Media Win-Back",
                    "channel": "📱 Social Media",
                    "hypothesis": "If we target churned users with testimonial ads on social, then comeback rate will increase by 30%, because social proof rebuilds trust",
                    "design": "Lookalike audience of churned users. Test creative variants with testimonials",
                    "metrics": "Return Rate, Ad Engagement, Reactivation Cost",
                    "duration": "4-6 weeks"
                }
            ]
        },
        "Retention": {
            "color": GOOGLE_GREEN,
            "campaigns": [
                {
                    "name": "Proactive Success Email Outreach",
                    "channel": "📧 Email",
                    "hypothesis": "If we send proactive check-in emails at 60-day mark, then churn rate will decrease by 30%, because early intervention addresses pain points",
                    "design": "RCT on users approaching 60 days. Proactive outreach vs reactive support only",
                    "metrics": "90-day Retention Rate, NPS Score, Support Tickets",
                    "duration": "12 weeks"
                },
                {
                    "name": "Customer Loyalty Program",
                    "channel": "📱 Product/App",
                    "hypothesis": "If we introduce tiered loyalty rewards, then 12-month retention will increase by 35%, because rewards create switching costs",
                    "design": "Cohort test. Loyalty program vs control. Track retention, engagement, spend",
                    "metrics": "12-month Retention, Customer LTV, Program Engagement",
                    "duration": "12 months"
                },
                {
                    "name": "Educational Content Series",
                    "channel": "📧 Email",
                    "hypothesis": "If we send monthly best practices emails, then power user retention will increase by 28%, because ongoing education increases product value",
                    "design": "A/B test educational content vs product updates. Track retention by engagement",
                    "metrics": "Retention Rate, Email Engagement, Feature Adoption",
                    "duration": "6 months"
                },
                {
                    "name": "Annual Plan Promotion",
                    "channel": "📧 Email",
                    "hypothesis": "If we offer annual billing with 20% discount, then LTV will increase by 45%, because upfront commitment reduces churn opportunities",
                    "design": "Offer annual plan to random 50% of monthly subscribers. Track adoption and retention",
                    "metrics": "Annual Plan Adoption, Year 1 Retention, Revenue per User",
                    "duration": "12 months"
                }
            ]
        }
    }
    
    objective_options = ["Awareness", "Acquisition", "Activation", "Engagement", "Resurrection", "Retention"]
    
    selected_objective = st.selectbox(
        "**Select Business Objective**",
        objective_options,
        index=0,
        key="business_objective_select",
        help="Choose which lifecycle phase you want to optimize"
    )
    
    if not isinstance(selected_objective, str) or selected_objective not in ['Awareness', 'Acquisition', 'Activation', 'Engagement', 'Resurrection', 'Retention']:
        if isinstance(selected_objective, int):
            selected_objective = objective_options[selected_objective]
        else:
            selected_objective = "Awareness"
    
    # Get objective data
    objective_data = lifecycle_hypotheses[selected_objective]
    
    # Display campaigns with enhanced cards
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {GOOGLE_BG} 0%, white 100%); 
                padding: 1rem; border-radius: 10px; margin: 1rem 0;">
    <h3 style="color: {objective_data['color']}; margin: 0 0 0.5rem 0; font-size: 1.3rem;">
    🎯 {selected_objective} Campaigns
    </h3>
    <p style="color: {GOOGLE_GREY_LIGHT}; margin: 0; font-size: 0.9rem;">
    Recommended experiments to drive {selected_objective.lower()} across multiple channels
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get campaigns for this objective
    campaigns = objective_data["campaigns"]
    
    # Group campaigns by channel for organized display
    channels_used = list(set([camp["channel"] for camp in campaigns]))
    
    # Display campaigns organized by channel
    for channel in channels_used:
        channel_campaigns = [c for c in campaigns if c["channel"] == channel]
        
        with st.expander(f"{channel} Campaigns ({len(channel_campaigns)})", expanded=False):
            for idx, camp in enumerate(channel_campaigns, 1):
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {objective_data['color']}; margin: 0.6rem 0; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">
                <h5 style="color: {objective_data['color']}; margin-top: 0; font-size: 1rem;">{camp['name']}</h5>
                <p style="font-size: 0.9rem; line-height: 1.5; margin: 0.4rem 0;"><strong>Hypothesis:</strong> {camp['hypothesis']}</p>
                <p style="font-size: 0.85rem; color: #666; margin: 0.4rem 0; line-height: 1.4;"><strong>Design:</strong> {camp['design']}</p>
                <p style="font-size: 0.8rem; color: #888; margin: 0.2rem 0;">
                <strong>Metrics:</strong> {camp['metrics']} | <strong>Duration:</strong> {camp['duration']}
                </p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def tab_define_metrics():
    st.markdown('<p class="phase-header">📊 Phase 2: Define Metrics</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Select metrics that directly measure your hypothesis. A well-designed measurement plan includes
    <strong>success metrics</strong>, <strong>supporting metrics</strong>, and <strong>guardrail metrics</strong>.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metric selection interface
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">3️⃣ Build Your Measurement Plan</div>
    """, unsafe_allow_html=True)
    
    metric_tabs = st.tabs(["✅ Success Metrics", "🎯 Support Metrics", "🛡️ Guardrail Metrics", "📚 Full Dictionary"])
    
    with metric_tabs[0]:
        st.markdown("""
        ### Primary Success Metrics
        
        Your **Overall Evaluation Criterion (OEC)** - the main metric that determines experiment success.
        Choose 1-2 metrics that directly measure your hypothesis.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            success_metric = st.text_input(
                "Primary Success Metric",
                placeholder="e.g., Purchase Conversion Rate",
                help="The #1 metric that matters most"
            )
            success_why = st.text_area(
                "Why is this the right success metric?",
                placeholder="Links directly to revenue, measures end-to-end journey impact",
                height=100,
                help="Justify why this metric is your OEC"
            )
        
        with col2:
            st.markdown(f"""
            <div class="info-box" style="margin-top: 2rem;">
            <strong>💡 Good Success Metrics</strong>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.9rem;">
            <li>Directly tied to business value</li>
            <li>Sensitive to changes</li>
            <li>Measurable in experiment timeframe</li>
            <li>Not easily gamed</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        check_success = st.checkbox("✓ Success metric defined", key="success_metric")
    
    with metric_tabs[1]:
        st.markdown("""
        ### Supporting Metrics
        
        Secondary metrics that provide context and help interpret results. These explain **how** the treatment worked.
        """)
        
        support_metrics = st.multiselect(
            "Select 2-4 support metrics",
            ["CTR", "Time on Page", "Add-to-Cart Rate", "Scroll Depth", "Video Completion", "Pages/Session", "Bounce Rate"],
            help="Metrics that help explain the mechanism of change"
        )
        
        if support_metrics:
            st.markdown(f"""
            <div class="success-box">
            <strong>✓ Selected {len(support_metrics)} support metrics:</strong> {', '.join(support_metrics)}
            </div>
            """, unsafe_allow_html=True)
        
        check_support = st.checkbox("✓ Support metrics selected", key="support_metric")
    
    with metric_tabs[2]:
        st.markdown("""
        ### Guardrail Metrics
        
        Early warning system to ensure your treatment doesn't cause unintended harm.
        These metrics should **not** degrade significantly.
        """)
        
        guardrail_metrics = st.multiselect(
            "Select 2-3 guardrail metrics",
            ["Bounce Rate", "Cart Abandonment", "Unsubscribe Rate", "Page Load Time", "Error Rate", "Return Rate", "Customer Satisfaction"],
            help="Metrics that protect against negative side effects"
        )
        
        if guardrail_metrics:
            st.markdown(f"""
            <div class="warning-box">
            <strong>⚠️ Monitoring {len(guardrail_metrics)} guardrail metrics:</strong> {', '.join(guardrail_metrics)}
            <br><br>
            <strong>Remember:</strong> If any guardrail degrades significantly, consider not shipping even if primary metric improves.
            </div>
            """, unsafe_allow_html=True)
        
        check_guardrail = st.checkbox("✓ Guardrail metrics selected", key="guardrail_metric")
    
    with metric_tabs[3]:
        show_full_metrics_dictionary()
    
    # Progress indicator
    total_checks = sum([
        st.session_state.get('success_metric', False),
        st.session_state.get('support_metric', False),
        st.session_state.get('guardrail_metric', False)
    ])
    
    st.markdown(f"""
    <div style="margin-top: 2rem; padding: 1rem; background: {GOOGLE_BG}; border-radius: 8px;">
    <strong>Measurement Plan Progress:</strong> {total_checks}/3 complete
    <div style="background: white; height: 8px; border-radius: 10px; margin-top: 0.5rem; overflow: hidden;">
    <div style="background: linear-gradient(90deg, {GOOGLE_BLUE} 0%, {GOOGLE_GREEN} 100%); 
                height: 100%; width: {(total_checks/3)*100}%; transition: width 0.5s ease;"></div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_full_metrics_dictionary():
    """Enhanced metrics dictionary with better organization"""
    st.markdown("### 📊 Complete Marketing Metrics Dictionary")
    
    st.markdown(f"""
    <div class="info-box">
    <strong>How to use this dictionary:</strong>
    <ol style="margin: 0.5rem 0; padding-left: 1.5rem;">
    <li>🎯 Browse key metrics tracked for each channel</li>
    <li>📐 Reference probability distributions for sample sizing</li>
    <li>📍 Find baseline sources to gather historical benchmarks</li>
    <li>🛡️ Identify guardrail metrics alongside primary KPIs</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced channel display
    for channel in MARKETING_METRICS.keys():
        with st.expander(f"📱 {channel}", expanded=False):
            metrics = MARKETING_METRICS[channel]
            
            for idx, metric in enumerate(metrics):
                # Alternating background colors
                bg_color = GOOGLE_BG if idx % 2 == 0 else "white"
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1.25rem; border-radius: 8px; margin: 0.75rem 0; border-left: 4px solid {GOOGLE_BLUE};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                <h4 style="color: {GOOGLE_BLUE}; margin: 0 0 0.5rem 0;">{metric['name']}</h4>
                <p style="color: {GOOGLE_GREY}; margin: 0 0 0.75rem 0;">{metric['description']}</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.9rem;">
                <div><strong>Formula:</strong> <code>{metric['formula']}</code></div>
                <div><strong>Typical Range:</strong> {metric['typical_range']}</div>
                <div><strong>Distribution:</strong> {metric['distribution']}</div>
                <div><strong>Test:</strong> {metric['test']}</div>
                </div>
                
                <div style="background: rgba(66, 133, 244, 0.08); padding: 0.75rem; border-radius: 6px; margin-top: 0.75rem; font-size: 0.85rem;">
                <strong>📍 Where to get baseline:</strong> {metric['where_to_get_baseline']}<br>
                <em style="color: {GOOGLE_GREY_LIGHT};">Source: {metric['industry_source']}</em>
                </div>
                </div>
                
                <div style="margin-left: 1rem;">
                """, unsafe_allow_html=True)
                
                # Lifecycle badge
                lifecycle_colors = {
                    "Awareness": "badge-awareness",
                    "Consideration": "badge-consideration",
                    "Conversion": "badge-conversion",
                    "Retention": "badge-retention"
                }
                badge_class = lifecycle_colors.get(metric['lifecycle'], "badge-awareness")
                st.markdown(f'<div class="metric-badge {badge_class}">{metric["lifecycle"]}</div>', unsafe_allow_html=True)
                
                st.markdown("</div></div></div>", unsafe_allow_html=True)

def tab_design_experiment():
    st.markdown('<p class="phase-header">🔬 Phase 3: Experiment Design</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Calculate how long to run your test and how many samples you need to detect a meaningful effect.
    This is the most critical phase - getting sample size wrong wastes time and resources.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Randomization
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">🎲 Step 1: Randomization Strategy</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        unit = st.selectbox(
            "**Randomization Unit**",
            ["User ID", "Session ID", "Device ID", "Email Address", "Page View", "Geographic Region", "Account/Org ID"],
            help="What entity do you randomize on? Most common: User ID"
        )
        
        st.markdown(f"""
        <div class="info-box" style="margin-top: 1rem;">
        <strong>💡 Why randomization unit matters:</strong>
        <ul style="margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.9rem;">
        <li><strong>User ID:</strong> Consistent experience across sessions (recommended)</li>
        <li><strong>Session ID:</strong> Faster data but users may see both variants</li>
        <li><strong>Page View:</strong> Maximum speed but high contamination risk</li>
        <li><strong>Account ID:</strong> B2B tests where org-level effects matter</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        split = st.slider(
            "**Traffic Split** (%)",
            10, 50, 50, 5,
            help="% of traffic to treatment. 50/50 is most statistically powerful"
        )
        
        # Visual split representation
        st.markdown(f"""
        <div style="display: flex; gap: 0.5rem; margin: 1rem 0;">
        <div style="flex: {100-split}; background: {GOOGLE_BLUE}; padding: 1rem; border-radius: 8px; color: white; text-align: center; font-weight: 600;">
        Control<br>{100-split}%
        </div>
        <div style="flex: {split}; background: {GOOGLE_GREEN}; padding: 1rem; border-radius: 8px; color: white; text-align: center; font-weight: 600;">
        Treatment<br>{split}%
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if split != 50:
            power_loss = (50/split)**2
            st.warning(f"⚠️ Unequal split reduces statistical power. You'll need ~{power_loss:.1f}x more samples.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Select Metric
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">📏 Step 2: Select Primary Metric & Get Baseline</div>
    """, unsafe_allow_html=True)
    
    channel_options = ["Select a channel..."] + list(MARKETING_METRICS.keys())
    channel = st.selectbox("**Marketing Channel**", channel_options, index=0)
    
    if not isinstance(channel, str):
        if isinstance(channel, int) and 0 <= channel < len(channel_options):
            channel = channel_options[channel]
        else:
            channel = channel_options[0]
    
    if channel != "Select a channel...":
        metric_names = [m['name'] for m in MARKETING_METRICS[channel]]
        selected_metric_name = st.selectbox("**Primary Success Metric**", metric_names)
        
        selected_metric = next(m for m in MARKETING_METRICS[channel] if m['name'] == selected_metric_name)
        
        # Enhanced metric card
        st.markdown(f"""
        <div class="metric-card">
        <h4>{selected_metric['name']}</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
        <div>
        <p><strong>Description:</strong><br>{selected_metric['description']}</p>
        <p><strong>Formula:</strong><br><code>{selected_metric['formula']}</code></p>
        </div>
        <div>
        <p><strong>Distribution:</strong><br>{selected_metric['distribution']}</p>
        <p><strong>Statistical Test:</strong><br>{selected_metric['test']}</p>
        <p><strong>Typical Range:</strong><br>{selected_metric['typical_range']}</p>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📍 Where to Get Your Baseline Data"):
            st.info(selected_metric['where_to_get_baseline'])
            st.caption(f"**Industry Benchmark Source:** {selected_metric['industry_source']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 3: Power Analysis
        st.markdown(f"""
        <div class="section-container">
        <div class="section-title">⚡ Step 3: Power Analysis - Calculate Sample Size</div>
        <p style="color: {GOOGLE_GREY_LIGHT}; margin-bottom: 1rem; font-size: 0.9rem;">
        Sample size calculation ensures you have enough data to detect a meaningful effect
        </p>
        """, unsafe_allow_html=True)
        
        # Create three columns for inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 1️⃣ Baseline")
            baseline = st.number_input(
                "Current metric value (%)",
                min_value=0.1,
                max_value=100.0,
                value=5.0,
                step=0.1,
                help="Get from your analytics platform"
            )
            
            with st.expander("ℹ️ How to determine baseline"):
                st.markdown(f"""
                **For {selected_metric_name}:**
                
                1. **Check your analytics:** {selected_metric['where_to_get_baseline']}
                2. **Time window:** Use last 2-4 weeks (avoid seasonality)
                3. **Segment if needed:** Mobile vs Desktop, New vs Returning
                4. **Exclude outliers:** Remove bot traffic, test accounts
                5. **Verify stability:** Metric should be relatively stable, not trending
                
                **Industry benchmark:** {selected_metric['typical_range']}  
                *Source: {selected_metric['industry_source']}*
                
                ⚠️ **Common mistake:** Using a single day or including a promo period  
                ✅ **Best practice:** 2-4 week average excluding unusual events
                """)
        
        with col2:
            st.markdown("#### 2️⃣ MDE")
            mde = st.number_input(
                "Minimum Detectable Effect (%)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
                help="Relative % change you want to detect"
            )
            
            absolute_change = baseline * (mde / 100)
            new_value = baseline + absolute_change
            
            st.metric("New Value", f"{new_value:.2f}%", f"+{absolute_change:.2f}%p")
            
            with st.expander("ℹ️ How to choose MDE"):
                st.markdown(f"""
                **MDE (Minimum Detectable Effect)** is the smallest change that matters to your business.
                
                **Framework for choosing MDE:**
                
                1. **Business Value Calculation:**
                   - If {selected_metric_name} improves by {mde}%, what's the $ impact?
                   - Does it cover cost of implementation + experiment?
                   - Example: 10% CVR increase on $1M/month revenue = $100K/month
                
                2. **Typical MDE by Metric Type:**
                   - 🟢 **High-frequency metrics** (CTR, Opens): 5-15% is detectable
                   - 🟡 **Medium-frequency** (CVR, Add-to-Cart): 10-20% realistic
                   - 🔴 **Low-frequency** (Purchases, Subscriptions): 15-30% needed
                
                3. **Trade-offs:**
                   - Smaller MDE = Longer test duration = More resources
                   - Larger MDE = Shorter test = Faster decisions but miss small wins
                
                4. **Reality Check:**
                   - Current: {baseline:.2f}%
                   - {mde}% change = {new_value:.2f}%
                   - Is this realistic? Most winning tests: 5-20% improvement
                
                ⚠️ **Common mistake:** MDE too small (3-5%) requires months of data  
                ✅ **Best practice:** Start with 10-15% MDE, iterate based on results
                """)
        
        with col3:
            st.markdown("#### 3️⃣ Parameters")
            alpha = st.number_input(
                "Significance level (α)",
                min_value=0.01,
                max_value=0.10,
                value=0.05,
                step=0.01,
                help="False positive rate (standard: 0.05)"
            )
            
            with st.expander("ℹ️ Understanding Alpha (α)"):
                st.markdown(f"""
                **Alpha (α)** is your tolerance for **false positives** - declaring a winner when there's actually no effect.
                
                **What it means:**
                - α = 0.05 means 5% chance of false positive (Type I error)
                - If you run 20 A/A tests, you'd expect ~1 false positive
                
                **When to adjust:**
                - **α = 0.01** (stricter): High-risk changes (billing, checkout flow)
                - **α = 0.05** (standard): Most marketing tests - **RECOMMENDED**
                - **α = 0.10** (looser): Early-stage exploration, low risk
                
                **Multiple Testing Problem:**
                - If testing 10 metrics, chance of ≥1 false positive = 40%!
                - Solution: Bonferroni correction (α/n) or FDR control
                - Best practice: Declare ONE primary metric before test
                
                **P-value interpretation:**
                - p < α → Reject null hypothesis (statistically significant)
                - p ≥ α → Fail to reject null (not significant)
                
                ⚠️ **Common mistake:** p=0.051, "almost significant" → Still not significant!  
                ✅ **Best practice:** Set α=0.05 and stick to it. No p-hacking.
                """)
            
            power = st.number_input(
                "Statistical power (1-β)",
                min_value=0.70,
                max_value=0.95,
                value=0.80,
                step=0.05,
                help="Detection rate (standard: 0.80)"
            )
            
            with st.expander("ℹ️ Understanding Power (1-β)"):
                st.markdown(f"""
                **Power (1-β)** is your ability to **detect a real effect** when it exists.
                
                **What it means:**
                - Power = 0.80 means 80% chance of detecting true effect (if MDE exists)
                - β = 0.20 means 20% chance of false negative (Type II error)
                - Higher power = need more samples = longer test
                
                **Power trade-offs:**
                - **0.70 (70%)**: Acceptable for early exploration, faster tests
                - **0.80 (80%)**: Industry standard - **RECOMMENDED**
                - **0.90 (90%)**: High-stakes decisions, worth extra time
                
                **What affects power:**
                1. Sample size ↑ → Power ↑ (most controllable)
                2. MDE ↑ → Power ↑ (larger effects easier to detect)
                3. Variance ↓ → Power ↑ (more consistent data)
                4. α ↑ → Power ↑ (but more false positives)
                
                **Power vs Sample Size:**
                - 0.80 power: baseline sample size
                - 0.90 power: ~1.4x more samples needed
                - 0.95 power: ~1.8x more samples needed
                
                **Underpowered tests are dangerous:**
                - True winner might appear non-significant
                - Waste resources running test that can't detect effect
                - False confidence from noisy results
                
                ⚠️ **Common mistake:** Running test without power calculation  
                ✅ **Best practice:** Calculate sample size BEFORE starting test
                """)
        
        # Calculate button
        if st.button("🧮 Calculate Sample Size", type="primary", use_container_width=True):
            p1 = baseline / 100
            p2 = new_value / 100
            
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            
            pooled_p = (p1 + p2) / 2
            n_per_group = ((z_alpha * math.sqrt(2 * pooled_p * (1 - pooled_p)) + 
                           z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p2 - p1)) ** 2
            
            n_per_group = int(math.ceil(n_per_group))
            n_total = n_per_group * 2
            
            st.session_state.experiment_data.update({
                'channel': channel,
                'metric': selected_metric_name,
                'baseline': baseline,
                'mde': mde,
                'sample_size_per_group': n_per_group,
                'total_sample_size': n_total,
                'alpha': alpha,
                'power': power,
                'calculated': True
            })
            st.rerun()
        
        # Show results if calculated
        if st.session_state.experiment_data.get('calculated'):
            n_per_group = st.session_state.experiment_data['sample_size_per_group']
            n_total = st.session_state.experiment_data['total_sample_size']
            
            st.markdown("---")
            st.markdown("### 📊 Sample Size Results")
            
            # Enhanced results display
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("**Per Group**", f"{n_per_group:,}", help="Samples needed per variant")
            with col2:
                st.metric("**Total Samples**", f"{n_total:,}", help="Total across both groups")
            with col3:
                st.metric("**Traffic Split**", f"{100-split}/{split}", help="Control/Treatment")
            
            # Visualization
            p1 = baseline / 100
            p2 = new_value / 100
            
            x_control = np.linspace(0, n_per_group, 1000)
            y_control = stats.norm.pdf(x_control, n_per_group*p1, np.sqrt(n_per_group*p1*(1-p1)))
            
            x_treatment = np.linspace(0, n_per_group, 1000)
            y_treatment = stats.norm.pdf(x_treatment, n_per_group*p2, np.sqrt(n_per_group*p2*(1-p2)))
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x_control, y=y_control, name='Control',
                fill='tozeroy', fillcolor=f'rgba(66, 133, 244, 0.3)',
                line=dict(color=GOOGLE_BLUE, width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=x_treatment, y=y_treatment, name='Treatment',
                fill='tozeroy', fillcolor=f'rgba(52, 168, 83, 0.3)',
                line=dict(color=GOOGLE_GREEN, width=3)
            ))
            
            fig.update_layout(
                title=dict(
                    text=f"<b>Sampling Distributions</b><br><sub>Control ({baseline}%) vs Treatment ({new_value:.2f}%)</sub>",
                    font=dict(size=16, family='Google Sans')
                ),
                xaxis_title="Number of Successes",
                yaxis_title="Probability Density",
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Step 4: Duration
            st.markdown("---")
            st.markdown("### ⏱️ Step 4: Calculate Test Duration")
            
            daily_traffic = st.number_input(
                "**Average Daily Visitors/Users**",
                min_value=100,
                max_value=10000000,
                value=10000,
                step=1000,
                help="Get from Google Analytics"
            )
            
            effective_daily = daily_traffic * (split / 100)
            days_needed = math.ceil(n_per_group / effective_daily)
            
            st.session_state.experiment_data['duration_days'] = days_needed
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Daily Traffic", f"{daily_traffic:,}")
            col2.metric("Effective Daily", f"{int(effective_daily):,}")
            col3.metric("**Test Duration**", f"**{days_needed} days**")
            
            # Duration guidance
            if days_needed < 7:
                st.markdown(f"""
                <div class="warning-box">
                <strong>⚠️ Short Duration: {days_needed} days</strong><br><br>
                Consider running for at least 7-14 days to:
                <ul>
                <li>Capture weekly patterns (weekday vs weekend)</li>
                <li>Allow novelty effect to settle</li>
                <li>Ensure statistical validity</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif days_needed <= 14:
                st.markdown(f"""
                <div class="success-box">
                <strong>✅ Ideal Duration: {days_needed} days</strong><br><br>
                This duration balances speed with statistical validity.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-box">
                <strong>⚠️ Long Duration: {days_needed} days ({days_needed/7:.1f} weeks)</strong><br><br>
                Consider:
                <ul>
                <li>Increasing MDE to shorten test</li>
                <li>Lowering power to 0.70-0.75</li>
                <li>Sequential testing with adjusted α</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Final summary
            st.markdown(f"""
            <div class="success-box" style="margin-top: 2rem;">
            <h4>📋 Experiment Design Summary</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div>
            <p><strong>Metric:</strong> {selected_metric_name}</p>
            <p><strong>Channel:</strong> {channel}</p>
            <p><strong>Baseline:</strong> {baseline}%</p>
            </div>
            <div>
            <p><strong>Target:</strong> {new_value:.2f}%</p>
            <p><strong>Sample Size:</strong> {n_per_group:,} per group</p>
            <p><strong>Duration:</strong> {days_needed} days</p>
            </div>
            </div>
            <p style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid {GOOGLE_LIGHT_GREY};">
            <strong>Statistical Parameters:</strong> {int(power*100)}% power to detect {mde}% relative change with α={alpha}
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def tab_implementation():
    st.markdown('<p class="phase-header">🚀 Phase 4: Implementation</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Move from design to execution with confidence. Use this comprehensive checklist to align 
    engineering, analytics, and stakeholders before launching your experiment.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Experiment snapshot
    data = st.session_state.experiment_data
    if data:
        st.markdown(f"""
        <div class="info-box">
        <h4 style="margin: 0 0 1rem 0;">📋 Experiment Snapshot</h4>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
        <div>
        <strong>Channel:</strong> {data.get('channel', 'N/A')}<br>
        <strong>Metric:</strong> {data.get('metric', 'N/A')}
        </div>
        <div>
        <strong>Sample Size:</strong> {data.get('sample_size_per_group', 'N/A'):,}/group<br>
        <strong>Duration:</strong> {data.get('duration_days', 'N/A')} days
        </div>
        <div>
        <strong>α:</strong> {data.get('alpha', '0.05')}<br>
        <strong>Power:</strong> {int(data.get('power', 0.8)*100)}%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">🎯 Launch Checklist</div>
    """, unsafe_allow_html=True)
    
    launch_col1, launch_col2 = st.columns(2)
    
    with launch_col1:
        st.markdown("#### 🛠 Technical Implementation")
        
        checks = [
            ("impl_tracking", "Event tracking verified in staging/dogfood"),
            ("impl_flag", "Experiment flag configured with correct exposure rules"),
            ("impl_eligibility", "Eligibility & exclusion criteria validated"),
            ("impl_srm", "SRM alert configured (sample ratio mismatch monitoring)")
        ]
        
        for key, label in checks:
            if st.checkbox(label, key=key):
                st.markdown(f"<span style='color: {GOOGLE_GREEN};'>✓</span>", unsafe_allow_html=True)
        
        st.text_area(
            "**Monitoring Dashboard Links**",
            placeholder="Paste links to dashboards, logging, metric alerts...",
            key="impl_dashboards",
            height=100
        )
    
    with launch_col2:
        st.markdown("#### 🤝 Cross-functional Alignment")
        
        checks = [
            ("impl_alignment", "Launch checklist reviewed with Eng/Product/Analytics"),
            ("impl_rollout", "Rollout & rollback plan documented"),
            ("impl_comms", "Communications plan ready (stakeholders, support)"),
            ("impl_qa", "QA playbook signed off (acceptance criteria met)")
        ]
        
        for key, label in checks:
            if st.checkbox(label, key=key):
                st.markdown(f"<span style='color: {GOOGLE_GREEN};'>✓</span>", unsafe_allow_html=True)
        
        st.text_area(
            "**Risks & Mitigation**",
            placeholder="Dependencies, guardrail monitoring, on-call rotations...",
            key="impl_risks",
            height=100
        )
    
    # Launch timeline
    st.markdown("---")
    st.markdown("#### 📅 Launch Timeline")
    
    col1, col2, col3 = st.columns(3)
    col1.date_input("**Target Launch Date**", key="impl_launch_date")
    col2.date_input("**Mid-test Check-in**", key="impl_mid_check")
    col3.date_input("**Planned End Date**", key="impl_end_date")
    
    st.markdown('</div>', unsafe_allow_html=True)

def tab_analysis():
    st.markdown('<p class="phase-header">📈 Phase 5: Analysis</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Your experiment has completed. Now analyze the results, interpret statistical significance, 
    and make a data-driven decision based on rigorous statistical methods.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Experiment recap
    with st.expander("📋 Your Experiment Design Recap", expanded=False):
        if st.session_state.experiment_data:
            data = st.session_state.experiment_data
            st.markdown(f"""
            - **Channel:** {data.get('channel', 'N/A')}
            - **Metric:** {data.get('metric', 'N/A')}
            - **Baseline:** {data.get('baseline', 0):.2f}%
            - **MDE:** {data.get('mde', 0):.1f}%
            - **Sample Size:** {data.get('sample_size_per_group', 0):,} per group
            - **Duration:** {data.get('duration_days', 0)} days
            """)
    
    # Step 1: Data Quality
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">✅ Step 1: Data Quality & Sanity Checks</div>
    <p style="color: {GOOGLE_GREY_LIGHT};">Before analyzing, verify your data is trustworthy</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Sample Ratio Mismatch Check")
        expected_ratio = st.number_input("Expected Split (Control%)", 0, 100, 50)
        actual_control_n = st.number_input("Actual Control Sample", 0, 10000000, 10000, key="srm_control")
        actual_treatment_n = st.number_input("Actual Treatment Sample", 0, 10000000, 10000, key="srm_treatment")
        
        total_samples = actual_control_n + actual_treatment_n
        actual_control_pct = (actual_control_n / total_samples * 100) if total_samples > 0 else 0
        
        # Chi-square SRM test
        expected_control = total_samples * (expected_ratio / 100)
        expected_treatment = total_samples * (1 - expected_ratio / 100)
        
        chi2_stat = ((actual_control_n - expected_control)**2 / expected_control + 
                     (actual_treatment_n - expected_treatment)**2 / expected_treatment)
        srm_p_value = 1 - stats.chi2.cdf(chi2_stat, 1)
        
        col_a, col_b = st.columns(2)
        col_a.metric("Actual Control %", f"{actual_control_pct:.1f}%")
        col_b.metric("SRM P-value", f"{srm_p_value:.4f}")
        
        if srm_p_value < 0.001:
            st.markdown(f"""
            <div class="danger-box">
            <strong>🚨 SRM DETECTED</strong> (p={srm_p_value:.6f})<br><br>
            Sample sizes deviate significantly. Possible causes:
            <ul>
            <li>Bot traffic affecting one variant</li>
            <li>Randomization implementation bug</li>
            <li>Triggering condition issues</li>
            </ul>
            <strong>⚠️ DO NOT TRUST RESULTS</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="success-box">
            ✅ <strong>No SRM detected</strong> (p={srm_p_value:.4f})
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🧪 A/A Test Recommendation")
        st.markdown(f"""
        <div class="info-box">
        <strong>Have you run an A/A test?</strong><br><br>
        An A/A test verifies:
        <ul>
        <li>✓ Randomization works correctly</li>
        <li>✓ No systematic biases</li>
        <li>✓ False positive rate matches α</li>
        </ul>
        <strong>Best practice:</strong> Run before first real experiment
        </div>
        """, unsafe_allow_html=True)
        
        aa_test_done = st.checkbox("A/A test passed", key="aa_test")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Enter Results
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">📊 Step 2: Enter Experiment Results</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Control Group (A)")
        control_n = st.number_input("Total Sample Size", 100, 10000000, 10000, key="results_control_n")
        control_x = st.number_input("Number of Successes", 0, control_n, int(control_n*0.05), key="results_control_x")
        control_rate = control_x / control_n if control_n > 0 else 0
        
        st.metric("Control Rate", f"{control_rate*100:.2f}%", f"{control_x:,} successes")
    
    with col2:
        st.markdown("#### Treatment Group (B)")
        treatment_n = st.number_input("Total Sample Size", 100, 10000000, 10000, key="results_treatment_n")
        treatment_x = st.number_input("Number of Successes", 0, treatment_n, int(treatment_n*0.055), key="results_treatment_x")
        treatment_rate = treatment_x / treatment_n if treatment_n > 0 else 0
        
        st.metric("Treatment Rate", f"{treatment_rate*100:.2f}%", f"{treatment_x:,} successes")
    
    # Step 3: Analyze
    if st.button("📊 Analyze Results", type="primary", use_container_width=True):
        # Two-proportion z-test
        pooled_rate = (control_x + treatment_x) / (control_n + treatment_n)
        se_pooled = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_n + 1/treatment_n))
        
        z_stat = (treatment_rate - control_rate) / se_pooled if se_pooled > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Confidence interval
        se_diff = math.sqrt(control_rate * (1 - control_rate) / control_n + 
                           treatment_rate * (1 - treatment_rate) / treatment_n)
        ci_lower = (treatment_rate - control_rate) - 1.96 * se_diff
        ci_upper = (treatment_rate - control_rate) + 1.96 * se_diff
        
        # Effect size
        absolute_lift = (treatment_rate - control_rate) * 100
        relative_lift = ((treatment_rate - control_rate) / control_rate) * 100 if control_rate > 0 else 0
        
        st.session_state['analysis_results'] = {
            'control_n': control_n,
            'treatment_n': treatment_n,
            'control_rate': control_rate,
            'treatment_rate': treatment_rate,
            'p_value': p_value,
            'absolute_lift': absolute_lift,
            'relative_lift': relative_lift,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'z_stat': z_stat,
            'se_diff': se_diff
        }
        
        st.markdown("---")
        st.markdown("### 📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Absolute Lift", f"{absolute_lift:.2f}%p")
        col2.metric("Relative Lift", f"{relative_lift:.2f}%")
        col3.metric("P-value", f"{p_value:.4f}")
        
        if p_value < 0.05:
            col4.metric("Result", "✅ Significant")
        else:
            col4.metric("Result", "❌ Not Sig")
        
        st.caption(f"**95% CI:** [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]")
        
        # Interpretation
        st.markdown("### 🎯 Statistical Interpretation")
        
        if p_value < 0.05:
            if relative_lift > 0:
                st.markdown(f"""
                <div class="success-box">
                <h4>✅ Statistically Significant Improvement</h4>
                <p><strong>Treatment is {relative_lift:.1f}% better</strong> than control (p={p_value:.4f})</p>
                <ul>
                <li>Only a {p_value*100:.2f}% chance of seeing this by random chance</li>
                <li>True effect likely between {ci_lower*100:.2f}% and {ci_upper*100:.2f}% (95% confidence)</li>
                <li>Strong evidence for treatment effectiveness</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="danger-box">
                <h4>❌ Statistically Significant Degradation</h4>
                <p><strong>Treatment is {abs(relative_lift):.1f}% worse</strong> (p={p_value:.4f})</p>
                <p>The treatment caused a significant decline. This is valuable learning!</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box">
            <h4>⚠️ Not Statistically Significant</h4>
            <p>No significant difference detected (p={p_value:.4f} ≥ 0.05)</p>
            <p>The observed {relative_lift:.2f}% change could be due to random chance.</p>
            <p><strong>Possible reasons:</strong> No true effect, underpowered test, high variance, or bad timing</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Control',
            x=['Conversion Rate'],
            y=[control_rate*100],
            marker_color=GOOGLE_BLUE,
            text=[f'{control_rate*100:.2f}%'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='Treatment',
            x=['Conversion Rate'],
            y=[treatment_rate*100],
            marker_color=GOOGLE_GREEN if treatment_rate > control_rate else GOOGLE_RED,
            text=[f'{treatment_rate*100:.2f}%'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f'<b>Control vs Treatment</b><br><sub>p={p_value:.4f}</sub>',
            yaxis_title='Conversion Rate (%)',
            barmode='group',
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Google Sans'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def tab_decision():
    st.markdown('<p class="phase-header">✅ Phase 6: Decision</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-container">
    <p style="font-size: 1rem; line-height: 1.6; color: {GOOGLE_GREY}; margin: 0;">
    Make an informed decision about rolling out the treatment. Quantify business impact,
    assess ROI, and document your learnings for future experiments.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    results = st.session_state.get('analysis_results')
    if not results:
        st.info("📊 Run the analysis phase first to compute experiment outcomes")
        return
    
    control_rate = results['control_rate']
    treatment_rate = results['treatment_rate']
    absolute_lift = results['absolute_lift']
    relative_lift = results['relative_lift']
    p_value = results['p_value']
    ci_lower = results['ci_lower']
    ci_upper = results['ci_upper']
    
    # Step 4: Recommendation
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">💡 Step 4: Decision Framework</div>
    """, unsafe_allow_html=True)
    
    if p_value < 0.05 and relative_lift > 0:
        st.markdown(f"""
        <div class="success-box">
        <h4>✅ RECOMMENDATION: ROLL OUT TREATMENT</h4>
        <p><strong>Rationale:</strong></p>
        <ul>
        <li>Statistically significant improvement: {relative_lift:.1f}% (p={p_value:.4f})</li>
        <li>95% confident true effect is positive (CI: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%])</li>
        <li>Low risk given strong statistical evidence</li>
        </ul>
        <p><strong>Next Steps:</strong></p>
        <ol>
        <li>Check guardrail metrics for degradation</li>
        <li>Perform segment analysis (device, geo, cohort)</li>
        <li>Plan gradual rollout (10% → 50% → 100%)</li>
        <li>Document learnings for future tests</li>
        <li>Maintain 5-10% holdout for long-term measurement</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    elif p_value < 0.05 and relative_lift < 0:
        st.markdown(f"""
        <div class="danger-box">
        <h4>❌ RECOMMENDATION: DO NOT ROLL OUT</h4>
        <p>Statistically significant <strong>degradation</strong>: {abs(relative_lift):.1f}% worse</p>
        <p><strong>Next Steps:</strong></p>
        <ol>
        <li>Perform root-cause analysis (session replays, user feedback)</li>
        <li>Look for segment-specific wins</li>
        <li>Refine hypothesis and iterate on improved variant</li>
        <li>Document findings - negative results are valuable</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box">
        <h4>⚠️ RECOMMENDATION: CONTEXT-DEPENDENT</h4>
        <p>No statistically significant difference (p={p_value:.4f})</p>
        <p><strong>Options:</strong></p>
        <ul>
        <li><strong>Extend test:</strong> Increase exposure to reduce variance</li>
        <li><strong>Ship anyway:</strong> Only if cost/risk is low</li>
        <li><strong>Abandon & iterate:</strong> Design new variant</li>
        <li><strong>Sequential testing:</strong> Plan another checkpoint</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 5: Business Impact
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">💰 Step 5: Quantify Business Impact</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_users = st.number_input(
            "**Expected Monthly Users**",
            min_value=1000,
            max_value=1_000_000_000,
            value=100_000,
            step=10_000
        )
        value_per_conversion = st.number_input(
            "**Value per Conversion ($)**",
            min_value=0.0,
            max_value=100_000.0,
            value=50.0,
            step=5.0
        )
    
    with col2:
        baseline_conversions = monthly_users * control_rate
        treatment_conversions = monthly_users * treatment_rate
        incremental_conversions = treatment_conversions - baseline_conversions
        monthly_impact = incremental_conversions * value_per_conversion
        annual_impact = monthly_impact * 12
        
        st.metric("Baseline Conversions/Month", f"{baseline_conversions:,.0f}")
        st.metric("Incremental Conversions/Month", f"{incremental_conversions:,.0f}")
        st.metric("**Monthly Revenue Impact**", f"**${monthly_impact:,.0f}**")
        st.metric("**Annual Revenue Impact**", f"**${annual_impact:,.0f}**")
    
    # ROI Assessment
    st.markdown("---")
    st.markdown("#### 🎯 ROI Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        implementation_cost = st.number_input(
            "One-time Implementation Cost ($)",
            0, 1_000_000, 10_000, 1_000
        )
    with col2:
        ongoing_cost_monthly = st.number_input(
            "Ongoing Monthly Cost ($)",
            0, 100_000, 0, 500
        )
    
    first_month_net = monthly_impact - implementation_cost - ongoing_cost_monthly
    ongoing_monthly_net = monthly_impact - ongoing_cost_monthly
    
    if monthly_impact > ongoing_cost_monthly and monthly_impact > 0:
        months_to_roi = implementation_cost / monthly_impact
    else:
        months_to_roi = float("inf")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("First Month Net", f"${first_month_net:,.0f}")
    col2.metric("Ongoing Monthly Net", f"${ongoing_monthly_net:,.0f}")
    col3.metric("Months to ROI", f"{months_to_roi:.1f}" if months_to_roi != float('inf') else "N/A")
    
    if first_month_net > 0:
        st.markdown("""
        <div class="success-box">
        ✅ <strong>Positive ROI from Month 1</strong> - Implementation cost recovered immediately
        </div>
        """, unsafe_allow_html=True)
    elif months_to_roi <= 6:
        st.markdown(f"""
        <div class="success-box">
        ✅ <strong>Good ROI</strong> - Recovered in {months_to_roi:.1f} months
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="danger-box">
        ❌ <strong>Questionable ROI</strong> - Re-evaluate effort vs benefit
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rollout Strategy
    st.markdown(f"""
    <div class="section-container">
    <div class="section-title">🚀 Rollout Strategy</div>
    """, unsafe_allow_html=True)
    
    rollout_options = {
        "Staged rollout (10% → 50% → 100%)": "Gradual ramp with monitoring",
        "Holdout control (keep 5-10%)": "Maintain ghost control for long-term measurement",
        "Geo / cohort phased launch": "Staggered deployment by market",
        "Dark launch (behind feature flag)": "Enable for internal/QA first",
        "Do not roll out": "Capture learnings and iterate"
    }
    
    default_strategy = "Staged rollout (10% → 50% → 100%)" if p_value < 0.05 and relative_lift > 0 else "Do not roll out"
    strategy_options = list(rollout_options.keys())
    
    try:
        default_index = strategy_options.index(default_strategy)
    except ValueError:
        default_index = 0
    
    selected_strategy = st.selectbox(
        "**Recommended Rollout Approach**",
        strategy_options,
        index=default_index
    )
    
    if not isinstance(selected_strategy, str) or selected_strategy not in rollout_options:
        if isinstance(selected_strategy, int):
            selected_strategy = strategy_options[selected_strategy]
        else:
            selected_strategy = strategy_options[0]
    
    st.markdown(f"""
    <div class="info-box">
    <strong>{selected_strategy}</strong><br>
    {rollout_options[selected_strategy]}
    </div>
    """, unsafe_allow_html=True)
    
    st.text_area(
        "**Launch Plan Notes**",
        placeholder="Document owners, dates, communication steps, success checkpoints, rollback triggers...",
        key="rollout_notes",
        height=100
    )
    
    # Final Summary
    st.markdown("---")
    st.markdown("### 📋 Final Experiment Summary")
    
    st.markdown(f"""
    <div class="metric-card">
    <h4>Experiment Results</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
    <div>
    <p><strong>Control Rate:</strong><br>{control_rate*100:.2f}%</p>
    <p><strong>Treatment Rate:</strong><br>{treatment_rate*100:.2f}%</p>
    </div>
    <div>
    <p><strong>Absolute Lift:</strong><br>{absolute_lift:.2f}%p</p>
    <p><strong>Relative Lift:</strong><br>{relative_lift:.2f}%</p>
    </div>
    <div>
    <p><strong>P-value:</strong><br>{p_value:.4f}</p>
    <p><strong>95% CI:</strong><br>[{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]</p>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.success("🎉 Experiment complete! Document your findings in your experimentation log for future reference.")

if __name__ == "__main__":
    main()