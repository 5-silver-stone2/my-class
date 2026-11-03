# api.py
# 수행평가용 외부 영화 검색 데이터
# 실제 인터넷 요청 대신 아래 데이터로 검색 상황을 재현한다.

TEST_MOVIES = [
    {
        "title": "테스트영화: 봄날의 기록",
        "director": "김하늘",
        "year": 2021,
    },
    {
        "title": "테스트영화: 마지막 여행",
        "director": "이바다",
        "year": 2023,
    },
]


def search_external_movies(keyword):
    """
    반환값: (영화 목록, 상태값)

    SUCCESS       : 검색 결과 있음
    EMPTY         : 빈 검색어 또는 공백만 입력
    NO_RESULT     : 검색 결과 없음
    NETWORK_ERROR : 검색어로 재현하는 네트워크 오류 메시지
    """

    keyword = keyword.strip()

    # 빈 입력 처리
    if keyword == "":
        return [], "EMPTY"

    # 실제 네트워크 오류와 관계없이 검색어로 메시지 표시 상황을 재현
    if keyword == "네트워크오류":
        return [], "NETWORK_ERROR"

    # 평가용 검색 결과 없음 상황 재현
    if keyword == "결과없음":
        return [], "NO_RESULT"

    # 제목 일부로 검색
    movies = []

    for movie in TEST_MOVIES:
        if keyword.casefold() in movie["title"].casefold():
            movies.append(movie.copy())

    if len(movies) == 0:
        return [], "NO_RESULT"

    return movies, "SUCCESS"
