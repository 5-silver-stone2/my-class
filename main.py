from book_manager import BookManager

def show_menu():
  print('1. 책 등록')
  print('2. 책 목록 보기')
  print('3. 평점 입력')
  print('4. 독서 완료 처리')
  print('5. 책 삭제')
  print('6. 책 검색')
  print('7. 독서 통계')
  print('0. 종료')

def main():
  manager = BookManager()

  while True:
    print()
    show_menu()

    choice = input("메뉴 번호를 입력하세요: ").strip()
    print()

    if choice == "1":
      title = input("책 제목: ").strip()
      author = input("저자: ").strip()

      if title == "" or author == "":
        print("책 제목과 저자를 모두 입력하세요.")
      else:
        manager.add_book(title, author)

    elif choice == "2":
      manager.show_books()

    elif choice == "3":
      if len(manager.books) == 0:
        print("등록된 책이 없습니다.")
        continue

      manager.show_books()

      try:
        number = int(input("평점을 입력할 책 번호: "))
        rating = int(input("평점(1~5): "))
        manager.set_rating(number, rating)
      except ValueError:
        print("책 번호와 평점은 숫자로 입력하세요.")

    elif choice == "4":
      if len(manager.books) == 0:
        print("등록된 책이 없습니다.")
        continue

      manager.show_books()

      try:
        number = int(input("완료 처리할 책 번호: "))
        manager.finish_book(number)
      except ValueError:
        print("책 번호는 숫자로 입력하세요.")

    elif choice == "5":
      if len(manager.books) == 0:
        print("등록된 책이 없습니다.")
        continue

      manager.show_books()

      try:
        number = int(input("삭제할 책 번호: "))
        manager.delete_book(number)
      except ValueError:
        print("책 번호는 숫자로 입력하세요.")

    elif choice == "6":
      keyword = input("검색할 책 제목 또는 저자: ")
      manager.search_book(keyword)

    elif choice == "7":
      manager.show_stats()

    elif choice == "0":
      print("프로그램을 종료합니다.")
      break

    else:
      print("0부터 7까지의 메뉴 번호를 입력하세요.")
if __name__=='__main__':
  main()