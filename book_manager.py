import json
from book import Book

class BookManager:
  def __init__(self, filename='books.json'):
    # 여러 Book 객체를 저장하는 리스트
    self.filename = filename
    self.books = []
    self.load_books()

  def save_books(self):
    data = []  #여러권 저장하는 리스트

    for book in self.books:
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