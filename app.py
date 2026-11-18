import sys, json, io, csv, base64
from pathlib import Path
from datetime import datetime, timezone, time, date
from urllib.parse import urlsplit, parse_qs
from decimal import Decimal, InvalidOperation
sys.path.insert(0,str(Path(__file__).parent/'src'))
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from scamtrace import providers
from scamtrace import database
from scamtrace.workflow import run_investigation
from scamtrace.scenarios import scenarios
from scamtrace.graph import build_graph
from scamtrace.agents import AGENT_NAMES

st.set_page_config(page_title="UPI ScamTrace",page_icon="🛡️",layout="wide",initial_sidebar_state="expanded")
database.init_db()
llm_config=providers.config_summary()
PAGES=["Dashboard","New Investigation","Case History","Analytics","About Project"]
CSS="""
<style>
:root{--emerald:#142923;--gold:#C6A76A;--ivory:#F5F2EA;--card:#FFFCF5;--ink:#17231E;--muted:#66716A;--line:#E9E1D2}
.stApp{background:#F5F2EA;color:#17231E;font-family:Inter,'Segoe UI',sans-serif}.block-container{padding:8px 18px 0;max-width:none}
header[data-testid="stHeader"]{height:0!important;min-height:0!important;visibility:hidden!important}
[data-testid="stMainBlockContainer"]{padding-top:2px!important}
[data-testid="stVerticalBlock"]{gap:.16rem!important}
[data-testid="stHorizontalBlock"]{gap:.55rem!important}
[data-testid="stSidebar"]{background:#142923;min-width:282px!important;width:282px!important;max-width:282px!important}
[data-testid="stSidebar"] > div:first-child{padding:0 10px!important}
[data-testid="stSidebarUserContent"]{margin-top:-60px!important;transform:translateY(19px)!important}
.brand,.sidebar-phone{margin-left:-10px!important;width:calc(100% + 20px)!important;background:#142923}.brand{margin-top:-16px!important;margin-bottom:55px!important}.sidebar-phone img{margin-top:51px!important}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:0!important}
[data-testid="stSidebar"] *{color:#F9F5E9}
[data-testid="stSidebar"] div.stButton{margin:0!important}
[data-testid="stSidebar"] div.stButton>button{height:50px!important;min-height:50px!important;width:100%;background:transparent!important;color:#F8F4E8!important;border:0!important;text-align:left!important;padding:0 17px!important;white-space:nowrap!important;font-size:16px!important;font-weight:650!important;border-radius:11px!important}
[data-testid="stSidebar"] div.stButton>button:hover{background:#142923!important;border-radius:11px!important}
[data-testid="stSidebar"] div.stButton>button[kind="primary"], [data-testid="stSidebar"] div.stButton>button[aria-pressed="true"]{background:linear-gradient(105deg,#C6A76A,#C6A76A)!important;color:#17231E!important}
[data-testid="stSidebar"] div.stButton>button[kind="primary"] p,[data-testid="stSidebar"] div.stButton>button[aria-pressed="true"] p{color:#17231E!important}
h1,h2,h3{color:#17231E!important;letter-spacing:-.025em}h3{font-size:19px!important;line-height:1.15!important;margin:.1rem 0 .38rem!important}
section.stMain > div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"]{gap:.32rem}
.brand img{display:block;width:100%;height:auto;margin:0 0 12px;mix-blend-mode:lighten}
.sidebar-phone img{display:block;width:94%;height:auto;margin-left:3%;margin-top:18px;mix-blend-mode:lighten}
.sidebar-status{background:#142923;border:1px solid #C6A76A;border-radius:14px;padding:12px 14px;margin:64px 0 6px;font-size:14px;font-weight:700;line-height:1.3}
.sidebar-status small{font-size:12px;font-weight:600;color:#64D77E!important}
.page-header{display:flex;align-items:flex-start;justify-content:space-between;min-height:70px;padding:0 4px 7px;transform:translateY(-14px)}
.page-header h1{font-size:30px;line-height:1.08;margin:0 0 4px;font-weight:750}
.page-header p{font-size:14px;line-height:1.25;margin:0;color:#17231E}
.profile{display:flex;align-items:center;gap:12px;padding-top:2px;font-size:14px;font-weight:650;white-space:nowrap;transform:translateY(10px)}
.profile .bell{position:relative;display:inline-flex;align-items:center;justify-content:center;width:24px;height:28px}.profile .bell svg{width:23px;height:23px;stroke:#17231E;fill:none;stroke-width:1.8}.profile .avatar{width:38px;height:38px;border-radius:50%;background:#F4E8C5;border:1px solid #C6A76A;display:inline-flex;align-items:center;justify-content:center}.profile .avatar svg{width:23px;height:23px;stroke:#17231E;fill:none;stroke-width:1.8}
.hero{background:linear-gradient(110deg,#142923,#142923);color:#fff;border-radius:15px;padding:0;margin:0 0 2px;box-shadow:0 4px 13px #152b241c;overflow:hidden}
.hero h2{color:#C6A76A!important;margin:0 0 2px;font-size:20px}.hero p{margin:0;color:#e9ede8;font-size:13px}
.hero .progressrow{font-size:11px;color:#e9ede8;margin-top:6px;letter-spacing:.02em}
.hero-reference{width:100%;height:216px;background-position:center;background-size:100% 100%;border-radius:15px}
.st-key-dashboard-actions{height:0!important;position:relative;z-index:5;margin-top:-78px!important;margin-bottom:52px!important;padding-left:48px!important;overflow:visible!important}
.st-key-dashboard-actions button{height:51px!important;min-height:51px!important;width:250px!important;opacity:0!important;cursor:pointer!important}
.investigation-hero-reference{width:100%;height:144px;background-position:center;background-size:100% 100%;border-radius:15px;margin-bottom:8px}
.about-hero-reference{width:100%;height:126px;background-position:center;background-size:100% 100%;border-radius:15px;margin-bottom:8px}
.panel{background:#FFFCF5;border:1px solid #E8E0D2;border-radius:13px;padding:10px 13px;margin-bottom:5px;box-shadow:0 2px 6px #392d150e}
.panel h3{font-size:16px;margin:0 0 9px}.muted{color:#66716A;font-size:12px}.gold{color:#C6A76A}.pill{display:inline-block;border-radius:20px;padding:4px 9px;background:#efe7d5;font-size:11px;font-weight:700}
.metric{background:#FFFCF5;border:1px solid #E8E0D2;border-radius:14px;padding:7px 10px;text-align:left;height:86px;box-sizing:border-box;display:flex;align-items:center;gap:16px;box-shadow:0 2px 5px #392d150c}
.metric .mi{width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#F8EDD4;font-size:30px}
.metric b{font-size:29px;color:#17231E;line-height:1.0}.metric small{display:block;color:#17231E;font-size:15px;font-weight:650;margin-top:4px}
.step{display:flex;gap:10px;align-items:center;background:#edf2ec;padding:10px;border-radius:8px;font-size:12px}
div.stButton>button{border-radius:9px;border:1px solid #C6A76A;color:#17231E;font-weight:700;min-height:36px;padding:3px 15px;background:#FFFCF5}
div.stButton>button[kind="primary"]{background:linear-gradient(105deg,#C6A76A,#C6A76A);color:#17231E;border:0}
div.stButton>button:disabled,div.stDownloadButton>button:disabled{background:#e9e5dc!important;color:#66716A!important;border:1px solid #d8d1c3!important;opacity:1!important;cursor:not-allowed!important}
[data-testid="stTabs"] button{font-size:14px!important;padding:9px 12px!important;font-weight:700!important}
[data-testid="stFileUploaderDropzone"]{padding:.35rem .7rem!important;min-height:48px!important}
.ref-panel{background:linear-gradient(120deg,#F5F2EA,#fcf7eb);border:1px solid #e9dfce;border-radius:14px;padding:12px 14px;box-shadow:0 2px 7px #201b1110}
.ref-panel h3{font-size:18px;font-weight:750;margin:0 0 10px}
.status-pill{float:right;background:#f3e5bf;border-radius:18px;padding:5px 11px;font-size:12px;color:#24543c}
.st-key-risk-overview-panel,[class*="st-key-risk-overview-panel"]{border-radius:14px!important}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#e8e0d2!important;border-radius:14px!important;background:#F5F2EA!important}
[data-testid="stVerticalBlockBorderWrapper"]>div{border-color:#e8e0d2!important;border-radius:14px!important;padding:12px!important}
.st-key-evidence_type [data-testid="stWidgetLabel"]{display:none!important;height:0!important;margin:0!important}.st-key-evidence_type [data-testid="stRadioGroup"]{display:grid!important;grid-template-columns:repeat(6,minmax(0,1fr))!important;gap:5px!important;align-items:stretch!important}.st-key-evidence_type label[data-testid="stRadioOption"]{position:relative;display:flex!important;align-items:center;justify-content:center;height:62px;min-height:62px;border:1px solid #e9e1d2;border-radius:8px;background:#FFFCF5;padding:5px 3px!important;font-size:11px!important;font-weight:700!important;white-space:normal!important;text-align:center}.st-key-evidence_type [data-testid="stRadioOption"] input{position:absolute!important;opacity:0!important;width:1px!important;height:1px!important}.st-key-evidence_type [data-testid="stRadioOption"]>div:last-child{display:flex!important;align-items:center;justify-content:center;width:100%;height:100%}.st-key-evidence_type [data-testid="stRadioOption"]>div:last-child>div:first-child{display:none!important}.st-key-evidence_type [data-testid="stRadioOption"]:has(input:checked){background:#142923;color:#C6A76A;border-color:#C6A76A;box-shadow:0 2px 0 #C6A76A}
.st-key-intake-message-upload [data-testid="stVerticalBlockBorderWrapper"]>div{padding:10px!important;min-height:140px}
.st-key-intake-evidence-panel [data-testid="stVerticalBlock"]{gap:.05rem!important}.st-key-intake-case-details [data-testid="stVerticalBlockBorderWrapper"]>div{padding:8px!important}
.st-key-settings-system [data-testid="stMetricValue"]{font-size:19px!important}.st-key-settings-system [data-testid="stMetricLabel"]{font-size:11px!important}
.ref-table{font-size:11px!important}
.ref-table td{white-space:nowrap}
.ref-table{width:100%;border-collapse:collapse;font-size:12px}.ref-table th{text-align:left;padding:8px;background:#f6f0e4}.ref-table td{padding:8px 7px;border-bottom:1px solid #eee6d8}
.agent-card{border:1px solid #e6d9c5;border-radius:12px;background:#fffaf0;text-align:center;padding:8px 4px;font-size:12px;font-weight:700;height:91px}
.agent-icon{font-size:24px;display:block;margin:0 auto 5px;color:#C6A76A}
.feature-card{border:1px solid #eee2cf;border-radius:10px;background:#fff9ef;padding:9px;text-align:center;min-height:76px;font-size:12px;font-weight:700}
.about-layout{display:grid;grid-template-rows:126px 154px 274px 210px 16px;gap:8px;color:#17231E}
.about-hero{height:126px;background-position:center;background-size:100% 100%;border-radius:15px;overflow:hidden}
.about-row{display:grid;gap:12px;min-width:0;min-height:0}
.about-top{grid-template-columns:.78fr 1.62fr}.about-middle{grid-template-columns:1.42fr 1fr}.about-bottom{grid-template-columns:1fr 1.1fr 1fr}
.about-card{height:100%;min-width:0;min-height:0;box-sizing:border-box;background:#FFFCF5;border:1px solid #E8E0D2;border-radius:13px;padding:11px 13px;box-shadow:0 2px 6px #392d150e;overflow:hidden}
.about-card h3{font-size:20px!important;line-height:1.1!important;padding:0!important;margin:0 0 11px!important;font-weight:750}
.about-objective p{font-size:15px;line-height:1.4;margin:0;color:#17231E}
.about-features-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.about-feature{height:90px;box-sizing:border-box;border:1px solid #eee2cf;border-radius:10px;background:#fff9ef;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:6px 5px;text-align:center;font-size:13px;line-height:1.2;font-weight:700}
.about-feature .ico{font-size:27px;line-height:1;color:#C6A76A;margin-bottom:7px}
.about-architecture{display:grid;grid-template-columns:.82fr 24px 1.55fr 24px .9fr;gap:5px;height:210px;align-items:center}
.about-architecture h4{font-size:13px;line-height:1.1;margin:0 0 9px;color:#17231E}
.about-inputs,.about-outputs{font-size:13px;line-height:1.65}
.about-arrow{font-size:24px;text-align:center;color:#142923;font-weight:800}
.about-architecture>div:first-child,.about-architecture>div:last-child{background:#fff9ef;border:1px solid #eee2cf;border-radius:10px;padding:9px;height:188px;box-sizing:border-box}
.about-architecture>div:first-child h4,.about-architecture>div:last-child h4{text-align:center}
.about-architecture .about-system{position:relative;border:1px dashed #78a286;border-radius:10px;padding:15px 8px 8px;height:205px;box-sizing:border-box;background:#fbfaf3}
.about-system-title{position:absolute;top:10px;left:50%;transform:translateX(-50%);background:#142923;color:#fff;border-radius:8px;padding:6px 16px;line-height:1.1;font-size:12px;font-weight:750;white-space:nowrap}
.about-agent-grid{position:absolute;top:54px;left:8px;right:8px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px}
.about-agent{height:48px;border:1px solid #eee2cf;border-radius:9px;background:#fff9ef;display:flex;align-items:center;justify-content:center;text-align:center;font-size:12px;line-height:1.1;font-weight:700;padding:3px}
.about-orchestration{position:absolute;left:8px;right:8px;bottom:8px;height:40px;border-radius:8px;background:#f6ead1;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:10px;font-weight:750;line-height:1.1}
.about-orchestration small{font-size:9px;font-weight:500}
.about-role{display:grid;grid-template-columns:22px 112px minmax(0,1fr);gap:5px;align-items:center;min-height:32px;border-bottom:1px solid #eee5d7;font-size:12px;line-height:1.15}
.about-role:last-child{border-bottom:0}.about-role b{font-size:12px}.about-role small{font-size:11px;color:#66716A;line-height:1.15}
.about-tech-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}
.about-tech{height:39px;background:#fff9ef;border:1px solid #eee2cf;border-radius:8px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:12px;font-weight:650}
.about-list{font-size:12px;line-height:1.45;margin:0}.about-list div{margin:0 0 4px}
.about-info{display:grid;grid-template-columns:92px minmax(0,1fr);column-gap:7px;row-gap:8px;font-size:12px;line-height:1.2}
.about-footer{font-size:9px;line-height:16px;color:#66716A;white-space:nowrap}
.analytics-banner{background:linear-gradient(105deg,#142923,#142923);border-radius:13px;padding:9px 12px;color:#fff;display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 16px;height:96px}
.analytics-banner h2{color:#C6A76A!important;font-size:19px!important;margin:0 0 3px!important}.analytics-banner p{color:#eff4ee;margin:0;font-size:11px}
.analytics-metrics{display:flex;gap:6px;align-items:stretch}.analytics-metric{min-width:100px;background:#fffaf0;color:#17231E;border:1px solid #ead8b8;border-radius:10px;padding:7px 9px;text-align:center;display:flex;flex-direction:column;justify-content:center}.analytics-metric b{font-size:19px;color:#C6A76A}.analytics-metric strong{font-size:20px;line-height:1.05}.analytics-metric small{font-size:10px;white-space:nowrap}
.history-heading{display:grid;grid-template-columns:2.6fr 1.25fr 1.2fr 1.2fr .65fr;gap:4px;background:#f6f0e4;padding:8px 5px;border-radius:7px;font-size:11px;white-space:nowrap}.history-heading b:last-child{text-align:right}
.history-case-cell{display:flex;align-items:center;gap:10px;min-height:60px}.history-case-icon{width:44px;height:44px;flex:0 0 44px;border-radius:50%;background:#f7ecd7;display:grid;place-items:center;font-size:24px}.history-case-copy{min-width:0;line-height:1.22}.history-case-copy b{display:block;font-size:12px}.history-case-copy small{display:block;color:#66716A;font-size:10px;margin-top:3px}
.history-meta{display:flex;align-items:center;gap:10px;min-height:50px;border-bottom:1px solid #eee5d7;font-size:11px}.history-meta>div{flex:1;min-width:0;overflow-wrap:anywhere}.history-meta b{display:block;font-size:11px}.history-meta small{color:#66716A;font-size:10px}
.history-overview{display:grid;grid-template-columns:1.08fr .92fr;gap:10px;margin-top:8px}.history-risk-card,.history-final-card{border:1px solid #eee2cf;border-radius:10px;background:#fffaf1;padding:10px;min-height:136px;box-sizing:border-box}.history-risk-body{display:grid;grid-template-columns:102px 1fr;gap:10px;align-items:center}.history-gauge{width:92px;height:92px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(#d94b49 var(--risk),#f0e9dc 0);position:relative}.history-gauge:before{content:"";position:absolute;inset:9px;border-radius:50%;background:#fffaf1}.history-gauge span{position:relative;text-align:center;font-size:20px;font-weight:800;line-height:1.05}.history-gauge small{display:block;font-size:9px;font-weight:650}.history-fact{padding:4px 0;border-bottom:1px solid #eee5d7;font-size:10px}.history-findings{border:1px solid #dce8d9;border-radius:10px;background:#f4f8f0;padding:10px 12px;margin-top:8px;font-size:11px;line-height:1.5}.history-findings div{margin-top:3px}.history-warning{border:1px solid #eddfbf;border-radius:10px;background:#fbf4e3;padding:9px 12px;margin-top:8px;font-size:10px;color:#6f5820}
.st-key-case-history-table-panel button[title="Preview case"]{min-width:38px!important;padding:0!important;color:#17231E!important;font-size:16px!important}
.risk-pill,.state-pill{display:inline-block;white-space:nowrap;border-radius:999px;padding:5px 8px;font-size:10px;font-weight:700;background:#f3ead3;color:#705618}.risk-high_concern{background:#f8dfdc;color:#9f302d}.risk-caution{background:#faedcf;color:#85600e}.risk-low_concern{background:#e5f1e4;color:#1d6646}.risk-insufficient_evidence{background:#e9eceb;color:#53625a}.state-pill{background:#e4f1e5;color:#216749}
.role-row{display:grid;grid-template-columns:24px 145px 1fr;gap:7px;align-items:center;padding:7px 3px;border-bottom:1px solid #eee5d7;font-size:11px}.role-row small{font-size:10px;color:#66716a}.settings-agent{padding:2px 0;font-size:11px}.settings-agent small{color:#66716a}
.settings-agent-list{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}.settings-agent-chip{background:#f4f6ef;border:1px solid #dfe8d8;border-radius:7px;padding:4px 6px;font-size:10px;line-height:1.15}.settings-agent-chip small{display:block;color:#66716a;font-size:9px;margin-top:2px}.sys-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.sys-card{border:1px solid #eee2cf;border-radius:8px;background:#fffaf0;padding:8px;text-align:center}.sys-card small{display:block;color:#66716a;font-size:10px}.sys-card b{font-size:14px}
.settings-info-note,.settings-credentials-note{margin-top:16px;font-size:10px;line-height:1.25;color:#66716A}
.mapping-table{border-collapse:collapse;width:100%;font-size:9px}.performance-table{border-collapse:collapse;width:100%;font-size:10px}.performance-table th{background:#f6f0e4;text-align:left;padding:5px 4px}.performance-table td{border-bottom:1px solid #eee5d7;padding:2px 4px;line-height:1.1}.performance-table td:nth-child(n+2){text-align:center}.performance-table .not-run{color:#7a827c;font-style:italic}.mapping-table th,.mapping-table td{padding:3px 2px;line-height:1.1;text-align:center;border-bottom:1px solid #eee5d7}.mapping-table th:first-child,.mapping-table td:first-child{text-align:left;font-size:10px}.mapping-table .matched{background:#e9f3e6;color:#08734d;font-weight:800}.mapping-table .unmatched{color:#b9bdb6}
.assessment-row{display:grid;grid-template-columns:1.75fr 1.05fr .5fr .6fr;gap:6px;align-items:center;padding:5px 5px;border-bottom:1px solid #eee4d4;font-size:10px}.assessment-row strong{font-size:11px}.assessment-risk{font-weight:750;border-radius:12px;padding:3px 7px;background:#f5ead1;text-align:center}.assessment-risk.high{background:#f8dfdc;color:#9f302d}.assessment-risk.caution{background:#faedcf;color:#85600e}.assessment-risk.low{background:#e5f1e4;color:#1d6646}.assessment-reason{font-size:9px;color:#66716a;grid-column:1/-1;margin-top:-2px}
.tracker-banner{background:linear-gradient(105deg,#142923,#142923);color:#fff;border-radius:12px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;margin:6px 0 12px}.tracker-banner strong{color:#C6A76A;font-size:19px}.tracker-banner span{font-size:12px}.tracker-stage{min-height:166px;border:1px solid #e4dac8;border-radius:12px;background:#fffaf0;padding:11px 9px;display:flex;flex-direction:column;gap:9px;box-shadow:0 2px 5px #21170b0b}.tracker-stage.observed{border-top:4px solid #08734d}.tracker-stage.missing{border-top:4px solid #c6a76a}.tracker-stage small{color:#8b7443;font-weight:700;font-size:9px}.tracker-stage b{font-size:14px;line-height:1.2}.tracker-stage span{font-size:11px;font-weight:700;color:#176545}.tracker-stage p{font-size:10px;color:#66716a;margin:0}.tracker-stage em{font-size:9px;color:#66716a;font-style:normal;overflow-wrap:anywhere}.report-summary{border-radius:12px;background:linear-gradient(100deg,#142923,#142923);padding:16px;color:#fff;display:flex;justify-content:space-between;align-items:center;margin:12px 0 18px}.report-summary b{color:#C6A76A;font-size:18px}.report-summary span{font-size:13px}
.tracker-banner-copy{display:flex;flex-direction:column;gap:3px}.tracker-disclaimer{font-size:9px;line-height:1.2;color:#e2e8e1}
.flow-row{display:flex;align-items:center;justify-content:space-around;gap:3px;margin:12px 0 7px}.flow-stage{flex:1;text-align:center;background:#f0f4eb;border-radius:9px;padding:8px 3px}.flow-stage b{display:block;font-size:19px;color:#142923}.flow-stage small{font-size:10px}.flow-arrow{color:#C6A76A;font-size:18px;font-weight:bold}
.impact-row{display:flex;align-items:center;justify-content:space-between;padding:8px 2px;border-bottom:1px solid #eee5d7;font-size:12px}.impact-row b{font-size:19px;color:#142923}
.st-key-analytics-distribution [data-testid="stVerticalBlock"],.st-key-analytics-agent-performance [data-testid="stVerticalBlock"],.st-key-analytics-outcomes [data-testid="stVerticalBlock"],.st-key-analytics-mapping [data-testid="stVerticalBlock"],.st-key-analytics-common-findings [data-testid="stVerticalBlock"],.st-key-analytics-correlation [data-testid="stVerticalBlock"],.st-key-analytics-trend [data-testid="stVerticalBlock"],.st-key-analytics-impact [data-testid="stVerticalBlock"],.st-key-analytics-insights [data-testid="stVerticalBlock"]{gap:.18rem!important}
.st-key-settings-application [data-testid="stVerticalBlock"],.st-key-settings-security [data-testid="stVerticalBlock"],.st-key-settings-ai [data-testid="stVerticalBlock"],.st-key-settings-storage [data-testid="stVerticalBlock"],.st-key-settings-system [data-testid="stVerticalBlock"]{gap:.08rem!important}
.st-key-settings-application [data-testid="stHorizontalBlock"],.st-key-settings-security [data-testid="stHorizontalBlock"],.st-key-settings-ai [data-testid="stHorizontalBlock"]{min-height:44px!important}
[data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"]:has(.metric){margin-bottom:0!important}
.st-key-risk-overview-panel,.st-key-journey-stages-panel{margin-top:25px!important}
.st-key-risk-overview-panel [data-testid="stPlotlyChart"],.st-key-journey-stages-panel [data-testid="stPlotlyChart"]{height:162px!important}
.st-key-recent-cases-panel,.st-key-agent-status-panel{margin-top:13px!important}
.st-key-recent-cases-panel .ref-table th{padding:6px 7px!important}.st-key-recent-cases-panel .ref-table td{padding:6px 7px!important}
.agent-status-heading{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 0 8px;min-height:25px}
.agent-status-heading h3{margin:0!important;font-size:16px!important;line-height:1.2!important}
.agent-status-heading .status-pill{float:none!important;margin:0!important;padding:4px 7px!important;font-size:9px!important;white-space:nowrap}
.agent-status-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.agent-card{height:70px!important;min-height:70px!important;box-sizing:border-box!important;overflow:hidden!important;border:1px solid #e6d9c5;border-radius:9px;background:#fffaf0;padding:6px 4px!important;text-align:center!important;font-size:10px!important;font-weight:700;line-height:1.08!important;white-space:normal!important}
.agent-card .agent-icon{display:block!important;height:22px!important;margin:0 auto 3px!important;font-size:19px!important;line-height:22px!important;color:#C6A76A}
.agent-card small{display:block!important;margin-top:3px!important;max-width:100%!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important;font-size:8px!important;color:#66716A!important;font-weight:650}
.st-key-agent-status-panel [data-testid="stVerticalBlockBorderWrapper"]>div{min-height:198px!important;box-sizing:border-box!important;padding:9px 10px!important}
.stMarkdownContainer:has(.investigation-hero-reference){margin-bottom:0!important}
.st-key-intake-evidence-panel,.st-key-intake-guidelines-panel{margin-top:4px!important}
.st-key-intake-evidence-panel [data-testid="stVerticalBlockBorderWrapper"]>div{padding:8px!important}
.st-key-intake-case-details [data-testid="stVerticalBlockBorderWrapper"]>div{padding:6px!important}
.st-key-case-history-table-panel [data-testid="stHorizontalBlock"]{min-height:62px!important;border-bottom:1px solid #eee5d7;padding:3px 0;box-sizing:border-box}
.st-key-case-history-table-panel .history-heading{min-height:34px!important}
.st-key-case-history-table-panel .ref-table th{padding:6px 7px!important}.st-key-case-history-table-panel .ref-table td{padding:6px 7px!important}
.st-key-case-preview-panel .history-meta{gap:6px}
.st-key-analytics-distribution [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-agent-performance [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-outcomes [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-mapping [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-common-findings [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-correlation [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-trend [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-impact [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-insights [data-testid="stVerticalBlockBorderWrapper"]>div{padding:9px!important}
.st-key-analytics-outcomes .stCaption{display:none!important}
.st-key-analytics-outcomes [data-testid="stVerticalBlockBorderWrapper"]>div{overflow:visible!important;padding:8px!important}
.st-key-analytics-outcomes [data-testid="stPlotlyChart"]{width:100%!important;height:128px!important;overflow:visible!important}
.st-key-analytics-outcomes [data-testid="stPlotlyChart"]>div,.st-key-analytics-outcomes [data-testid="stPlotlyChart"] .plot-container{width:100%!important;height:128px!important}
.st-key-analytics-trend{margin-top:10px!important}
.st-key-analytics-trend [data-testid="stPlotlyChart"]{height:118px!important}
.supported-evidence-list{display:flex;flex-direction:column}
.supported-evidence-item{height:52px;box-sizing:border-box;border-bottom:1px solid #eee5d7;display:flex;align-items:center;gap:13px;padding:4px 3px}
.supported-evidence-item:last-child{border-bottom:0}.supported-evidence-item>span{width:34px;text-align:center;font-size:22px;color:#B27B1A}.supported-evidence-item b{display:block;font-size:12px;line-height:1.15}.supported-evidence-item small{display:block;color:#66716A;font-size:10px;line-height:1.15;margin-top:2px}
.insights-title{background:#142923;color:#fff;padding:6px 9px;border-radius:8px;margin:0 0 5px;font-size:13px;font-weight:750;line-height:1.15;box-sizing:border-box}
.dist-layout,.outcome-layout{display:grid;grid-template-columns:142px minmax(0,1fr);gap:7px;align-items:center}
.dist-list,.outcome-list{display:flex;flex-direction:column;gap:3px}.dist-row,.outcome-row{display:grid;grid-template-columns:17px minmax(0,1fr) auto;align-items:center;gap:5px;min-height:20px;font-size:10px;line-height:1.1}.dist-row i,.outcome-row i{width:10px;height:10px;border-radius:50%;display:inline-block}.dist-row b,.outcome-row b{font-size:10px;white-space:nowrap}
.agent-perf-list{display:flex;flex-direction:column;gap:1px}.agent-perf-row{display:grid;grid-template-columns:112px minmax(0,1fr) 38px;gap:6px;align-items:center;min-height:20px;font-size:10px;line-height:1.05;border-bottom:1px solid #eee5d7;padding-bottom:1px}.agent-perf-row b{font-size:10px;line-height:1.05;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.agent-perf-row small{display:block;color:#66716A;font-size:8px;line-height:1.05;white-space:nowrap}.agent-perf-row strong{font-size:10px;text-align:right}.agent-conf-track{height:7px;background:#e1eadc;border-radius:9px;overflow:hidden}.agent-conf-track span{display:block;height:100%;background:linear-gradient(90deg,#178753,#07543a);border-radius:9px}
.analytics-key-insights{font-size:9px;line-height:1.18}.analytics-key-insights div{margin:0 0 3px;display:flex;align-items:flex-start;gap:4px}.analytics-key-insights i{color:#178753;font-style:normal;font-weight:800;flex:0 0 auto}.analytics-key-insights span{display:block}
.st-key-analytics-trend [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-impact [data-testid="stVerticalBlockBorderWrapper"]>div,.st-key-analytics-insights [data-testid="stVerticalBlockBorderWrapper"]>div{min-height:168px!important}
.st-key-analytics-insights [data-testid="stVerticalBlockBorderWrapper"]>div{height:168px!important;overflow:hidden!important;box-sizing:border-box!important}
[data-testid="stTabs"]:has(button[aria-label*="Evidence & Agent Analysis"]) [data-baseweb="tab-list"]{display:flex!important;background:#fffaf1!important;border:1px solid #e8dfcf!important;border-radius:13px!important;padding:4px!important;gap:4px!important}
[data-testid="stTabs"]:has(button[aria-label*="Evidence & Agent Analysis"]) [data-baseweb="tab"]{flex:1!important;justify-content:center!important;border-radius:9px!important;min-height:38px!important}
[data-testid="stTabs"]:has(button[aria-label*="Evidence & Agent Analysis"]) [data-baseweb="tab"][aria-selected="true"]{background:#142923!important;color:#fff!important;box-shadow:inset 0 -2px 0 #C6A76A!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"]){width:44px!important;min-width:44px!important;height:26px!important;display:inline-flex!important;align-items:center!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"])>div:first-of-type{position:relative!important;width:42px!important;min-width:42px!important;height:24px!important;box-sizing:border-box!important;border-radius:99px!important;background:#C9CDC9!important;border:1px solid #b9c0ba!important;box-shadow:none!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"])>div:first-of-type>div{position:absolute!important;left:2px!important;right:auto!important;top:2px!important;width:18px!important;height:18px!important;border-radius:50%!important;background:#fff!important;border:1px solid #e6e8e5!important;box-shadow:0 1px 2px #0002!important;transform:none!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"]:checked)>div:first-of-type{background:#168A50!important;border-color:#168A50!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"]:checked)>div:first-of-type>div{left:auto!important;right:2px!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"]:disabled)>div:first-of-type{background:#e0e2df!important;border-color:#d2d6d2!important}
[data-testid="stMainBlockContainer"] label:has(input[role="switch"]:focus-visible)>div:first-of-type{outline:2px solid #C6A76A!important;outline-offset:2px!important}
.st-key-settings-application [data-testid="stCheckbox"],.st-key-settings-security [data-testid="stCheckbox"],.st-key-settings-ai [data-testid="stCheckbox"]{width:100%!important;display:flex!important;justify-content:flex-end!important}
.st-key-settings-application .stElementContainer:has([data-testid="stCheckbox"]),.st-key-settings-security .stElementContainer:has([data-testid="stCheckbox"]),.st-key-settings-ai .stElementContainer:has([data-testid="stCheckbox"]){margin-left:auto!important}

@media(max-width:900px){[data-testid="stSidebar"]{min-width:220px!important;width:220px!important}.block-container{padding-left:1rem;padding-right:1rem}}
@media(max-width:1200px){
.analytics-banner{height:82px!important;padding:7px 9px!important}
.analytics-metric{min-width:82px!important;padding:5px 6px!important}
.analytics-metric strong{font-size:17px!important}
.analytics-metric small{font-size:9px!important}
.analytics-metrics{gap:4px!important}
.agent-perf-row{grid-template-columns:96px minmax(0,1fr) 32px!important}
.mapping-table{font-size:8px!important}
.mapping-table th:first-child,.mapping-table td:first-child{font-size:9px!important}
.sidebar-phone{display:none!important}
}
@media(max-width:760px){
.block-container{padding-left:.55rem!important;padding-right:.55rem!important}
[data-testid="stSidebar"]{min-width:72px!important;width:72px!important}
.brand img{width:72px!important;object-fit:contain!important}
[data-testid="stSidebar"] div.stButton>button{font-size:0!important;padding:0!important;text-align:center!important}
[data-testid="stSidebar"] div.stButton>button p{font-size:18px!important}
.analytics-banner{align-items:flex-start!important;height:auto!important;min-height:82px!important}
.analytics-banner p{display:none!important}
.analytics-metrics{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important}
.analytics-metric{min-width:0!important}
.analytics-metric:nth-child(n+4){display:none!important}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>"""
st.markdown(CSS,unsafe_allow_html=True)
if "page" not in st.session_state:
    initial_page=database.get_setting("default_view","Dashboard")
    st.session_state.page=initial_page if initial_page in PAGES else "Dashboard"
