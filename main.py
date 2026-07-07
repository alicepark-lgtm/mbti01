import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global MBTI Dashboard", page_icon="🌍", layout="wide")

st.title("🌍 글로벌 MBTI 데이터 시각화 대시보드")
st.markdown("---")

st.markdown("""
### 📊 데이터 개요
이 애플리케이션은 전 세계 국가별 MBTI 유형 분포 데이터를 시각화하여 분석합니다.
기존의 세분화된 데이터(`-A`, `-T` 유형)를 하나의 표준 16가지 MBTI 유형으로 통합하여 국가별 성향을 한눈에 비교할 수 있도록 돕습니다.

* **데이터 소스:** `countries_mbti.csv`
* **분석 대상 유형:** 표준 16가지 MBTI (INFJ, INTJ, INFP, INTP 등)
""")

# 데이터 미리보기
try:
    df = pd.read_csv('countries_mbti.csv')
    
    st.subheader("💡 데이터 미리보기")
    st.dataframe(df.head(10), use_container_width=True)
    
    # 간단한 요약 통계
    st.subheader("📈 데이터 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 대상 국가 수", f"{len(df)} 개국")
    col2.metric("가장 데이터가 많은 국가", df.iloc[0]['Country'])
    col3.metric("분석된 MBTI 유형 수", f"{len(df.columns) - 1} 개")

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
