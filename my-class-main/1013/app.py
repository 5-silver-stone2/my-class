import streamlit as st

from database import (create_table, 
                      add_book, 
                      get_all_books, 
                      update_rating, 
                      toggle_finished, 
                      delete_book,
                      search_books)

from api import search_external_books

create_table()

def print_books(rows):
  if len(rows) == 0:
    st.info('등록된 책이 없습니다.')
    return

  st.write(f'총 {len(rows)}권')

  for row in rows:
    book_id = row[0]
    title = row[1]
    author = row[2]
    rating = row[3]
    finished = row[4]

    if finished == 1 : status = '완료'
    else: status = '읽는 중'

    if rating == 0: rating_text = '평점 없음'
    else: rating_text = f"{rating}점"

    with st.container(border=True):
      st.subheader(f'{book_id}. {title}')
      st.caption(f'{author} · {status} · {rating_text}')

      col1, col2, col3, col4 = st.columns(4)
      with col1:
        toggle_label = "독서 완료 처리" if finished == 0 else "독서 중으로 변경"
        if st.button(toggle_label, key=f"toggle_{book_id}"):
          toggle_finished(book_id)
          st.toast(f"'{title}'의 독서 상태가 변경되었습니다.")
          st.rerun()
      with col2:
        current_rating = rating if 1 <= rating <= 5 else 1
        new_rating = st.selectbox(
          "평점 선택",
          options=[1, 2, 3, 4, 5],
          index=current_rating - 1,
          key=f"rate_sel_{book_id}",
          label_visibility="collapsed",
        )
      with col3:
        if st.button("평점 수정", key=f"rate_btn_{book_id}"):
          update_rating(book_id, new_rating)
          st.toast(f"'{title}'의 평점이 {new_rating}점으로 수정되었습니다.")
          st.rerun()
      with col4:
        if st.button("삭제", key=f"delete_{book_id}"):
          delete_book(book_id)
          st.toast(f"'{title}' 책이 삭제되었습니다.")
          st.rerun()

def print_search_results(results):
    if len(results) == 0:
        st.info('검색 결과가 없습니다.')
        return
    
    st.subheader('\n=========검색 결과=========')
    
    for index, book in enumerate(results, start=1):
        title = book['title']
        author = book['author']
        st.success(f"{index}. {title} / {author}")
        col_info, col_save = st.columns([4, 1])
        with col_info:
          st.markdown(f"**{index}. {title}** / {author}")
        with col_save:
          if st.button("내 서제에 저장", key=f"save_{index}", use_container_width=True):
            try:
              add_book(title, author)
              st.toast(f"'{title}' 책이 내 서제에 저장되었습니다.")
            except Exception as e:
              st.error(f"책 저장 중 오류가 발생했습니다. {e}")
        st.divider()

st.set_page_config(page_title="독서 기록 관리 시스탬", page_icon="📚", layout="wide")

st.sidebar.title("독서 기록 관리")
st.sidebar.write("나만의 독서기록 관리")

menu = st.sidebar.radio("메뉴 선택", 
                        ["내 서제(목록/관리)", "직접 도서 등록", "외부도서 검색 및 등록"]) 
if menu == "내 서제(목록/관리)":
    st.header("📖내 서제")
    st.write("내 서제 목록을 확인하고 관리할 수 있습니다.")

    keyword = st.text_input("책 제목 검색", placeholder="검색할 책 제목을 입력하세요")
    
    if keyword.strip():
        rows = search_books(keyword.strip())
    else:
       rows = get_all_books()
    print_books(rows)
    
elif menu == "직접 도서 등록":
    st.header("직접 도서 등록")
    st.write("책 제목과 저자를 입력하여 직접 도서를 등록할 수 있습니다.")

    with st.form(key='add_book_form', clear_on_submit=True):
        title = st.text_input("책 제목", placeholder="책 제목을 입력하세요")
        author = st.text_input("저자", placeholder="저자를 입력하세요" )
        submit_button = st.form_submit_button(label='등록')

        if submit_button:
            if title.strip() == '' or author.strip() == '':
                st.warning("책 제목과 저자를 모두 입력하세요.")
            else:
                add_book(title.strip(), author.strip())
                st.success(f"'{title}' 책이 등록되었습니다.")   

elif menu == "외부도서 검색 및 등록":
    st.header("외부도서 검색 및 등록")
    st.write("외부 도서 API를 통해 책 제목이나 저자를 검색하고, 검색 결과에서 원하는 책을 선택하여 내 서제에 등록할 수 있습니다.")

    search_col, btn_col = st.columns([4, 1])
    with search_col:
      keyword = st.text_input("검색할 책제목 입력", placeholder="책 제목이나 저자를 입력하세요",
      label_visibility="collapsed")

    with btn_col:
      search_clicked = st.button("도서검색", use_container_width=True)

    if search_clicked:
      if keyword.strip() == "":
        st.warning("검색어를 입력하세요.")
      
      else:
        try:
          results = search_external_books(keyword.strip())
          st.session_state['search_results'] = results
        except Exception as e:
          st.error(f"외부 도서 검색 중 오류가 발생했습니다. {e}")
          st.session_state['search_results'] = []

    if 'search_results' in st.session_state:
      results = st.session_state['search_results']
      print_search_results(results)