if "selected_case" not in st.session_state: st.session_state.selected_case=None
if "evidence_drafts" not in st.session_state:
    try:
        st.session_state.evidence_drafts=json.loads(database.get_setting("evidence_drafts","{}") or "{}")
    except (TypeError,ValueError):
        st.session_state.evidence_drafts={}
    for saved_draft in st.session_state.evidence_drafts.values():
        for key in ("call_date","payment_time"):
            if isinstance(saved_draft.get(key),str):
                try: saved_draft[key]=date.fromisoformat(saved_draft[key])
                except ValueError: saved_draft.pop(key,None)
        for key in ("call_time","payment_clock"):
            if isinstance(saved_draft.get(key),str):
                try: saved_draft[key]=time.fromisoformat(saved_draft[key])
                except ValueError: saved_draft.pop(key,None)

def cases(): return database.list_cases()
def risk(c): return (c.get("assessment") or {}).get("risk_level","INSUFFICIENT_EVIDENCE")
def card(title,body): st.markdown(f'<div class="panel"><h3>{title}</h3>{body}</div>',unsafe_allow_html=True)
def image_uri(name):
    path=Path(__file__).parent/"assets"/"reference-crops"/name
    return "data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode("ascii")
def run(case_id):
    mode="Groq online agents with local fallback" if llm_config["provider"]=="groq" else "labeled local deterministic fallback"
    with st.spinner(f"Running LangGraph investigation ({mode})…"):
        result=run_investigation(case_id)
    st.session_state.selected_case=case_id
    st.session_state.page="Case History"
    st.rerun()
