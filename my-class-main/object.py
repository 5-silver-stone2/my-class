class Object:
  def __init__(self, title, date, rating = 0, finished = False, review = ''):
    self.title = title
    self.date = date
    self.rating = 0
    self.finished = False
    self.review = review

  def to_dict(self):
    return{
      'title':self.title,
      'date':self.date,
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
    return "대여중"

  def get_rating_text(self):
    if self.rating == 0:
      return "평점 없음"
    return f"{self.rating}점"

  def get_info(self):
    return (
        f"[{self.get_status()}] "
        f"{self.title} / "
        f"{self.date} / "
        f"{self.get_rating_text()}"
    )


Object1 = Object('컴퓨터', '2026-09-01')

print(Object1.finished)
Object1.finish()
print(Object1.finished)
