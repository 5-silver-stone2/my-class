import requests

API_URL = 'https://itunes.apple.com/search?media=music&entity=song&country=US'

def search_external_songs(keyword):
    if keyword.strip() == '':
        return []

    params = {
        'term': keyword,
        'limit': 5
    }
    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        print(f'네트워크 오류가 발생했습니다: {error}')
        return []
    except ValueError:
        print('응답 데이터를 처리하는 중 오류가 발생했습니다.')
        return []
    results = []

    for item in data.get('results', []):
        song = {
            'title': item.get('trackName', '제목없음'),
            'artist': item.get('artistName', '가수없음'),
            'collectionName': item.get('collectionName', '앨범없음')
        }
        song['album'] = song.pop('collectionName')
        results.append(song)

    return results
