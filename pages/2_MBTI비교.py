import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI별 국가 비교", page_icon="⚖️", layout="wide")

st.title("⚖️ MBTI 기준 국가별 비교")
st.markdown("특정 MBTI 유형이 어느 국가에서 가장 많이 나타나는지 확인해 보세요.")

try:
    df = pd.read_csv('countries_mbti.csv')
    
    # MBTI 유형 목록 추출 (Country 컬럼 제외)
    mbti_types = df.columns.drop('Country')
    selected_mbti = st.selectbox("🧠 비교할 MBTI 유형을 선택하세요:", mbti_types)
    
    # 상위 N개 국가 슬라이더
    top_n = st.slider("🔝 표시할 상위 국가 수 조정:", min_value=5, max_value=30, value=15)
    
    # 선택한 MBTI 기준으로 데이터 정렬 후 상위 N개 추출
    compare_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(top_n)
    
    # 시각화 (Plotly 가로 바 차트)
    fig = px.bar(
        compare_df,
        x=selected_mbti,
        y='Country',
        orientation='h',
        title=f"🏆 {selected_mbti} 유형 비율 상위 {top_n} 개국",
        labels={selected_mbti: '비율', 'Country': '국가'},
        color=selected_mbti,
        color_continuous_scale='Plasma'
    )
    
    # 높은 순서대로 위에서부터 나오도록 y축 정렬 뒤집기
    fig.update_yaxis(categoryorder='total ascending')
    
    st.plotly_chart(fig, use_container_width=True)
    
except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
