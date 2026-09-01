import json
from object import Object

class ObjectManager:
  def __init__(self, filename='objects.json'):
    
    self.filename = filename
    self.objects = []
    self.load_objects()

  def save_objects(self):
    data = []  #여러 저장하는 리스트

    for object in self.objects:
      data.append(object.to_dict()) #하나를 딕션어리로

    with open(self.filename,'w',encoding='utf-8')as file:
      json.dump(data, file, ensure_ascii=False)

  def add_object(self, title, date):
    # 같은 장비 이미 있는지 확인
    for object in self.objects:
      if object.title == title and object.date == date:
        print("이미 등록된 장비입니다.")
        return False

    new_object = Object(title, date)
    self.objects.append(new_object)
    self.save_objects()
    print(f"'{title}' 장비를 등록했습니다.")
    return True

  def show_objects(self):
    if len(self.objects) == 0:
      print("등록된 장비가 없습니다.")
      return

    for i, object in enumerate(self.objects, start=1):
      print(f"{i}. {object.get_info()}")

  def get_object(self, number):
    index = number - 1

    if 0 <= index < len(self.objects):
      return self.objects[index]

    return None

  def finish_object(self, number):
    object = self.get_object(number)

    if object is None:
      print("해당 번호의 장비가 없습니다.")
      return False

    object.finish()
    self.save_objects()
    print(f"'{object.title}' 장비를 대여 완료 처리했습니다.")
    return True

  def set_rating(self, number, rating):
    object = self.get_object(number)

    if object is None:
      print("해당 번호의 장비가 없습니다.")
      return False

    if object.sef_rating(rating):
      self.save_objects()
      print(f"'{object.title}' 장비의 평점을 {rating}점으로 저장했습니다.")
      return True

    print("평점은 1점부터 5점까지 입력할 수 있습니다.")
    return False

  def delete_object(self, number):
    object = self.get_object(number)

    if object is None:
      print("해당 번호의 장비가 없습니다.")
      return False

    self.objects.remove(object)
    self.save_objects()
    print(f"'{object.title}' 장비를 삭제했습니다.")
    return True

  def search_object(self, keyword):
    keyword = keyword.strip().lower()

    if keyword == "":
      print("검색어를 입력하세요.")
      return []

    result = []

    for object in self.objects:
      if keyword in object.title.lower() or keyword in object.date.lower():
        result.append(object)

    if len(result) == 0:
      print("검색 결과가 없습니다.")
      return result

    print(f"검색 결과: {len(result)}개")
    for i, object in enumerate(result, start=1):
      print(f"{i}. {object.get_info()}")

    return result

  def show_stats(self):
    total = len(self.objects)
    finished_count = 0
    rating_sum = 0
    rating_count = 0

    for object in self.objects:
      if object.finished:
        finished_count += 1

      if object.rating != 0:
        rating_sum += object.rating
        rating_count += 1

    br_count = total - finished_count

    print(f"전체 장비 수: {total}개")
    print(f"대여 완료된 장비 수: {finished_count}개")
    print(f"대여 중인 장비 수: {br_count}개")

    if rating_count > 0:
      average = rating_sum / rating_count
      print(f"평균 평점: {average:.1f}점")
    else:
      print("평균 평점: 평점 없음")

  def load_objects(self):
    try:
        with open(self.filename,'r',encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
      self.objects = []
      return
    except json.JSONDecodeError:
      print('저장파일을 읽을수 없다.')
      self.objects = []
      return
    except OSError:
      print('파일을 불러오는중 오류가 발생했다.')
      self.objects = []
      return
    
    self.objects = []

    for item in data:
      object = Object (
          title=item['title'],
          date=item['date'],
          rating=item.get('rating',0),
          finished=item.get('finished',False),
          review=item.get('review',"")
        )
      self.objects.append(object)