def show_menu():
  print('1. 책 등록')
  print('2. 책 목록 보기')
  print('3. 평점 입력')
  print('4. 독서 완료 처리')
  print('5. 책 삭제')
  print('6. 책 검색')
  print('7. 독서 통계')
  print('0. 종료')

class Book:
  def __init__(self, title, author, rating = 0, finished = False, review = ''):
    self.title = title
    self.author = author
    self.rating = 0
    self.finished = False
    self.review = review

  def to_dict(self):
    return{
      'title':self.title,
      'author':self.author,
      'rating':self.rating,
      'finished':self.finished,
      'review':self.review
    }

  def finish(self):
    self.finished = True

  def sef_rating(self, rating):
    if 1 <= rating <= 5:
      self.rating = rating
      return True
    return False

  def get_status(self):
    if self.finished:
      return "완료"
    return "읽는중"

  def get_rating_text(self):
    if self.rating == 0:
      return "평점 없음"
    return f"{self.rating}점"

  def get_info(self):
    return (
        f"[{self.get_status()}] "
        f"{self.title} / "
        f"{self.author} / "
        f"{self.get_rating_text()}"
    )


Book1 = Book('어린왕자', '생텍쥐페리')

# Book 객체가 정상적으로 동작하는지 확인
print(Book1.finished)
Book1.finish()
print(Book1.finished)

import json

class BookManager:
  def __init__(self, filename='books,json'):
    # 여러 Book 객체를 저장하는 리스트
    self.filename = filename
    self.books = []
    self.load_books()

  def save_books(self):
    data = []  #여러권 저장하는 리스트

    for book in self.book:
      data.append(book.to_dict()) #책 한권을 딕션어리로

    with open(self.filename,'w',encoding='utf-8')as file:
      json.dump(data, file, ensure_ascii=False)

  def add_book(self, title, author):
    # 같은 제목과 저자의 책이 이미 있는지 확인
    for book in self.books:
      if book.title == title and book.author == author:
        print("이미 등록된 책입니다.")
        return False

    new_book = Book(title, author)
    self.books.append(new_book)
    self.save_books()
    print(f"'{title}' 책을 등록했습니다.")
    return True

  def show_books(self):
    if len(self.books) == 0:
      print("등록된 책이 없습니다.")
      return

    for i, book in enumerate(self.books, start=1):
      print(f"{i}. {book.get_info()}")

  def get_book(self, number):
    index = number - 1

    if 0 <= index < len(self.books):
      return self.books[index]

    return None

  def finish_book(self, number):
    book = self.get_book(number)

    if book is None:
      print("해당 번호의 책이 없습니다.")
      return False

    book.finish()
    self.save_books()
    print(f"'{book.title}' 책을 독서 완료 처리했습니다.")
    return True

  def set_rating(self, number, rating):
    book = self.get_book(number)

    if book is None:
      print("해당 번호의 책이 없습니다.")
      return False

    if book.sef_rating(rating):
      self.save_books()
      print(f"'{book.title}' 책의 평점을 {rating}점으로 저장했습니다.")
      return True

    print("평점은 1점부터 5점까지 입력할 수 있습니다.")
    return False

  def delete_book(self, number):
    book = self.get_book(number)

    if book is None:
      print("해당 번호의 책이 없습니다.")
      return False

    self.books.remove(book)
    self.save_books()
    print(f"'{book.title}' 책을 삭제했습니다.")
    return True

  def search_book(self, keyword):
    keyword = keyword.strip().lower()

    if keyword == "":
      print("검색어를 입력하세요.")
      return []

    result = []

    for book in self.books:
      if keyword in book.title.lower() or keyword in book.author.lower():
        result.append(book)

    if len(result) == 0:
      print("검색 결과가 없습니다.")
      return result

    print(f"검색 결과: {len(result)}권")
    for i, book in enumerate(result, start=1):
      print(f"{i}. {book.get_info()}")

    return result

  def show_stats(self):
    total = len(self.books)
    finished_count = 0
    rating_sum = 0
    rating_count = 0

    for book in self.books:
      if book.finished:
        finished_count += 1

      if book.rating != 0:
        rating_sum += book.rating
        rating_count += 1

    reading_count = total - finished_count

    print(f"전체 책 수: {total}권")
    print(f"완독한 책 수: {finished_count}권")
    print(f"읽는 중인 책 수: {reading_count}권")

    if rating_count > 0:
      average = rating_sum / rating_count
      print(f"평균 평점: {average:.1f}점")
    else:
      print("평균 평점: 평점 없음")

  # 선택 확장 활동 2: 완독한 책만 조회
  def show_finished_books(self):
    finished_books = []

    for book in self.books:
      if book.finished:
        finished_books.append(book)

    if len(finished_books) == 0:
      print("완독한 책이 없습니다.")
      return

    for i, book in enumerate(finished_books, start=1):
      print(f"{i}. {book.get_info()}")

  # 선택 확장 활동 4: 제목 또는 저자 기준 정렬
  def sort_books(self, key):
    if key == "title":
      self.books.sort(key=lambda book: book.title)
      return True

    if key == "author":
      self.books.sort(key=lambda book: book.author)
      return True

    return False

  def load_books(self):
    try:
        with open(self.filename,'r',encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
      self.books = []
      return
    except json.JSONDecodeError:
      print('저장파일을 읽을수 없다.')
      self.books = []
      return
    except OSError:
      print('파일을 불러오는중 오류가 발생했다.')
      self.books = []
      return
    
    self.books = []

    for item in data:
      book = Book(
        title=item['title'],
        author=item['author'],
        rating=item.get('rating',0),
        finished=item.get('finished',False),
        review=item.get('review',"")
      )
      self.books.append(book)


# 프로그램 전체에서 사용할 관리자 객체
manager = BookManager()

def run_program():
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

run_program()