def create_scenario(item):
    cid=database.create_case(item['title'],item['summary'],True,item['events']); return cid
def go_case(cid): st.session_state.selected_case=cid; st.session_state.page="Case History"

EVIDENCE_TYPES={
    "Messages / Chat":{"slug":"message","fields":["message_text","upload"]},
    "Call Summary":{"slug":"call","fields":["call_date","call_time","participants","call_summary","upload"]},
    "URL / Link":{"slug":"url","fields":["url_value","url_context"]},
    "QR Code":{"slug":"qr","fields":["qr_payload","upload"]},
    "Payment / UPI":{"slug":"payment","fields":["payment_amount","payment_time","upi_id","payment_reference","payment_status","payment_description","payment_clock"]},
    "Files / Screenshots":{"slug":"file","fields":["file_description","upload"]},
}
ALLOWED_UPLOAD_EXTENSIONS={".txt",".csv",".png",".jpg",".jpeg",".webp"}
MAX_UPLOAD_BYTES=10*1024*1024
MAX_EVENT_TEXT=5000
MAX_CASE_EVENTS=50

def _evidence_widget_key(evidence_type,field):
    slug=EVIDENCE_TYPES[evidence_type]['slug']
    if field=="upload":
        epoch=st.session_state.setdefault("upload_widget_epoch",{}).get(slug,0)
        return f"intake_{slug}_{field}_{epoch}"
    return f"intake_{slug}_{field}"

def _persist_evidence_drafts():
    persistent={name:{key:value for key,value in item.items() if key!="upload"}
                for name,item in st.session_state.get("evidence_drafts",{}).items()}
    neutral_defaults={"payment_status":"Request received","call_time":time(12,0),"payment_clock":time(12,0)}
    persistent={name:item for name,item in persistent.items()
                if any(value not in (None,"") and neutral_defaults.get(key)!=value for key,value in item.items())}
    if persistent:
        database.set_setting("evidence_drafts",json.dumps(persistent,default=lambda value:value.isoformat() if hasattr(value,"isoformat") else str(value)))
    else:
        database.delete_setting("evidence_drafts")

def _save_evidence_draft(evidence_type=None):
    evidence_type=evidence_type or st.session_state.get("active_evidence_type","Messages / Chat")
    config=EVIDENCE_TYPES.get(evidence_type)
    if not config: return
    drafts=st.session_state.setdefault("evidence_drafts",{})
    draft=drafts.setdefault(evidence_type,{})
    for field in config["fields"]:
        value=st.session_state.get(_evidence_widget_key(evidence_type,field))
        if field=="upload" and value is not None:
            try: draft[field]={"filename":value.name,"mime_type":value.type or "application/octet-stream","data":value.getvalue()}
            except Exception: pass
        elif field!="upload" and value is not None:
            draft[field]=value
    auto_save=str(database.get_setting("auto_save","true")).lower() in {"1","true","yes","on"}
    if auto_save:
        # Only serializable text/date values are persisted here. Uploaded binary
        # files remain in the active browser session until explicitly added.
        _persist_evidence_drafts()

def _evidence_type_changed():
    previous=st.session_state.get("active_evidence_type","Messages / Chat")
    _save_evidence_draft(previous)
    st.session_state.active_evidence_type=st.session_state.get("evidence_type",previous)

def _save_default_view_setting():
    database.set_setting("default_view",st.session_state.setting_default_view)

def _save_auto_save_setting():
    enabled=bool(st.session_state.setting_auto_save)
    database.set_setting("auto_save",str(enabled).lower())
    if enabled:
        _persist_evidence_drafts()
    else:
        database.delete_setting("evidence_drafts")

def _save_small_model_setting():
    database.set_setting("use_small_model",str(bool(st.session_state.setting_use_small_model)).lower())
    st.cache_data.clear()

def _clear_all_intake():
    case_id=st.session_state.get("draft_case")
    if case_id: database.delete_case(case_id)
    st.session_state.draft_case=None
    st.session_state.evidence_drafts={}
    database.delete_setting("evidence_drafts")
    st.session_state.pending_intake_reset="all"

def _prepare_intake_reset():
    pending=st.session_state.pop("pending_intake_reset",None)
    if not pending: return
    for evidence_type,config in EVIDENCE_TYPES.items():
        if pending!="all" and evidence_type!=pending: continue
        for field in config["fields"]:
            key=_evidence_widget_key(evidence_type,field)
            if field=="upload":
                # Streamlit file_uploader widget keys are read-only after use.
                # Rotate the key to mount an empty uploader on the next run.
                epochs=st.session_state.setdefault("upload_widget_epoch",{})
                slug=config["slug"]
                epochs[slug]=epochs.get(slug,0)+1
            else:
                st.session_state.pop(key,None)
    if pending=="all":
        for key in ("case_title","case_incident_date","case_summary","evidence_type"):
            st.session_state.pop(key,None)
        st.session_state.active_evidence_type="Messages / Chat"
    else:
        st.session_state.evidence_drafts[pending]={}
    if str(database.get_setting("auto_save","true")).lower() in {"1","true","yes","on"}:
        _persist_evidence_drafts()


with st.sidebar:
    st.markdown(f'<div class="brand"><img src="{image_uri("sidebar-brand-blended.png")}" alt="UPI ScamTrace — Multi-Agent Scam Journey Reconstruction"></div>',unsafe_allow_html=True)
    nav_icons={"Dashboard":"⌂","New Investigation":"＋","Case History":"▱","Analytics":"▥","Settings":"⚙","About Project":"ⓘ"}
    for p in PAGES:
        if st.button(f"{nav_icons[p]}　{p}",key="nav_"+p,width="stretch",type="primary" if st.session_state.page==p else "secondary"):
            st.session_state.page=p; st.session_state.selected_case=None; st.rerun()
    st.markdown(f'<div class="sidebar-phone"><img src="{image_uri("sidebar-phone-blended.png")}" alt="UPI safety illustration"></div>',unsafe_allow_html=True)
    provider_label="Groq configured" if llm_config["provider"]=="groq" else "Local fallback ready"
    st.markdown(f'<div class="sidebar-status">◉ Multi-Agent System<br><small>● {provider_label}</small></div>',unsafe_allow_html=True)

page=st.session_state.page
_prepare_intake_reset()
all_cases=cases()

def header(title,sub):
    st.markdown(f'<div class="page-header"><div><h1>{title}</h1><p>{sub}</p></div><div class="profile"><span class="bell" aria-label="Notifications"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"/></svg></span><span style="color:#C6A76A">●</span><span class="avatar" aria-label="User profile"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><span>ScamTrace User　⌄</span></div></div>',unsafe_allow_html=True)

