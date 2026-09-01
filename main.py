from object_manager import ObjectManager

def show_menu():
  print('1. 대여장비 등록')
  print('2. 대여장비 목록 보기')
  print('3. 장비 평점 입력')
  print('4. 대여 완료 처리')
  print('5. 대여장비 삭제')
  print('6. 대여장비 검색')
  print('7. 대여장비 통계')
  print('0. 종료')

def main():
  manager = ObjectManager()

  while True:
    print()
    show_menu()

    choice = input("메뉴 번호를 입력하세요: ").strip()
    print()

    if choice == "1":
      title = input("장비 이름: ").strip()
      date = input("날자: ").strip()

      if title == "" or date == "":
        print("장비 이름과 날자를 모두 입력하세요.")
      else:
        manager.add_object(title, date)

    elif choice == "2":
      manager.show_objects()

    elif choice == "3":
      if len(manager.objects) == 0:
        print("등록된 책이 없습니다.")
        continue

      manager.show_objects()

      try:
        number = int(input("평점을 입력할 장비 번호: "))
        rating = int(input("평점(1~5): "))
        manager.set_rating(number, rating)
      except ValueError:
        print("장비 번호와 평점은 숫자로 입력하세요.")

    elif choice == "4":
      if len(manager.objects) == 0:
        print("등록된 장비가 없습니다.")
        continue

      manager.show_objects()

      try:
        number = int(input("완료 처리할 장비 번호: "))
        manager.finish_object(number)
      except ValueError:
        print("장비 번호는 숫자로 입력하세요.")

    elif choice == "5":
      if len(manager.objects) == 0:
        print("등록된 장비가 없습니다.")
        continue

      manager.show_objects()

      try:
        number = int(input("삭제할 장비 번호: "))
        manager.delete_object(number)
      except ValueError:
        print("장비 번호는 숫자로 입력하세요.")

    elif choice == "6":
      keyword = input("검색할 장비이름 또는 날자: ")
      manager.search_object(keyword)

    elif choice == "7":
      manager.show_stats()

    elif choice == "0":
      print("프로그램을 종료합니다.")
      break

    else:
      print("0부터 7까지의 메뉴 번호를 입력하세요.")
if __name__=='__main__':
  main()