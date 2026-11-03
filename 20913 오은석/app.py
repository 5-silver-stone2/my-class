import streamlit as st

from api import search_external_movies
from database import (
    create_table,
    add_movie,
    get_all_movies,
    search_movies,
)

# 1. 프로그램 설정
st.set_page_config(
    page_title="영화 기록 관리",
    page_icon="🎬",
)

create_table()

if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

st.title("🎬 영화 기록 관리")

menu = st.sidebar.radio(
    "메뉴",
    ["내 영화 목록", "외부 영화 검색"],
)


# 2. 내 영화 목록
if menu == "내 영화 목록":
    st.header("내 영화 목록")

    keyword = st.text_input(
        "영화 제목 검색",
        key="saved_keyword",
    )

    if keyword.strip() == "":
        movies = get_all_movies()
        empty_message = "저장된 영화가 없습니다."
    else:
        movies = search_movies(keyword.strip())
        empty_message = "검색된 영화가 없습니다."

    if len(movies) == 0:
        st.info(empty_message)
    else:
        table = []

        for movie in movies:
            table.append(
                {
                    "ID": movie[0],
                    "제목": movie[1],
                    "감독": movie[2],
                    "개봉연도": movie[3],
                }
            )

        st.dataframe(
            table,
            width="stretch",
            hide_index=True,
        )


# 3. 외부 영화 검색
elif menu == "외부 영화 검색":
    st.header("외부 영화 검색")

    keyword = st.text_input(
        "검색할 영화 제목",
        key="external_keyword",
    )

    if st.button("검색"):
        st.session_state["search_results"] = []

        with st.spinner("영화 정보를 검색하고 있습니다..."):
            results, status = search_external_movies(keyword)

        if status == "EMPTY":
            st.warning("검색어를 입력하세요.")

        elif status == "NETWORK_ERROR":
            st.error("네트워크 오류가 발생했습니다.")

        elif status == "SUCCESS":
            st.session_state["search_results"] = results
            st.success("검색이 완료되었습니다.")

        elif status == "DATA_ERROR":
            st.error("응답 데이터를 처리할 수 없습니다.")

        else:
            st.info("검색 결과가 없습니다.")

    # 4. 검색 결과 표시 및 선택
    results = st.session_state["search_results"]

    if len(results) > 0:
        st.subheader("검색 결과")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True,
        )

        selected_index = st.selectbox(
            "저장할 영화",
            options=range(len(results)),
            format_func=lambda index: (
                f"{results[index]['title']} / "
                f"{results[index]['director']} / "
                f"{results[index]['year']}"
            ),
        )

        selected_movie = results[selected_index]

        st.subheader("선택한 영화")
        st.write("제목:", selected_movie["title"])
        st.write("감독:", selected_movie["director"])
        st.write("개봉연도:", selected_movie["year"])

        # 5. 선택한 영화 저장
        if st.button("내 영화 목록에 저장"):
            add_movie(
                selected_movie["title"],
                selected_movie["director"],
                selected_movie["year"],
            )

            st.success("내 영화 목록에 저장했습니다.")
