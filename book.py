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
