from database import (create_table, 
                      add_song, 
                      get_all_songs, 
                      update_rating, 
                      toggle_finished, 
                      delete_song,
                      search_songs)

from api import search_external_songs

def show_menu():
  print('\n===== 관심 음악 관리 ======')
  print('1. 외부 음악 검색')
  print('2. 외부 음악 검색 후 등록')
  print('3. 음악 목록보기')
  print('4. 음악 검색')
  print('5. 평점 입력') 
  print('6. 음악 삭제')
  print('0. 종료')
  print('=================================')

def input_number(massage):
  try:
    return int(input(massage))
  except ValueError:
    print('숫자를 입력하세요.')
    return None

def print_songs(rows):
  if len(rows) == 0:
    print('등록된 노래가 없습니다.')
    return

  print('\n=========노래 목록=========')

  for row in rows:
    song_id = row[0]
    title = row[1]
    artist = row[2]
    album = row[3]
    rating = row[4]
    
    if rating == 0: rating_text = '평점 없음'
    else: rating_text = f"{rating}점"

    print(f'{song_id}. {title} / {artist} / {album} / {rating_text}')

def print_search_results(results):
    if len(results) == 0:
        print('검색 결과가 없습니다.')
        return
    
    print('\n=========검색 결과=========')
    
    for index, song in enumerate(results, start=1):
        title = song['title']
        artist = song['artist']
        album = song['album'] if 'album' in song else '앨범없음'
        print(f"{index}. {title} / {artist} / {album}")

def main():

    create_table()
    results = []

    while True:

        show_menu()

        menu = input("메뉴 선택: ").strip()

        if menu == "3":
            rows = get_all_songs()
            print_songs(rows)

        elif menu == "5":
            rows = get_all_songs()
            print_songs(rows)

            if len(rows) == 0:
                continue

            song_id = input_number("평점을 수정할 노래 ID: ")

            if song_id is None:
                continue

            rating = input_number("평점 입력 (1~5): ")
            if rating is None:
                continue

            if rating < 1 or rating > 5:
                print("평점은 1~5 사이로 입력하세요.")
                continue

            changed = update_rating(song_id, rating)
            if changed == 0:
                print("해당 ID의 노래가 없습니다.")
            else:
                print("평점이 수정되었습니다.")


        elif menu == "6":
            rows = get_all_songs()
            print_songs(rows)

            if len(rows) == 0:
                continue

            song_id = input_number("삭제할 노래 ID: ")

            if song_id is None:
                continue

            changed = delete_song(song_id)

            if changed == 0:
                print("해당 ID의 노래가 없습니다.")
            else:
                print("노래가 삭제되었습니다.")

        elif menu == "4":
            keyword = input("검색할 노래 제목: ").strip()
            rows = search_songs(keyword)
            print_songs(rows)

        elif menu == "1":
            keyword = input('외부에서 검색할 노래 제목: ').strip()
            
            if keyword == '':
                print('검색어를 입력하세요.')
                continue
            
            results = search_external_songs(keyword)
            print_search_results(results)
            

        elif menu == "2":
            if len(results) == 0:
                print('먼저 1번 메뉴에서 외부 노래를 검색하세요.')
                continue
            
            print_search_results(results)
            
            number = input_number('등록할 노래 번호: ')
            
            if number is None:
                continue
            
            if number < 1 or number > len(results):
                print('올바른 번호를 입력하세요.')
                continue
            
            selected_song = results[number - 1]

            title = selected_song['title']
            artist = selected_song['artist']
            album = selected_song['album']
            
            add_song(title, artist, album)
            print(f"'{title}' 노래가 등록되었습니다.")
        elif menu == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("올바른 메뉴를 선택하세요.")

if __name__ == '__main__':
   main()
