import pandas as pd
import streamlit as st

# 1. 페이지 설정 (세로형 레이아웃을 위해 centered로 변경)
st.set_page_config(page_title="공부습관 대시보드", page_icon="📚", layout="centered")

st.title("📚 나의 공부습관 대시보드")
st.write("Streamlit과 Pandas를 활용한 데이터 시각화 웹앱입니다.")

st.markdown("---")


# 2. 데이터 불러오기 (study.csv 파일 읽기)
@st.cache_data
def load_data():
  df = pd.read_csv("study.csv")
  return df


df = load_data()

# 3. 상단 요약 지표 (세로형 순차적 표시)
st.subheader("📌 전체 요약 정보")

total_students = len(df)  # 총 학생 수
avg_score = df["점수"].mean()  # 평균 점수
avg_study_time = df["공부시간"].mean()  # 평균 공부시간

st.metric(label="총 학생 수", value=f"{total_students}명")
st.metric(label="평균 점수", value=f"{avg_score:.1f}점")
st.metric(label="평균 공부시간", value=f"{avg_study_time:.1f}시간")

st.markdown("---")

# 4. 슬라이더 설정 (최댓값 4.5)
st.subheader("🔍 데이터 필터링")
min_time = st.slider(
    "최소 공부시간 선택", min_value=0.0, max_value=4.5, value=0.0, step=0.5
)

# 5. 데이터 필터링 (선택한 최소 공부시간 이상인 학생)
filtered_df = df[df["공부시간"] >= min_time]

st.info(
    f"현재 **{min_time}시간 이상** 공부한 학생은 총 **{len(filtered_df)}명**입니다."
)

# 6. 세로형 시각화 및 데이터 표 출력
if len(filtered_df) > 0:
  st.markdown("---")

  # [표 출력] 필터링된 데이터 테이블
  st.subheader("📋 조건에 맞는 학생 목록 (표)")
  st.dataframe(filtered_df, use_container_width=True)

  st.markdown("---")

  # [차트 1] 산점도 (공부시간 vs 점수)
  st.subheader("📈 공부시간에 따른 점수 (산점도)")
  st.scatter_chart(filtered_df, x="공부시간", y="점수", color="스마트폰")

  st.markdown("---")

  # [차트 2] 학생별 점수 막대그래프
  st.subheader("📊 학생별 점수 (막대그래프)")
  # 학생ID를 인덱스로 설정하여 X축으로 표현
  chart_data = filtered_df.set_index("학생ID")[["점수"]]
  st.bar_chart(chart_data)

else:
  st.warning("조건에 해당하는 학생 데이터가 없습니다. 슬라이더를 조정해 주세요.")