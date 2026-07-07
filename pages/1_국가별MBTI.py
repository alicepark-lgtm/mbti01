import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 현황", page_icon="📍", layout="wide")

st.title("📍 국가별 MBTI 현황 분석")
st.markdown("특정 국가를 선택하여 해당 국가의 MBTI 유형별 분포를 확인하세요.")

try:
    df = pd.read_csv('countries_mbti.csv')
    
    # 국가 선택 셀렉트박스
    countries = df['Country'].unique()
    selected_country = st.selectbox("🌐 분석할 국가를 선택하세요:", countries)
    
    # 선택한 국가의 데이터 필터링
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).T
    country_data.columns = ['Proportion']
    country_data = country_data.reset_index().rename(columns={'index': 'MBTI'})
    
    # 비율 기준 내림차순 정렬
    country_data = country_data.sort_values(by='Proportion', ascending=False)
    
    # 시각화 (Plotly 바 차트)
    fig = px.bar(
        country_data, 
        x='MBTI', 
        y='Proportion', 
        title=f"📊 {selected_country}의 MBTI 유형별 비율",
        labels={'Proportion': '비율', 'MBTI': 'MBTI 유형'},
        color='Proportion',
        color_continuous_scale='Viridis'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 데이터 테이블 표시
    with st.expander("📄 상세 데이터 보기"):
        st.dataframe(country_data.style.format({'Proportion': '{:.2%}'}), use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
