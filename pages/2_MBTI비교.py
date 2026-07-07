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
    
    # [수정] 차트에서 위에서부터 순서대로 나오도록 데이터프레임을 미리 오름차순(ascending=True)으로 정렬합니다.
    # Plotly 가로 바 차트는 아래서부터 데이터를 쌓아 올리기 때문에, 코드로 정렬할 때는 True로 주어야 화면 위쪽에 가장 높은 값이 옵니다.
    compare_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=True).tail(top_n)
    
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
    
    # 에러가 발생하던 축 업데이트 코드를 제거하고, 간결하게 차트를 출력합니다.
    st.plotly_chart(fig, use_container_width=True)
    
    # 데이터 테이블 표시
    with st.expander("📄 상세 데이터 보기"):
        # 표에서는 높은 순서(내림차순)로 보이도록 정렬하여 출력합니다.
        table_df = compare_df.sort_values(by=selected_mbti, ascending=False)
        st.dataframe(table_df.style.format({selected_mbti: '{:.2%}'}), use_container_width=True)
    
except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