if page=="Dashboard":
    header("Dashboard","Investigate, reconstruct, and prevent UPI fraud using a multi-agent AI system.")
    st.markdown(f'<div class="hero-reference" style="background-image:url({image_uri("dashboard-hero.png")})" role="img" aria-label="UPI ScamTrace journey reconstruction"></div>',unsafe_allow_html=True)
    with st.container(key="dashboard-actions"):
        ba,bb=st.columns([.24,.32],gap="small")
        with ba:
            if st.button("Start New Investigation",key="dashboard_start",help="Start New Investigation"):
                st.session_state.page="New Investigation"; st.rerun()
        with bb:
            if st.button("View Demo",key="dashboard_demo",help="Load synthetic demo scenarios"):
                existing={c['title']:c for c in all_cases}; made=[]; rerun_count=0
                for sc in scenarios():
                    if sc['title'] not in existing:
                        cid=create_scenario(sc); made.append(cid); run_investigation(cid); rerun_count+=1
                    elif not existing[sc['title']].get('assessment'):
                        run_investigation(existing[sc['title']]['id']); rerun_count+=1
                st.success(f"Loaded {len(made)} synthetic cases and ran {rerun_count} LangGraph investigations."); st.rerun()
    all_cases=cases(); counts={level:sum(1 for c in all_cases if risk(c)==level) for level in ["HIGH_CONCERN","CAUTION","LOW_CONCERN","INSUFFICIENT_EVIDENCE"]}
    metrics=[("📁","Total Cases",len(all_cases),"#F8EDD4"),("⚠️","High-Risk Cases",counts["HIGH_CONCERN"],"#FBE5E1"),("⚠","Medium-Risk Cases",counts["CAUTION"],"#FFF0CC"),("🛡️","Low-Risk / Benign",counts["LOW_CONCERN"],"#E6F2E4")]
    cols=st.columns(4,gap="small")
    for col,(icon,label,val,tint) in zip(cols,metrics):
        col.markdown(f'<div class="metric"><span class="mi" style="background:{tint}">{icon}</span><div><b>{val}</b><small>{label}</small></div></div>',unsafe_allow_html=True)
    l,r=st.columns([.93,1.07],gap="small")
    with l:
        with st.container(border=True,key="risk-overview-panel"):
            ra,rb=st.columns([1,.55],vertical_alignment="center")
            with ra: st.markdown("### Scam Risk Overview")
            with rb: period=st.selectbox("Period",["All Cases","Last 30 Days"],index=1,label_visibility="collapsed",key="dash_period")
            selected_cases=all_cases
            if period=="Last 30 Days":
                cutoff=datetime.now(timezone.utc).timestamp()-30*86400
                selected_cases=[c for c in all_cases if c.get('created_at') and datetime.fromisoformat(c['created_at']).timestamp()>=cutoff]
            rc={level:sum(risk(c)==level for c in selected_cases) for level in ["HIGH_CONCERN","CAUTION","LOW_CONCERN","INSUFFICIENT_EVIDENCE"]}
            if selected_cases:
                total=len(selected_cases); high_pct=100*rc['HIGH_CONCERN']/total
                df=pd.DataFrame({"Risk":["High Risk","Medium Risk","Low Risk / Benign","Insufficient Evidence"],"Cases":[rc['HIGH_CONCERN'],rc['CAUTION'],rc['LOW_CONCERN'],rc['INSUFFICIENT_EVIDENCE']]})
                fig=px.pie(df,names="Risk",values="Cases",hole=.60,color="Risk",color_discrete_map={"High Risk":"#e23d3e","Medium Risk":"#f2ad16","Low Risk / Benign":"#1a9e60","Insufficient Evidence":"#b6b8ae"})
                fig.update_layout(height=162,margin=dict(l=0,r=4,t=0,b=0),showlegend=True,legend=dict(orientation="v",x=1.0,y=.5,font=dict(size=11,color="#17231E")),font=dict(size=11,color="#17231E"),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",annotations=[dict(text=f"{high_pct:.1f}%<br><sup>High Risk</sup>",x=.5,y=.5,showarrow=False,font=dict(size=22,color="#17231E"))])
                st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=162)
            else: st.info("No cases in this period.")
    with r:
        with st.container(border=True,key="journey-stages-panel"):
            st.markdown("### Scam Journey Stages Detected")
            stage_codes={"Initial Contact":("impersonation","urgency","credential_request"),"Trust Building":("impersonation",),"Link / App Induction":("external_link",),"Payment Request":("payment_direction_unclear","repeated_payment_request"),"Repeat / Escalation":("repeated_payment_request","credential_request")}
            stage_shares=[]
            for codes_for_stage in stage_codes.values():
                present=sum(any(i.get('code') in codes_for_stage for f in (c.get('findings') or []) for i in f.get('indicators',[])) for c in all_cases)
                stage_shares.append(100*present/max(1,len(all_cases)))
            stage_fig=px.bar(x=list(stage_codes),y=stage_shares,text=[f"{x:.0f}%" for x in stage_shares],labels={"x":"","y":"Cases"},color_discrete_sequence=["#056443"])
            stage_fig.update_traces(textposition="outside",cliponaxis=False)
            stage_fig.update_layout(height=162,margin=dict(l=10,r=8,t=8,b=18),font=dict(size=10,color="#17231E"),showlegend=False,xaxis_tickangle=0,xaxis=dict(showgrid=False,tickfont=dict(color="#17231E")),yaxis=dict(range=[0,100],ticksuffix="%",showgrid=False,tickfont=dict(color="#17231E")),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",bargap=.32)
            st.plotly_chart(stage_fig,width="stretch",config={"displayModeBar":False},height=162)
    recent,agents_panel=st.columns([1,1],gap="small")
    with recent:
        with st.container(border=True,key="recent-cases-panel"):
            titlecol,viewcol=st.columns([4,1]); titlecol.markdown("### Recent Investigations")
            if viewcol.button("View All →",key="view_all_cases"): st.session_state.page="Case History"; st.rerun()
            table='<table class="ref-table"><thead><tr><th>Case ID</th><th>Scenario (Detected)</th><th>Risk Level</th><th>Status</th><th>Updated</th></tr></thead><tbody>'
            recent_cases=all_cases[:3]
            for c in recent_cases:
                updated=(c.get('updated_at') or '')[:16].replace('T',' ')
                table+=f"<tr><td>{c['id']}</td><td>{'🧪 ' if c['synthetic'] else ''}{c['title']}</td><td>{risk(c).replace('_',' ').title()}</td><td>{c['status']}</td><td>{updated}</td></tr>"
            st.markdown(table+'</tbody></table>',unsafe_allow_html=True)
    with agents_panel:
        with st.container(border=True,key="agent-status-panel"):
            analyzed=next((c for c in all_cases if c.get('findings')),None)
            found={f['agent_name']:f for f in ((analyzed or {}).get('findings') or [])}
            active=sum(1 for name in AGENT_NAMES if name in found and found[name].get('status') in ('success','local','fallback'))
            stat=f"{active}/6 with saved findings" if active else "Ready for investigation"
            st.markdown(f'<div class="agent-status-heading"><h3>Multi-Agent System Status</h3><span class="status-pill">● {stat}</span></div>',unsafe_allow_html=True)
            titles=[("💬","Message Agent"),("🔗","Link & QR Agent"),("💳","Payment Agent"),("▦","Timeline Agent"),("♧","Investigator Agent"),("♢","Decision Agent")]
            cards=[]
            for icon,name in titles:
                lookup="Journey Agent" if name=="Investigator Agent" else name
                f=found.get(lookup); label=(f.get('model') or f.get('provider','local')) if f else "Ready"
                cards.append(f'<div class="agent-card"><span class="agent-icon">{icon}</span>{name}<small>{label}</small></div>')
            st.markdown('<div class="agent-status-grid">'+''.join(cards)+'</div>',unsafe_allow_html=True)

elif page=="New Investigation":
    header("New Investigation","Provide the evidence from your UPI interaction to reconstruct the scam journey.")
    st.markdown(f'<div class="investigation-hero-reference" style="background-image:url({image_uri("investigation-hero.png")})" role="img" aria-label="Start a new scam investigation"></div>',unsafe_allow_html=True)
    left,right=st.columns([2.4,1],gap="small");
    with left:
        active_type=st.session_state.get("active_evidence_type","Messages / Chat")
        st.session_state.setdefault("case_incident_date",None)
        st.session_state.setdefault("evidence_type",active_type)
        draft_values=st.session_state.setdefault("evidence_drafts",{}).get(active_type,{})
        labels={"Messages / Chat":"💬 Messages / Chat","Call Summary":"☎ Call Summary","URL / Link":"🔗 URL / Link","QR Code":"▦ QR Code","Payment / UPI":"₹ Payment / UPI","Files / Screenshots":"▧ Files / Screenshots"}
        field_defaults={"message_text":"","call_date":None,"call_time":time(12,0),"participants":"","call_summary":"","url_value":"","url_context":"","qr_payload":"","payment_amount":"","payment_time":None,"upi_id":"","payment_reference":"","payment_status":"Request received","payment_description":"","payment_clock":time(12,0),"file_description":""}
        for field in EVIDENCE_TYPES[active_type]["fields"]:
            if field!="upload": st.session_state.setdefault(_evidence_widget_key(active_type,field),draft_values.get(field,field_defaults.get(field,"")))
        with st.container(border=True,key="intake-evidence-panel"):
            st.markdown("### ▣ Add Evidence")
            st.caption("Provide one or more evidence types related to the suspected UPI interaction.")
            typ=st.radio("Evidence type",list(EVIDENCE_TYPES),horizontal=True,label_visibility="collapsed",format_func=lambda x:labels[x],key="evidence_type",on_change=_evidence_type_changed)
            # A changed type triggers a rerun; the selected branch below presents type-specific fields.
            kind={"Messages / Chat":"message","Call Summary":"call_summary","URL / Link":"url","QR Code":"qr_payload","Payment / UPI":"payment_request","Files / Screenshots":"other"}[typ]
            st.markdown(f"### {labels[typ]} Evidence")
            fields={}
            upload_widget=None
            uploaded_bytes=None
            if typ=="Messages / Chat":
                message_col,upload_col=st.columns([1.2,1],gap="small")
                message_col.caption("Paste the suspicious message, conversation, or key excerpts.")
                fields["message_text"]=message_col.text_area("Message / chat text",height=92,max_chars=MAX_EVENT_TEXT,key=_evidence_widget_key(typ,"message_text"),on_change=_save_evidence_draft,placeholder='e.g., “Your KYC will be deactivated today. Click the link to update…”')
                with upload_col.container(border=True,key="intake-message-upload"):
                    st.markdown("#### Upload chat screenshot(s)")
                    st.caption("Drag and drop, or choose files")
                    upload_widget=st.file_uploader("Upload chat screenshot or text export (optional)",type=["txt","csv","png","jpg","jpeg","webp"],key=_evidence_widget_key(typ,"upload"),on_change=_save_evidence_draft,label_visibility="collapsed")
                    st.caption("PNG · JPG · WEBP · TXT · CSV · 10 MB max")
            elif typ=="Call Summary":
                st.caption("Record what the caller claimed and what they asked you to do. Do not include OTPs or passwords.")
                ca,cb,cc=st.columns([1,1,1.35],gap="small")
                fields["call_date"]=ca.date_input("Call date",key=_evidence_widget_key(typ,"call_date"),on_change=_save_evidence_draft)
                fields["call_time"]=cb.time_input("Call time",key=_evidence_widget_key(typ,"call_time"),on_change=_save_evidence_draft)
                fields["participants"]=cc.text_input("Participants (optional)",max_chars=160,key=_evidence_widget_key(typ,"participants"),on_change=_save_evidence_draft,placeholder="Caller / recipient")
                summary_col,upload_col=st.columns([1.2,1],gap="small")
                fields["call_summary"]=summary_col.text_area("Call summary / transcript",height=66,max_chars=MAX_EVENT_TEXT,key=_evidence_widget_key(typ,"call_summary"),on_change=_save_evidence_draft,placeholder="Claims, instructions, channel changes.")
                upload_widget=upload_col.file_uploader("Call notes / transcript (optional)",type=["txt","csv"],key=_evidence_widget_key(typ,"upload"),on_change=_save_evidence_draft)
                upload_col.caption("TXT / CSV · 10 MB max")
            elif typ=="URL / Link":
                st.caption("URLs are parsed locally. ScamTrace does not open or fetch the address.")
                fields["url_value"]=st.text_input("URL / Link",max_chars=2048,key=_evidence_widget_key(typ,"url_value"),on_change=_save_evidence_draft,placeholder="https://example.com/path")
                fields["url_context"]=st.text_area("Where it appeared / surrounding text",height=92,max_chars=MAX_EVENT_TEXT,key=_evidence_widget_key(typ,"url_context"),on_change=_save_evidence_draft,placeholder="Who sent it and what they said about the link")
            elif typ=="QR Code":
                st.caption("QR content is untrusted. Decoding is not enabled here; paste any text shown by a trusted scanner if available.")
                fields["qr_payload"]=st.text_area("QR payload / payment URI (optional)",height=72,max_chars=MAX_EVENT_TEXT,key=_evidence_widget_key(typ,"qr_payload"),on_change=_save_evidence_draft,placeholder="upi://pay?... or other visible payload")
                upload_widget=st.file_uploader("Upload QR image",type=["png","jpg","jpeg","webp"],key=_evidence_widget_key(typ,"upload"),on_change=_save_evidence_draft)
            elif typ=="Payment / UPI":
                pa,pb,pc=st.columns([.8,1.1,1.15],gap="small")
                fields["payment_amount"]=pa.text_input("Amount",max_chars=24,key=_evidence_widget_key(typ,"payment_amount"),on_change=_save_evidence_draft,placeholder="e.g., 500.00")
                fields["upi_id"]=pb.text_input("UPI ID",max_chars=120,key=_evidence_widget_key(typ,"upi_id"),on_change=_save_evidence_draft,placeholder="name@bank")
                fields["payment_status"]=pc.selectbox("Reported status",["Request received","Attempted","Completed (user reported)","Failed","Unknown"],key=_evidence_widget_key(typ,"payment_status"),on_change=_save_evidence_draft,help="Status is supplied by the user and is not independently verified.")
                pd,pe,pf=st.columns([1.2,.9,.9],gap="small")
                fields["payment_reference"]=pd.text_input("Reference ID",max_chars=120,key=_evidence_widget_key(typ,"payment_reference"),on_change=_save_evidence_draft)
                fields["payment_time"]=pe.date_input("Date",key=_evidence_widget_key(typ,"payment_time"),on_change=_save_evidence_draft)
                fields["payment_clock"]=pf.time_input("Time",key=_evidence_widget_key(typ,"payment_clock"),on_change=_save_evidence_draft)
                fields["payment_description"]=st.text_input("Description / context",max_chars=1000,key=_evidence_widget_key(typ,"payment_description"),on_change=_save_evidence_draft,placeholder="What was requested or reported? Never enter PINs or OTPs.")
            else:
                st.caption("Supported files are stored locally. Text and CSV contents can be extracted; OCR is not enabled.")
                fields["file_description"]=st.text_area("File context / manual description",height=70,max_chars=MAX_EVENT_TEXT,key=_evidence_widget_key(typ,"file_description"),on_change=_save_evidence_draft)
                upload_widget=st.file_uploader("Upload evidence file",type=["txt","csv","png","jpg","jpeg","webp"],key=_evidence_widget_key(typ,"upload"),on_change=_save_evidence_draft)
            saved_upload=draft_values.get("upload")
            if typ in ("Messages / Chat","Call Summary","QR Code","Files / Screenshots"):
                if upload_widget is not None:
                    uploaded_bytes=upload_widget.getvalue()
                    filename=upload_widget.name
                    mime_type=upload_widget.type or "application/octet-stream"
                elif saved_upload:
                    filename=saved_upload["filename"]; mime_type=saved_upload["mime_type"]; uploaded_bytes=saved_upload["data"]
                    st.info(f"Previously selected file retained: {filename} · {len(uploaded_bytes):,} bytes")
                if uploaded_bytes and Path(filename).suffix.lower() in {".png",".jpg",".jpeg",".webp"}:
                    try:
                        from PIL import Image
                        image=Image.open(io.BytesIO(uploaded_bytes))
                        if image.width*image.height<=20_000_000: st.image(image,caption=f"Preview · {filename}",width=180)
                        else: st.warning("Image dimensions exceed the 20 megapixel preview limit.")
                    except Exception: st.error("The selected image is malformed and cannot be previewed.")
                if uploaded_bytes: st.caption(f"Selected: {filename} · {len(uploaded_bytes):,} bytes · {mime_type}")
            if str(database.get_setting("auto_save","true")).lower() in {"1","true","yes","on"}:
                st.session_state.evidence_drafts.setdefault(typ,{}).update(fields)
                _persist_evidence_drafts()
            with st.container(border=True,key="intake-case-details"):
                st.markdown("### ▤ Case Details")
                case_title,incident_date=st.columns(2,gap="small")
                title=case_title.text_input("Case Title *",max_chars=160,key="case_title",placeholder="e.g., Fake Refund Scam, KYC Update Scam")
                incident_date_value=incident_date.date_input("Incident Date / Period",key="case_incident_date")
                summary=st.text_input("Additional Context (Optional)",max_chars=1000,key="case_summary",placeholder="Add only relevant context; avoid secrets.")
                draft_case_id=st.session_state.get("draft_case")
                draft_count=len(database.get_case(draft_case_id)["events"]) if draft_case_id and database.get_case(draft_case_id) else 0
                clear_col,add_col,start_col=st.columns([.8,1.1,1.1],gap="small")
                clear_col.button("↻ Clear All",key="clear_all_intake",on_click=_clear_all_intake)
                add=add_col.button(f"Add Evidence{f' · {draft_count} saved' if draft_count else ''}",type="primary",key="add_evidence_to_draft",width="stretch")
                has_unsaved=any(str(value).strip() for field,value in fields.items() if field not in ("payment_status","call_date","call_time","payment_time","payment_clock") and value) or bool(upload_widget)
                start_clicked=start_col.button("Start Investigation →",key="run_draft",type="primary",disabled=not bool(draft_case_id) or has_unsaved,width="stretch",help="Save the current evidence before starting." if has_unsaved else None)
        if add:
            values=fields
            content=""
            event_fields={}
            timestamp=None
            amount_invalid=False
            if typ=="Messages / Chat": content=values.get("message_text","").strip()
            elif typ=="Call Summary":
                content=values.get("call_summary","").strip()
                event_fields={"participants":values.get("participants","").strip()}
                if values.get("call_date"): timestamp=datetime.combine(values["call_date"],values.get("call_time") or time(12,0),tzinfo=timezone.utc).isoformat()
            elif typ=="URL / Link":
                raw_url=values.get("url_value","").strip()
                context=values.get("url_context","").strip()
                if raw_url:
                    candidate=raw_url if "://" in raw_url else "https://"+raw_url
                    parsed=urlsplit(candidate)
                    if parsed.scheme not in ("http","https") or not parsed.hostname: st.error("Enter a valid HTTP or HTTPS URL. The app will not visit it.")
                    else:
                        event_fields={"url":raw_url,"domain":parsed.hostname.lower()}
                        content=f"URL: {raw_url}"+(f"\nContext: {context}" if context else "")
                elif context: content=context
            elif typ=="QR Code":
                payload=values.get("qr_payload","").strip()
                if payload:
                    event_fields={"payload":payload}
                    if payload.lower().startswith("upi://pay?"):
                        parsed_qr=parse_qs(urlsplit(payload).query,keep_blank_values=True)
                        event_fields["upi_fields"]={k:parsed_qr[k][0] for k in ("pa","pn","am","cu","tn") if parsed_qr.get(k)}
                    content="QR payload supplied by user: "+payload
            elif typ=="Payment / UPI":
                amount=values.get("payment_amount","").strip(); upi=values.get("upi_id","").strip(); reference=values.get("payment_reference","").strip(); status=values.get("payment_status","Unknown"); description=values.get("payment_description","").strip()
                if amount:
                    try:
                        parsed_amount=Decimal(amount)
                        if not parsed_amount.is_finite() or parsed_amount<0: raise InvalidOperation
                    except InvalidOperation:
                        st.error("Amount must be a non-negative number."); amount_invalid=True
                event_fields={"amount":amount,"upi_id":upi,"reference_id":reference,"reported_status":status}
                content="User-reported payment information: "+"; ".join(f"{label}: {value}" for label,value in (("Amount",amount),("UPI ID",upi),("Reference ID",reference),("Status",status),("Description",description)) if value)
                kind="payment_attempt" if status in ("Attempted","Completed (user reported)","Failed") else "payment_request"
                if values.get("payment_time"): timestamp=datetime.combine(values["payment_time"],values.get("payment_clock") or time(12,0),tzinfo=timezone.utc).isoformat()
            else:
                content=values.get("file_description","").strip()
            attach_info=None
            upload_invalid=False
            if uploaded_bytes:
                ext=Path(filename).suffix.lower()
                allowed_mimes={".txt":{"text/plain","application/octet-stream"},".csv":{"text/csv","application/vnd.ms-excel","application/octet-stream"},".png":{"image/png"},".jpg":{"image/jpeg"},".jpeg":{"image/jpeg"},".webp":{"image/webp"}}
                if len(uploaded_bytes)>MAX_UPLOAD_BYTES:
                    st.error("File exceeds the 10 MB limit."); upload_invalid=True
                elif ext not in ALLOWED_UPLOAD_EXTENSIONS:
                    st.error("Unsupported file extension."); upload_invalid=True
                elif mime_type not in allowed_mimes.get(ext,set()) and mime_type!="application/octet-stream":
                    st.error("The file type does not match its extension."); upload_invalid=True
                else:
                    if ext in (".txt",".csv"):
                        extracted=uploaded_bytes.decode("utf-8","replace")
                        if len(extracted)>MAX_EVENT_TEXT:
                            st.error("Extracted text exceeds the 5,000 character limit."); upload_invalid=True
                        else: content=(content+"\n"+extracted).strip()
                    elif ext in (".png",".jpg",".jpeg",".webp"):
                        try:
                            from PIL import Image
                            image=Image.open(io.BytesIO(uploaded_bytes)); image.verify()
                            image=Image.open(io.BytesIO(uploaded_bytes))
                            if image.width*image.height>20_000_000:
                                st.error("Image dimensions exceed the 20 megapixel limit."); upload_invalid=True
                        except Exception:
                            st.error("The selected image is malformed."); upload_invalid=True
                    if not upload_invalid:
                        if not content: content=f"User-provided {typ.lower()} attachment: {filename}. Image content was not OCR-decoded."
                        attach_info={"filename":filename,"mime_type":mime_type,"data":uploaded_bytes}
            if typ=="Payment / UPI" and not any(values.get(k) for k in ("payment_amount","upi_id","payment_reference","payment_description","payment_time")):
                st.error("Add at least one payment detail or description; the reported status alone is not evidence.")
            if typ=="Files / Screenshots" and not uploaded_bytes: st.error("Upload a supported file before adding this evidence.")
            if typ=="QR Code" and not uploaded_bytes and not values.get("qr_payload","").strip(): st.error("Enter the visible QR payload or upload the QR image.")
            if typ=="URL / Link" and not values.get("url_value","").strip() and not values.get("url_context","").strip(): st.error("Enter a URL or add relevant context.")
            if not content.strip(): st.error("Add evidence text or upload a supported file before continuing.")
            if len(content)>MAX_EVENT_TEXT: st.error("Evidence text exceeds the 5,000 character limit.")
            if not title.strip(): title="UPI Scam Investigation — "+datetime.now().strftime("%d %b %Y")
            current=database.get_case(st.session_state.get("draft_case")) if st.session_state.get("draft_case") else None
            has_error=bool((typ=="URL / Link" and values.get("url_value","").strip() and not event_fields.get("domain")) or (typ=="Files / Screenshots" and not uploaded_bytes) or (typ=="QR Code" and not uploaded_bytes and not values.get("qr_payload","").strip()) or not content.strip() or len(content)>MAX_EVENT_TEXT or (uploaded_bytes and (len(uploaded_bytes)>MAX_UPLOAD_BYTES or attach_info is None)) or upload_invalid or amount_invalid or (typ=="Payment / UPI" and not any(values.get(k) for k in ("payment_amount","upi_id","payment_reference","payment_description","payment_time"))))
            if not has_error:
                if current and len(current["events"])>=MAX_CASE_EVENTS: st.error(f"A case can contain at most {MAX_CASE_EVENTS} evidence items.")
                else:
                    case_id=st.session_state.get("draft_case") or database.create_case(title.strip(),summary.strip())
                    st.session_state.draft_case=case_id
                    if not current: current=database.get_case(case_id)
                    event_date=incident_date_value
                    if timestamp is None and event_date: timestamp=datetime.combine(event_date,datetime.min.time(),tzinfo=timezone.utc).isoformat()
                    database.add_event(case_id,{"timestamp":timestamp or datetime.now(timezone.utc).isoformat(),"event_type":kind,"channel":typ,"content":content,"source":"uploaded-file" if attach_info else "user-entered","fields":event_fields,"attachment":attach_info})
                    st.session_state.evidence_drafts.setdefault(typ,{})["upload"]=None
                    st.session_state.pending_intake_reset=typ
                    st.toast("Evidence added to the local case draft.")
                    st.rerun()
        draft=st.session_state.get("draft_case")
        if draft:
            dc=database.get_case(draft)
            with st.expander(f"Evidence saved to draft · {len(dc['events'])} item(s)",expanded=False):
                for item in dc["events"][-5:]: st.markdown(f"**{item['event_type'].replace('_',' ').title()}** · {item['channel']} · {item['timestamp'][:16]}<br>{item['content'][:180]}",unsafe_allow_html=True)
            clear_col,start_col=st.columns(2)
            if start_clicked: run(draft)
    with right:
        with st.container(border=True,key="intake-guidelines-panel"):
            st.markdown("### ⓘ Investigation Guidelines")
            st.markdown("✓ Add as much related evidence as possible<br>✓ Include the full sequence of interactions<br>✓ Screenshots help in better analysis<br>✓ Add multiple evidence types<br><br><b>Never share a PIN, OTP, or password.</b>",unsafe_allow_html=True)
        with st.container(border=True,key="intake-supported-panel"):
            st.markdown("### ▱ Supported Evidence")
            supported=[("💬","Messages / Chat","SMS, WhatsApp, Telegram, etc."),("☎","Call Summary","Call notes, transcripts, or key details"),("↗","URL / Link","Suspicious or shared links"),("▦","QR Code","Visible QR payload or payment URI"),("₹","Payment / UPI","User-reported amount, ID, and reference"),("▧","Files / Screenshots","Images, documents, or other proof")]
            st.markdown('<div class="supported-evidence-list">'+''.join(f'<div class="supported-evidence-item"><span>{icon}</span><div><b>{title}</b><small>{desc}</small></div></div>' for icon,title,desc in supported)+'</div>',unsafe_allow_html=True)
        if llm_config["provider"]=="groq": st.info("Groq mode sends submitted evidence text to Groq for selected agent analysis.")
        else: st.caption("Local fallback mode · evidence is not sent to an LLM provider.")

elif page=="Case History":
    selected=st.session_state.selected_case
    if selected:
        c=database.get_case(selected)
        if not c: st.session_state.selected_case=None; st.rerun()
        header(c['title'],f"Case ID: {c['id']} · {'Synthetic demo' if c['synthetic'] else 'User-provided'} · {risk(c).replace('_',' ')}")
        if st.button("← Back to Case History"): st.session_state.selected_case=None; st.rerun()
        tabs=st.tabs(["Scam Timeline","Evidence & Agent Analysis","Scam Tracker / Journey Tracker","Final Assessment","Report & Actions"])
        with tabs[0]:
            st.subheader("Scam Timeline")
            for e in c['events']:
                with st.expander(f"{e['timestamp'][:16]} · {e['event_type'].replace('_',' ').title()} · {e['channel']} · {e['id']}",expanded=False):
                    st.write(e['content']); st.caption(f"Source: {e['source']} · Event ID: {e['id']}")
                    for attachment in e.get('attachments',[]): st.caption(f"Attachment: {attachment['filename']} · {attachment['size_bytes']} bytes · OCR unavailable")
            if st.button("＋ Add follow-up evidence"):
                st.session_state.add_followup=True
            if st.session_state.get('add_followup'):
                with st.form("followup"):
                    txt=st.text_area("Evidence text"); et=st.selectbox("Type",["message","call_summary","url","qr_payload","payment_request","payment_attempt","note","other"]); channel=st.text_input("Channel",value="Other")
                    if st.form_submit_button("Save evidence"):
                        if txt.strip(): database.add_event(selected,{"event_type":et,"content":txt,"channel":channel}); run(selected)
        with tabs[1]:
            st.subheader("Evidence Inventory & Agent Findings")
            st.caption("Evidence is user-provided and not independently verified. Each agent finding records its provider, model, and any local fallback.")
            st.dataframe(pd.DataFrame([{k:e[k] for k in ["id","timestamp","event_type","channel","source"]} for e in c['events']]),width="stretch",hide_index=True,height=110)
            for f in c.get('findings') or []:
                model_label=(f.get('model') or f.get('provider') or 'local')
                with st.expander(f"{f['agent_name']} · {f['status']} · {model_label} · confidence {f.get('confidence',0):.0%}"):
                    st.write(f['summary']); st.write("Evidence references: "+(", ".join(f.get('evidence_refs',[])) or "None"));
                    for i in f.get('indicators',[]): st.write(f"• {i['code']} — {i['description']} · {', '.join(i['event_ids'])}")
                    if f.get('uncertainties'): st.caption("Uncertainty: "+"; ".join(f['uncertainties']))
                    if f.get('fallback_reason'): st.caption("Fallback reason: "+f['fallback_reason'].replace('_',' '))
            if st.button("Run / Update Investigation",type="primary"): run(selected)
        with tabs[2]:
            st.subheader("Candidate Scam Journey")
            stages=[("Initial Contact",any(e['event_type'] in ('message','call_summary') for e in c['events'])),("Trust Building",any('support' in e['content'].lower() or 'bank' in e['content'].lower() for e in c['events'])),("Link / App Induced",any(e['event_type'] in ('url','qr_payload') or 'http' in e['content'] for e in c['events'])),("Payment Request",any(e['event_type']=='payment_request' for e in c['events'])),("Payment Attempt",any(e['event_type']=='payment_attempt' for e in c['events']))]
            for i,(name,seen) in enumerate(stages): st.write(("✅" if seen else "○")+f"  {i+1}. {name} — "+("observed in supplied evidence" if seen else "not observed"))
            st.caption("Candidate stages are rule-derived, not official tracking. Unobserved stages are not assumed.")
        with tabs[3]:
            a=c.get('assessment') or {}; st.subheader("Final Assessment")
            st.metric("Risk Level",a.get('risk_level','INSUFFICIENT_EVIDENCE').replace('_',' '),f"Score {a.get('score','—')} / 100 (rule index, not a probability)")
            st.caption(a.get('reason','No investigation has been run yet.'))
            synthesis=a.get('llm_synthesis')
            if synthesis:
                model_label=synthesis.get('model') or synthesis.get('provider','local')
                st.markdown(f"**Final Synthesis · {synthesis.get('status','fallback')} · {model_label}**")
                st.write(synthesis.get('summary',''))
                if synthesis.get('fallback_reason'): st.caption("Synthesis fallback: "+synthesis['fallback_reason'].replace('_',' '))
                if synthesis.get('evidence_basis'): st.caption("Synthesis evidence: "+", ".join(synthesis['evidence_basis']))
            st.caption("Supporting events: "+(", ".join(a.get('supporting_event_ids',[])) or "None"))
            unc,recs=st.columns(2)
            with unc:
                st.markdown("**Uncertainties**")
                st.markdown("<br>".join("• "+x for x in (a.get('uncertainties',[]) or ["No additional uncertainty recorded."])),unsafe_allow_html=True)
            with recs:
                st.markdown("**Safe next steps**")
                st.markdown("<br>".join("• "+x for x in (a.get('recommendations',[]) or ["No additional steps recorded."])),unsafe_allow_html=True)
            st.caption("ScamTrace is a student prototype, not affiliated with UPI or any bank.")
        with tabs[4]:
            st.subheader("Report & Actions")
            report={k:c.get(k) for k in ['id','title','summary','synthetic','events','assessment','findings','relations']}
            md=f"# UPI ScamTrace Case Report — {c['title']}\n\nCase: {c['id']} | Synthetic: {bool(c['synthetic'])}\n\n## Assessment\n\n{json.dumps(c.get('assessment'),indent=2)}\n\n## Timeline\n"+"\n".join(f"- {e['timestamp']} · {e['event_type']} · {e['channel']} · {e['id']}: {e['content']}" for e in c['events'])+"\n\nUser-provided evidence is not independently verified. This prototype cannot reverse transactions."
            x,y=st.columns(2); x.download_button("Download Markdown report",md,file_name=f"{selected}.md",mime="text/markdown"); y.download_button("Download JSON case",json.dumps(report,indent=2),file_name=f"{selected}.json",mime="application/json")
            for attachment in database.get_attachments(selected):
                st.download_button(f"Download attachment: {attachment['filename']}",attachment['data'],file_name=attachment['filename'],mime=attachment['mime_type'],key=f"attachment_{attachment['id']}")
            st.warning("Deleting a case removes its events and saved analysis.")
            if "confirm_delete" not in st.session_state: st.session_state.confirm_delete=False
            if st.button("Delete Case",type="secondary"): st.session_state.confirm_delete=True
            if st.session_state.confirm_delete:
                st.error("Confirm permanent deletion?"); x,y=st.columns(2)
                if x.button("Yes, delete permanently"):
                    database.delete_case(selected); st.session_state.selected_case=None; st.session_state.confirm_delete=False; st.rerun()
                if y.button("Cancel deletion"): st.session_state.confirm_delete=False; st.rerun()
    else:
        header("Case History","View and manage your past investigations. Search, filter, and track the status of all cases.")
        fq,fs,fr,fd,reset=st.columns([2.4,1.05,1.35,1.15,.9],gap="small")
        q=fq.text_input("Search",placeholder="Search case ID, title, phone, UPI ID, URL, or evidence",label_visibility="collapsed",key="history_search")
        status=fs.selectbox("Status",["All Statuses","New","Evidence added","Investigated"],key="history_status")
        risks=fr.selectbox("Risk Level",["All Risk Levels","HIGH_CONCERN","CAUTION","LOW_CONCERN","INSUFFICIENT_EVIDENCE"],key="history_risk")
        datef=fd.selectbox("Date Range",["All Time","Last 30 Days"],key="history_date")
        if reset.button("↻ Reset Filters",key="reset_case_filters"):
            for key in ("history_search","history_status","history_risk","history_date","history_sort"):
                if key in st.session_state: del st.session_state[key]
            st.session_state.history_page=0; st.rerun()
        cutoff=datetime.now(timezone.utc).timestamp()-30*86400
        filtered=[]
        for item in all_cases:
            body=item['id']+item['title']+item.get('summary','')
            if q.strip():
                detail=database.get_case(item['id'])
                event_text=" ".join(" ".join((event.get('content') or '',json.dumps(event.get('fields') or {},ensure_ascii=False)," ".join(att.get('filename','') for att in event.get('attachments',[])))) for event in detail['events'])
                body+=" "+event_text
            body=body.casefold()
            date_ok=datef!="Last 30 Days" or (item.get('created_at') and datetime.fromisoformat(item['created_at']).timestamp()>=cutoff)
            if q.lower() in body and (status=="All Statuses" or item['status']==status) and (risks=="All Risk Levels" or risk(item)==risks) and date_ok:
                filtered.append(item)
        left,right=st.columns([1,1],gap="small")
        with left:
            with st.container(border=True,key="case-history-table-panel"):
                list_head,sort_col=st.columns([1.3,1],gap="small",vertical_alignment="center")
                list_head.caption(f"Total Cases: {len(filtered)}")
                sort_by=sort_col.selectbox("Sort by",["Newest First","Oldest First","Risk (Highest First)","Risk (Lowest First)"],key="history_sort",label_visibility="collapsed")
                risk_rank={"HIGH_CONCERN":3,"CAUTION":2,"LOW_CONCERN":1,"INSUFFICIENT_EVIDENCE":0}
                if sort_by=="Newest First": filtered.sort(key=lambda c:c.get('updated_at') or '',reverse=True)
                elif sort_by=="Oldest First": filtered.sort(key=lambda c:c.get('updated_at') or '')
                elif sort_by=="Risk (Highest First)": filtered.sort(key=lambda c:(risk_rank.get(risk(c),0),c.get('updated_at') or ''),reverse=True)
                else: filtered.sort(key=lambda c:(risk_rank.get(risk(c),0),c.get('updated_at') or ''))
                st.markdown("<div class='history-heading'><b>Case Details</b><b>Risk Level</b><b>Status</b><b>Date & Time</b><b>Actions</b></div>",unsafe_allow_html=True)
                page_size=8; pages=max(1,(len(filtered)+page_size-1)//page_size)
                page_idx=min(st.session_state.get("history_page",0),pages-1); st.session_state.history_page=page_idx
                shown=filtered[page_idx*page_size:(page_idx+1)*page_size]
                for c in shown:
                    icon="🔗" if "link" in c['title'].lower() else ("🛡️" if risk(c)=="LOW_CONCERN" else "💬")
                    row=st.columns([2.6,1.25,1.2,1.2,.65],gap="small",vertical_alignment="center")
                    selected_row=" selected" if st.session_state.get("preview_case")==c['id'] else ""
                    row[0].markdown(f'<div class="history-case-cell{selected_row}" data-case-id="{c["id"]}"><div class="history-case-icon">{icon}</div><div class="history-case-copy"><b>{c["title"]}</b><small>Case ID: {c["id"]} · {"Synthetic demo" if c["synthetic"] else "User-provided"}</small><small>{len(database.get_case(c["id"])["events"])} evidence item(s)</small></div></div>',unsafe_allow_html=True)
                    row[1].markdown(f"<span class='risk-pill risk-{risk(c).lower()}'>{risk(c).replace('_',' ').title()}</span>",unsafe_allow_html=True)
                    row[2].markdown(f"<span class='state-pill'>{c['status']}</span>",unsafe_allow_html=True)
                    updated=(c.get('updated_at') or '')[:16].replace('T',' ')
                    row[3].markdown(f"<small>{updated}</small>",unsafe_allow_html=True)
                    if row[4].button("→",key="preview_"+c['id'],help="Preview case"):
                        st.session_state.preview_case=c['id']; st.rerun()
                if pages>1:
                    pa,pb,pc=st.columns([1,1,1])
                    if pa.button("‹",disabled=page_idx==0,key="history_prev"): st.session_state.history_page=page_idx-1; st.rerun()
                    pb.caption(f"Page {page_idx+1} of {pages}")
                    if pc.button("›",disabled=page_idx>=pages-1,key="history_next"): st.session_state.history_page=page_idx+1; st.rerun()
                if not filtered: st.info("No matching cases. Use New Investigation or load the labeled synthetic demo.")
        with right:
            with st.container(border=True,key="case-preview-panel"):
                selected_id=st.session_state.get("preview_case")
                target=next((item for item in filtered if item['id']==selected_id),filtered[0] if filtered else None)
                if target:
                    c=database.get_case(target['id'])
                    preview_icon="🔗" if "link" in c['title'].lower() else ("🛡️" if risk(c)=="LOW_CONCERN" else "💬")
                    st.markdown(f'<div class="history-preview-head"><span class="history-case-icon">{preview_icon}</span><div><b>{c["title"]}</b><small>Case ID: {c["id"]} · {"Synthetic demo" if c["synthetic"] else "User-provided"}</small></div><span class="state-pill">{c["status"]}</span></div>',unsafe_allow_html=True)
                    first_event=(c.get('events') or [{}])[0]
                    participants=next((str(e.get('fields',{}).get('participants')) for e in c.get('events',[]) if e.get('fields',{}).get('participants')),"Not recorded")
                    upi_id=next((str(e.get('fields',{}).get('upi_id')) for e in c.get('events',[]) if e.get('fields',{}).get('upi_id')),"Not recorded")
                    event_date=(first_event.get('timestamp') or c.get('created_at') or 'Date not recorded')[:16].replace('T',' ')
                    st.markdown(f'<div class="history-meta"><div><b>◷ Date &amp; Time</b><small>{event_date}</small></div><div><b>♧ Participants</b><small>{participants}</small></div><div><b>↗ UPI ID</b><small>{upi_id}</small></div></div>',unsafe_allow_html=True)
                    tabs=st.tabs(["Overview","Timeline","Evidence","Agent Analysis","Report"])
                    with tabs[0]:
                        assessment=c.get('assessment') or {}
                        score=int(assessment.get('score',0) or 0)
                        confidence=sum(float(f.get('confidence',0) or 0) for f in (c.get('findings') or []))/max(1,len(c.get('findings') or []))
                        event_types=sorted({e.get('event_type','').replace('_',' ').title() for e in c['events'] if e.get('event_type')})
                        reason_codes=', '.join(x.replace('_',' ').title() for x in (assessment.get('reason_codes') or [])) or 'No material rule indicators saved'
                        summary=c.get('summary') or 'No case summary supplied.'
                        st.markdown(f'<div class="history-overview"><div class="history-risk-card"><b>Rule-Based Risk Assessment</b><div class="history-risk-body"><div class="history-gauge" style="--risk:{score*3.6}deg"><span>{score}<small>Rule index / 100</small></span></div><div><div class="history-fact"><b>Assessment</b>{risk(c).replace("_"," ").title()}</div><div class="history-fact"><b>Evidence types</b>{len(event_types)} · {len(c["events"])} item(s)</div><div class="history-fact"><b>Mean finding confidence</b>{confidence:.2f} · descriptive</div></div></div></div><div class="history-final-card"><b>Final Assessment</b><p>{assessment.get("reason","Analysis has not been run.")}</p><small>Indicators: {reason_codes}</small></div></div>',unsafe_allow_html=True)
                        st.markdown(f'<div class="history-findings"><b>Overview &amp; Key Findings</b><div>{summary}</div>'+''.join(f'<div>✓　{f["agent_name"]}: {f["summary"]}</div>' for f in (c.get('findings') or [])[:3])+'</div>',unsafe_allow_html=True)
                        st.markdown('<div class="history-warning"><b>Important</b> Evidence is user-provided and not independently verified. A rule score is not a fraud probability.</div>',unsafe_allow_html=True)
                    with tabs[1]:
                        for e in c['events'][:5]: st.markdown(f"**{e['timestamp'][:16]} · {e['event_type'].replace('_',' ').title()}**　{e['channel']}<br>{e['content'][:180]}",unsafe_allow_html=True)
                    with tabs[2]:
                        for e in c['events'][:7]: st.markdown(f"**{e['event_type'].replace('_',' ').title()}** · {e['channel']} · {e['id']}<br>{e['content'][:140]}",unsafe_allow_html=True)
                    with tabs[2]:
                        for f in (c.get('findings') or []): st.markdown(f"**{f['agent_name']}** · {f.get('provider','local')} · {f['status']}<br>{f['summary']}",unsafe_allow_html=True)
                    with tabs[3]:
                        st.caption("Reports include the assessment, evidence timeline, and saved findings.")
                        if st.download_button("Download Markdown report",f"# {c['title']}\n\n{json.dumps(c.get('assessment'),indent=2)}",file_name=f"{c['id']}.md",mime="text/markdown",key="history_report_"+c['id']): st.toast("Report downloaded")
                    if st.button("Open selected case workspace",type="primary",key="history_workspace"):
                        go_case(c['id']); st.rerun()
                else:
                    st.info("Select a case to preview details.")

elif page=="Analytics":
    header("Analytics — Scam Intelligence","Comprehensive insights on scam detection, investigation patterns, agent findings, and evidence analysis.")
    cs=cases(); analyzed=[c for c in cs if c.get('assessment')]; details={c['id']:database.get_case(c['id']) for c in cs}
    events=[e for c in details.values() for e in c['events']]
    findings=[f for c in analyzed for f in (c.get('findings') or [])]
    indicators=[i for f in findings for i in f.get('indicators',[])]
    analytics_tabs=st.tabs(["Scam Timeline","Evidence & Agent Analysis","Scam Tracker","Final Assessment","Report & Actions"],default="Evidence & Agent Analysis")
    with analytics_tabs[0]:
        timeline_cases=len(cs); timeline_events=len(events)
        a,b,c=st.columns(3)
        a.metric("Persisted cases",timeline_cases); b.metric("Evidence events",timeline_events); c.metric("Analyzed cases",len(analyzed))
        trend_cols,feed_col=st.columns([1.55,1],gap="small")
        with trend_cols:
            with st.container(border=True,key="analytics-timeline-trend"):
                st.markdown("### Evidence arrivals over time")
                dated=[]
                for e in events:
                    try: dated.append({"Date":datetime.fromisoformat(e['timestamp'].replace('Z','+00:00')).date().isoformat(),"Evidence type":e['event_type'].replace('_',' ').title()})
                    except (TypeError,ValueError): continue
                if dated:
                    counts=pd.DataFrame(dated).groupby(["Date","Evidence type"]).size().reset_index(name="Events")
                    fig=px.bar(counts,x="Date",y="Events",color="Evidence type",barmode="stack",color_discrete_sequence=["#142923","#C6A76A","#5A9C78","#95B68D","#BFC9BC"])
                    fig.update_layout(height=260,margin=dict(l=8,r=8,t=8,b=8),font=dict(size=10),legend=dict(orientation="h",y=-.25),plot_bgcolor="#F5F2EA",paper_bgcolor="#F5F2EA")
                    st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=260)
                else: st.info("No evidence timeline is available yet. Add evidence to create one.")
                st.caption("Counts use timestamps stored with persisted evidence. Synthetic examples are included and labeled in Case History.")
        with feed_col:
            with st.container(border=True,key="analytics-timeline-feed"):
                st.markdown("### Recent recorded events")
                latest=sorted(events,key=lambda e:e.get('timestamp',''),reverse=True)[:5]
                if latest:
                    for event in latest:
                        owner=next((c for c in cs if any(x['id']==event['id'] for x in details[c['id']]['events'])),None)
                        st.markdown(f"**{event['event_type'].replace('_',' ').title()}** · {event['channel']}<br><small>{event.get('timestamp','')[:16]} · {owner['title'] if owner else 'Saved case'} · {event['id']}</small>",unsafe_allow_html=True)
                        st.divider()
                else: st.info("No saved events yet.")
    with analytics_tabs[1]:
        metrics=[("▤",str(len(events)),"Total Evidences"),("▱",str(len(analyzed)),"Investigations"),("♧",str(len(AGENT_NAMES)),"Specialist Agents"),("◎",str(len(indicators)),"Recorded Indicators"),("◉",f"{sum(f.get('confidence',0) for f in findings)/len(findings):.2f}" if findings else "—","Mean Agent Confidence")]
        banner=''.join(f'<div class="analytics-metric"><b>{icon}</b><strong>{value}</strong><small>{label}</small></div>' for icon,value,label in metrics)
        st.markdown(f'<div class="analytics-banner"><div><h2>Evidence & Agent Analysis</h2><p>Computed from persisted cases; synthetic examples remain labeled in Case History.</p></div><div class="analytics-metrics">{banner}</div></div>',unsafe_allow_html=True)
        row1a,row1b,row1c=st.columns([1.2,1.5,1],gap="small")
        with row1a:
            with st.container(border=True,key="analytics-distribution"):
                st.markdown("### Evidence Type Distribution")
                type_counts={}
                for e in events: type_counts[e['event_type']]=type_counts.get(e['event_type'],0)+1
                if type_counts:
                    type_labels={"message":"Messages / Chat","call_summary":"Call Summaries","url":"URLs / Links","qr_payload":"QR Payloads","payment_request":"Payment Requests","payment_attempt":"Payment Attempts","note":"Notes","other":"Files / Other"}
                    palette=["#08734D","#D8A332","#5A9C78","#89B991","#B9D7C3","#D9CDAF","#AAB2A9","#C6A76A"]
                    distribution=sorted(type_counts.items(),key=lambda x:(-x[1],x[0]))
                    colors={kind:palette[i%len(palette)] for i,(kind,_) in enumerate(distribution)}
                    dist_col,list_col=st.columns([.9,1.1],gap="small",vertical_alignment="center")
                    with dist_col:
                        fig=px.pie(names=[type_labels.get(x,x.replace('_',' ').title()) for x,_ in distribution],values=[n for _,n in distribution],hole=.62,color_discrete_sequence=[colors[x] for x,_ in distribution])
                        fig.update_layout(height=138,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",annotations=[dict(text=f"{len(events)}<br><sup>Events</sup>",x=.5,y=.5,showarrow=False,font=dict(size=16,color="#17231E"))])
                        st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=138)
                    dist_html=''.join(f'<div class="dist-row"><i style="background:{colors[kind]}"></i><span>{type_labels.get(kind,kind.replace("_"," ").title())}</span><b>{count} · {count/max(1,len(events)):.1%}</b></div>' for kind,count in distribution[:6])
                    list_col.markdown('<div class="dist-list">'+dist_html+'</div>',unsafe_allow_html=True)
                else: st.caption("No evidence data yet.")
        with row1b:
            with st.container(border=True,key="analytics-agent-performance"):
                st.markdown("### Multi-Agent Performance")
                perf_html='<div class="agent-perf-list">'
                for name in AGENT_NAMES:
                    runs=[f for f in findings if f['agent_name']==name]
                    mean=sum(float(f.get('confidence',0)) for f in runs)/len(runs) if runs else None
                    providers=', '.join(sorted({f.get('provider','local') for f in runs})) if runs else 'Not run'
                    value=f'{mean:.2f}' if mean is not None else '—'
                    width=max(0,min(100,round((mean or 0)*100)))
                    perf_html+=f'<div class="agent-perf-row"><div><b>{name}</b><small>{len(runs)} finding(s) · {providers}</small></div><div class="agent-conf-track"><span style="width:{width}%"></span></div><strong>{value}</strong></div>'
                st.markdown(perf_html+'</div>',unsafe_allow_html=True)
        with row1c:
            with st.container(border=True,key="analytics-outcomes"):
                st.markdown("### Assessment Outcomes")
                outcomes={"High concern":sum(risk(c)=="HIGH_CONCERN" for c in analyzed),"Caution":sum(risk(c)=="CAUTION" for c in analyzed),"Low concern":sum(risk(c)=="LOW_CONCERN" for c in analyzed),"Insufficient":sum(risk(c)=="INSUFFICIENT_EVIDENCE" for c in analyzed)}
                if analyzed:
                    outcome_colors={"High concern":"#D84A43","Caution":"#D8A332","Low concern":"#278158","Insufficient":"#A9B1A7"}
                    out_col,list_col=st.columns([1.05,.95],gap="small",vertical_alignment="center")
                    with out_col:
                        fig=px.pie(names=list(outcomes),values=list(outcomes.values()),hole=.62,color=list(outcomes),color_discrete_map=outcome_colors)
                        fig.update_traces(domain=dict(x=[0.08,0.92],y=[0.08,0.92]))
                        fig.update_layout(height=128,margin=dict(l=4,r=4,t=4,b=4),showlegend=False,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",annotations=[dict(text=f"{len(analyzed)}<br><sup>Cases</sup>",x=.5,y=.5,showarrow=False,font=dict(size=15,color="#17231E"))])
                        st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=128)
                    out_html=''.join(f'<div class="outcome-row"><i style="background:{outcome_colors[name]}"></i><span>{name}</span><b>{count} · {count/max(1,len(analyzed)):.0%}</b></div>' for name,count in outcomes.items())
                    list_col.markdown('<div class="outcome-list">'+out_html+'</div><small>Deterministic labels, not fraud probabilities.</small>',unsafe_allow_html=True)
                else: st.caption("No investigations have saved assessments yet.")
        row2a,row2b,row2c=st.columns([1.2,1,1.2],gap="small")
        type_agents={}
        evidence_group={"message":"Messages / Chat","call_summary":"Call Summaries","url":"URLs / Links / QR","qr_payload":"URLs / Links / QR","payment_request":"Payment / UPI","payment_attempt":"Payment / UPI","other":"Files / Other","note":"Files / Other"}
        for case in analyzed:
            type_by_id={e['id']:e['event_type'] for e in details[case['id']]['events']}
            for f in case.get('findings') or []:
                for event_id in f.get('evidence_refs',[]):
                    if event_id in type_by_id:
                        category=evidence_group.get(type_by_id[event_id],"Files / Other")
                        type_agents.setdefault(category,set()).add(f['agent_name'])
        with row2a:
            with st.container(border=True,key="analytics-mapping"):
                st.markdown("### Evidence → Agent Mapping")
                if type_agents:
                    agent_cols=["Message Agent","Link & QR Agent","Payment Agent","Timeline Agent","Journey Agent","Decision Agent"]
                    html='<table class="mapping-table"><thead><tr><th>Evidence</th>'+''.join(f'<th>{name.replace(" Agent","")}</th>' for name in agent_cols)+'</tr></thead><tbody>'
                    for kind,names in sorted(type_agents.items()):
                        html+=f'<tr><td>{kind}</td>'+''.join(f'<td class="{"matched" if name in names else "unmatched"}">{"✓" if name in names else "·"}</td>' for name in agent_cols)+'</tr>'
                    st.markdown(html+'</tbody></table>',unsafe_allow_html=True)
                else: st.caption("No saved evidence references yet.")
        with row2b:
            with st.container(border=True,key="analytics-common-findings"):
                st.markdown("### Key Agent Findings")
                code_counts={}
                for item in indicators: code_counts[item['code'].replace('_',' ').title()]=code_counts.get(item['code'].replace('_',' ').title(),0)+1
                if code_counts:
                    top=sorted(code_counts.items(),key=lambda x:x[1],reverse=True)[:5]
                    common_fig=px.bar(x=[v for _,v in top],y=[k for k,_ in top],orientation="h",color_discrete_sequence=["#08734D"])
                    common_fig.update_traces(text=[str(v) for _,v in top],textposition="outside",cliponaxis=False)
                    common_fig.update_layout(height=112,margin=dict(l=3,r=18,t=2,b=2),font=dict(size=9),showlegend=False,xaxis=dict(title=None,showgrid=False,zeroline=False,range=[0,max(1,max(v for _,v in top))*1.25],tickmode="array",tickvals=list(range(max(1,max(v for _,v in top))+1))),yaxis=dict(title=None,autorange="reversed"))
                    st.plotly_chart(common_fig,width="stretch",config={"displayModeBar":False},height=112)
                else: st.caption("No indicator findings have been recorded.")
        with row2c:
            with st.container(border=True,key="analytics-correlation"):
                st.markdown("### Evidence Correlation")
                buckets=[("Messages / Chat",{"message","call_summary"}),("URLs / Links",{"url","qr_payload"}),("Payments / UPI",{"payment_request","payment_attempt"})]
                counts_by_bucket=[sum(any(e['event_type'] in kinds for e in details[case['id']]['events']) for case in cs) for _,kinds in buckets]
                flow=''.join(f'<div class="flow-stage"><b>{count}</b><small>{label}</small></div>'+('<span class="flow-arrow">→</span>' if i<2 else '') for i,((label,_),count) in enumerate(zip(buckets,counts_by_bucket)))
                st.markdown(f'<div class="flow-row">{flow}</div><small>Cases with each evidence category. Categories may overlap.</small>',unsafe_allow_html=True)
        row3a,row3b,row3c=st.columns([1.38,1,1.05],gap="small")
        with row3a:
            with st.container(border=True,key="analytics-trend"):
                st.markdown("### Evidence Usage & Rule Score")
                if cs:
                    trend=pd.DataFrame({"Case":range(1,len(cs)+1),"Evidence items":[len(details[case['id']]['events']) for case in cs],"Rule score index":[(case.get('assessment') or {}).get('score',0) for case in cs]})
                    fig=go.Figure()
                    fig.add_trace(go.Scatter(x=trend["Case"],y=trend["Evidence items"],mode="lines+markers",name="Evidence items",line=dict(color="#08734D",width=2),marker=dict(size=6)))
                    fig.add_trace(go.Scatter(x=trend["Case"],y=trend["Rule score index"],mode="lines+markers",name="Rule score index",line=dict(color="#C6A76A",width=2),marker=dict(size=6)))
                    y_max=max(2,trend["Evidence items"].max(),trend["Rule score index"].max())
                    fig.update_layout(
                        height=118,
                        margin=dict(l=28,r=5,t=20,b=18),
                        font=dict(size=8),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h",y=1.03,x=0,entrywidth=0.48,entrywidthmode="fraction",font=dict(size=8)),
                        xaxis=dict(title="",tickmode="array",tickvals=trend["Case"].tolist(),zeroline=False,showgrid=False),
                        yaxis=dict(title="",range=[0,y_max*1.12],tickfont=dict(size=8),showgrid=True,gridcolor="#EEE5D7",zeroline=False),
                    )
                    st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=118)
                else: st.caption("No persisted cases.")
                st.caption("Rule score is an index, not a fraud probability.")
        with row3b:
            with st.container(border=True,key="analytics-impact"):
                st.markdown("### Investigation Impact")
                multi=sum(len(details[case['id']]['events'])>=3 for case in cs)
                relations=sum(len(case.get('relations') or []) for case in analyzed)
                st.markdown(f'<div class="impact-row"><span>Cases with ≥3 evidence items</span><b>{multi}</b></div><div class="impact-row"><span>Grounded evidence relations</span><b>{relations}</b></div><div class="impact-row"><span>Mean events per case</span><b>{round(len(events)/max(1,len(cs)),1)}</b></div>',unsafe_allow_html=True)
        with row3c:
            with st.container(border=True,key="analytics-insights"):
                st.markdown('<div class="insights-title">💡 Key Insights</div>',unsafe_allow_html=True)
                type_labels={"message":"Messages / Chat","call_summary":"Call Summaries","url":"URLs / Links","qr_payload":"QR Payloads","payment_request":"Payment Requests","payment_attempt":"Payment Attempts","note":"Notes","other":"Files / Other"}
                top_type=type_labels.get(max(type_counts,key=type_counts.get),"No evidence yet") if type_counts else "No evidence yet"
                high=sum(risk(case)=="HIGH_CONCERN" for case in analyzed)
                case_word="case" if len(cs)==1 else "cases"
                st.markdown(f'<div class="analytics-key-insights"><div><i>✓</i><span>{len(cs)} persisted {case_word} {"is" if len(cs)==1 else "are"} included; synthetic cases are labeled in history.</span></div><div><i>✓</i><span>{top_type} is the most common submitted evidence type.</span></div><div><i>✓</i><span>{high} saved assessments have high-concern rule labels.</span></div><div><i>✓</i><span>Scores are deterministic indices, not fraud probabilities.</span></div></div>',unsafe_allow_html=True)
    with analytics_tabs[2]:
        tracker_cases=[case for case in cs if case.get('assessment')]
        if tracker_cases:
            selected_tracker=st.selectbox("Case journey",tracker_cases,format_func=lambda x:f"{x['title']} · {x['id']}"+(" · Synthetic demo" if x['synthetic'] else ""),key="analytics_tracker_case",label_visibility="collapsed")
            c=details[selected_tracker['id']]
            codes={indicator['code'] for finding in (c.get('findings') or []) for indicator in finding.get('indicators',[])}
            stages=[
                ("Initial Contact",[e for e in c['events'] if e['event_type'] in ("message","call_summary")],"Message or call evidence"),
                ("Trust Building",[e for e in c['events'] if any(code in codes for code in ("impersonation","urgency","credential_request")) and e['id'] in {eid for finding in (c.get('findings') or []) for eid in finding.get('evidence_refs',[])}],"Saved specialist indicators"),
                ("Link / App Induced",[e for e in c['events'] if e['event_type'] in ("url","qr_payload") or "http://" in e['content'].lower() or "https://" in e['content'].lower()],"URL or QR evidence"),
                ("Payment Request",[e for e in c['events'] if e['event_type']=="payment_request"],"User-reported request"),
                ("Payment Attempt",[e for e in c['events'] if e['event_type']=="payment_attempt"],"User-reported attempt"),
            ]
            st.markdown(f'<div class="tracker-banner"><div class="tracker-banner-copy"><strong>Candidate Scam Journey</strong><small class="tracker-disclaimer">Stages are evidence-derived candidates; missing stages are not inferred. This is not an official UPI tracking service.</small></div><span>{c["id"]} · {len(c["events"])} evidence item(s) · {risk(c).replace("_"," ")}</span></div>',unsafe_allow_html=True)
            stage_cols=st.columns(5,gap="small")
            for i,(name,items,rule) in enumerate(stages):
                with stage_cols[i]:
                    refs=', '.join(e['id'] for e in items) or "No supporting evidence"
                    status="Observed" if items else "Not observed"
                    st.markdown(f'<div class="tracker-stage {"observed" if items else "missing"}"><small>STAGE {i+1}</small><b>{name}</b><span>{"●" if items else "○"} {status}</span><p>{rule}</p><em>{refs}</em></div>',unsafe_allow_html=True)
            with st.container(border=True,key="tracker-evidence-panel"):
                st.markdown("### Evidence supporting the selected journey")
                if c['events']:
                    st.dataframe(pd.DataFrame([{"Stage evidence":e['event_type'].replace('_',' ').title(),"Event ID":e['id'],"Timestamp":e['timestamp'][:16],"Channel":e['channel'],"Agent references":", ".join(f['agent_name'] for f in (c.get('findings') or []) if e['id'] in f.get('evidence_refs',[])) or "No saved agent reference"} for e in c['events']]),width="stretch",height=220,hide_index=True)
        else: st.info("Run an investigation to create a saved candidate journey. Synthetic cases are labeled in Case History.")
    with analytics_tabs[3]:
        assessment_counts={"HIGH_CONCERN":sum(risk(c)=="HIGH_CONCERN" for c in analyzed),"CAUTION":sum(risk(c)=="CAUTION" for c in analyzed),"LOW_CONCERN":sum(risk(c)=="LOW_CONCERN" for c in analyzed),"INSUFFICIENT_EVIDENCE":sum(risk(c)=="INSUFFICIENT_EVIDENCE" for c in analyzed)}
        total_assessments=len(analyzed); high_count=assessment_counts['HIGH_CONCERN']
        m1,m2,m3=st.columns(3)
        m1.metric("Saved assessments",total_assessments);m2.metric("High concern",high_count);m3.metric("Mean rule score",round(sum((c.get('assessment') or {}).get('score',0) for c in analyzed)/max(1,total_assessments),1) if analyzed else "—")
        dist_col,decision_col=st.columns([1,1.25],gap="small")
        with dist_col:
            with st.container(border=True,key="analytics-assessment-chart"):
                st.markdown("### Deterministic risk assessment distribution")
                if analyzed:
                    assessment_labels={x.replace('_',' ').title():v for x,v in assessment_counts.items()}
                    assessment_df=pd.DataFrame({"Risk level":list(assessment_labels),"Cases":list(assessment_labels.values())})
                    fig=px.pie(assessment_df,names="Risk level",values="Cases",hole=.57,color="Risk level",color_discrete_map={"High Concern":"#D84A43","Caution":"#D8A332","Low Concern":"#278158","Insufficient Evidence":"#A9B1A7"})
                    fig.update_layout(height=270,margin=dict(l=5,r=5,t=5,b=5),showlegend=True,legend=dict(font=dict(size=11)))
                    st.plotly_chart(fig,width="stretch",config={"displayModeBar":False},height=270)
                else: st.info("No saved assessments yet.")
                st.caption("Risk levels and scores are rule-based indicators, not fraud probabilities.")
        with decision_col:
            with st.container(border=True,key="analytics-assessment-cases"):
                st.markdown("### Case decisions and rationale")
                rows=[]
                for case in analyzed:
                    assess=case.get('assessment') or {}
                    rows.append({"Case":case['title']+(" · Synthetic" if case['synthetic'] else ""),"Risk":risk(case).replace('_',' ').title(),"Rule index":assess.get('score',0),"Evidence":len(details[case['id']]['events']),"Rationale":assess.get('reason','')})
                if rows:
                    rows=sorted(rows,key=lambda x:x["Rule index"],reverse=True)
                    html=""
                    for row in rows:
                        risk_class="high" if row["Risk"]=="High Concern" else ("caution" if row["Risk"]=="Caution" else ("low" if row["Risk"]=="Low Concern" else ""))
                        html+=f'<div class="assessment-row"><strong>{row["Case"]}</strong><span class="assessment-risk {risk_class}">{row["Risk"]}</span><span>Index <b>{row["Rule index"]}</b></span><span>{row["Evidence"]} events</span><small class="assessment-reason">{row["Rationale"]}</small></div>'
                    st.markdown(html,unsafe_allow_html=True)
                else: st.info("Run an investigation to create a saved assessment.")
    with analytics_tabs[4]:
        report_cases=cs
        label="All persisted cases"
        if cs:
            choices=["All persisted cases"]+cs
            selected_report=st.selectbox("Report scope",choices,format_func=lambda x:x if isinstance(x,str) else f"{x['title']} · {x['id']}",key="analytics_report_scope")
            if not isinstance(selected_report,str): report_cases=[selected_report];label=f"Case {selected_report['id']}"
        report_data={"report_scope":label,"generated_at":datetime.now(timezone.utc).isoformat(),"synthetic_cases_included":sum(bool(c['synthetic']) for c in report_cases),"case_count":len(report_cases),"evidence_count":sum(len(details[c['id']]['events']) for c in report_cases),"cases":report_cases}
        markdown=f"# UPI ScamTrace Analytics Report\n\nScope: {label}\nGenerated: {report_data['generated_at']}\nCases: {report_data['case_count']} (synthetic: {report_data['synthetic_cases_included']})\nEvidence events: {report_data['evidence_count']}\n\n"+"\n".join(f"## {c['title']} ({c['id']})\n\nSynthetic demo: {bool(c['synthetic'])}\nAssessment: {json.dumps(c.get('assessment'),ensure_ascii=False)}\n" for c in report_cases)
        report_rows=[]
        for case in report_cases:
            for event in details[case['id']]['events']:
                report_rows.append({"case_id":case['id'],"case_title":case['title'],"synthetic":case['synthetic'],"event_id":event['id'],"timestamp":event['timestamp'],"event_type":event['event_type'],"channel":event['channel'],"source":event['source'],"content":event['content']})
        st.markdown(f'<div class="report-summary"><b>{label}</b><span>{report_data["case_count"]} cases · {report_data["evidence_count"]} evidence events · {report_data["synthetic_cases_included"]} synthetic demo cases</span></div>',unsafe_allow_html=True)
        d1,d2,d3=st.columns(3)
        d1.download_button("Download JSON report",json.dumps(report_data,indent=2,ensure_ascii=False),file_name="scamtrace-analytics.json",mime="application/json",width="stretch")
        d2.download_button("Download Markdown report",markdown,file_name="scamtrace-analytics.md",mime="text/markdown",width="stretch")
        d3.download_button("Download evidence CSV",pd.DataFrame(report_rows).to_csv(index=False),file_name="scamtrace-evidence.csv",mime="text/csv",width="stretch")
        st.warning("Reports contain user-provided evidence. Store and share exported files securely; no data is independently verified.")
        st.caption("All report values are read from the selected persisted case scope. Synthetic entries are explicitly labeled.")

elif page=="About Project":
    header("About Project","Learn about UPI ScamTrace, its objectives, working, and the technology behind it.")
    about_hero=image_uri("about-hero.png")
    feature_items=[("⌕","Multi-Agent<br>Analysis"),("♧","Scam Journey<br>Reconstruction"),("♧","Evidence<br>Correlation"),("⛨","Risk<br>Assessment"),("▥","Analytics<br>&amp; Trends"),("▤","Investigation<br>Report")]
    feature_html="".join(f'<div class="about-feature"><span class="ico">{icon}</span><span>{label}</span></div>' for icon,label in feature_items)
    agent_items=["Message Agent","Link &amp; QR Agent","Payment Agent","Timeline Agent","Investigator Agent","Decision Agent"]
    agent_html="".join(f'<div class="about-agent">{name}</div>' for name in agent_items)
    role_items=[("💬","Message Agent","Analyzes submitted message and call text."),("🔗","Link & QR Agent","Parses visible URLs and QR payload text."),("▣","Payment Agent","Separates requests from reported attempts."),("◷","Timeline Agent","Orders events and transitions."),("♧","Investigator Agent","Reconstructs a candidate sequence."),("♢","Decision Agent","Applies deterministic risk rules.")]
    role_html="".join(f'<div class="about-role"><span>{icon}</span><b>{name}</b><small>{desc}</small></div>' for icon,name,desc in role_items)
    tech_html="".join(f'<div class="about-tech">{name}</div>' for name in ["Python","LangGraph","Groq","Streamlit","Pydantic","SQLite","NetworkX","Pandas · Plotly"])
    st.markdown(f'''<div class="about-layout">
      <div class="about-hero" role="img" aria-label="UPI ScamTrace Project Overview" style="background-image:url({about_hero})"></div>
      <div class="about-row about-top">
        <section class="about-card about-objective"><h3>◎　Objective</h3><p>Automate and strengthen UPI scam investigation using a multi-agent AI approach for accurate detection, journey reconstruction, and actionable insights.</p></section>
        <section class="about-card"><h3>☆　Key Features</h3><div class="about-features-grid">{feature_html}</div></section>
      </div>
      <div class="about-row about-middle">
        <section class="about-card"><h3>▱　System Architecture</h3><div class="about-architecture">
          <div><h4>Input (Evidence)</h4><div class="about-inputs">💬 Messages / Chat<br>☎ Call Logs<br>🔗 URLs / Links<br>₹ UPI / Payments<br>▧ Files / Screenshots</div></div>
          <div class="about-arrow" aria-hidden="true">→</div>
          <div class="about-system"><div class="about-system-title">Multi-Agent AI System</div><div class="about-agent-grid">{agent_html}</div><div class="about-orchestration">◉ LangGraph Workflow<small>Sequential specialists · evidence graph · final synthesis</small></div></div>
          <div class="about-arrow" aria-hidden="true">→</div>
          <div><h4>Output (Results)</h4><div class="about-outputs">✅ Scam Detection<br>✅ Reconstructed Journey<br>✅ Evidence Graph<br>✅ Risk Assessment<br>✅ Investigation Report</div></div>
        </div></section>
        <section class="about-card"><h3>♙　AI Agents (Roles)</h3>{role_html}</section>
      </div>
      <div class="about-row about-bottom">
        <section class="about-card"><h3>▱　Technologies Used</h3><div class="about-tech-grid">{tech_html}</div></section>
        <section class="about-card"><h3>◎　Use Cases</h3><div class="about-list"><div>✅ Investigating user-provided concerns.</div><div>✅ Reconstructing a multi-event journey (contact → trust → payment).</div><div>✅ Identifying common scam patterns and modus operandi.</div><div>✅ Supporting banks, cyber cells, and users in fraud analysis.</div><div>✅ Generating structured, evidence-based investigation reports.</div></div></section>
        <section class="about-card"><h3>ⓘ　Project Information</h3><div class="about-info"><b>Project Type</b><span>AI / ML multi-agent system</span><b>Development</b><span>Jan 2026 – Mar 2026</span><b>Institution</b><span>KIIT University</span><b>Version</b><span>v1.0.0</span></div></section>
      </div>
      <div class="about-footer">No official UPI or bank affiliation. Evidence is user-provided and not independently verified. This prototype cannot reverse payments.</div>
    </div>''',unsafe_allow_html=True)
