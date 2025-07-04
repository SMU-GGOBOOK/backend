from django.shortcuts import render
import requests
from .models import Book
import urllib.parse


def search(request):
    query = request.GET.get('query', '').strip() or '아름다운'
    query_lower = query.lower()
    books = []
    apipage = 1
    total_count = 0

    if query:
        headers = {
            "Authorization": "KakaoAK 5262b6fed76275833a5b8806921d6af1"
        }

        while True:
            params = {
                "query": query,
                "size": 30,
                "page": apipage,
            }

            response = requests.get("https://dapi.kakao.com/v3/search/book", headers=headers, params=params)

            if response.status_code != 200:
                print("❌ API 오류:", response.status_code)
                print("에러 내용:", response.text)
                break

            data = response.json()
                        
            documents = data.get('documents', [])

            for doc in documents:
                title = doc.get('title', '')
                author = ", ".join(doc.get('authors', []))
                publisher = doc.get('publisher', '')
                thumbnail_url = doc.get('thumbnail', '')
                book_url = doc.get('url', '')

                # 고화질 이미지 추출
                if 'fname=' in thumbnail_url:
                    cover = urllib.parse.unquote(thumbnail_url.split("fname=")[-1])
                else:
                    cover = thumbnail_url

                pub_date_raw = doc.get('datetime', '')
                pub_date = pub_date_raw[:10] if pub_date_raw else None

                isbn_raw = doc.get('isbn', '')
                isbn = isbn_raw.split()[-1] if isbn_raw else None

                # 대소문자 구분 없이 정확히 title 또는 author 안에 query 포함 여부 확인
                if query_lower in title.lower() or query_lower in author.lower():
                    if not Book.objects.filter(title=title, publisher=publisher).exists():
                        Book.objects.create(
                            title=title,
                            author=author,
                            publisher=publisher,
                            cover=cover,
                            pub_date=pub_date,
                            ISBN=isbn
                        )
                    books.append({
                        'title': title,
                        'author': author,
                        'publisher': publisher,
                        'cover': cover,
                        'book_url': book_url
                    })
                    total_count += 1


            if data.get('meta', {}).get('is_end'):
                break

            apipage += 1

    # total_count 정리 (천 단위 쉼표 추가)
    filtered_total_count = f"{total_count:,}"

    page = int(request.GET.get('page', 1))
        # page 변수는 이미 있음
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    list = books[start:end]  # API 원본 필터링 리스트에서 페이징
    
    total_pages = (total_count + per_page - 1) // per_page

    block_size = 5
    block_num = (page - 1) // block_size
    block_start = block_num * block_size + 1
    block_end = min(block_start + block_size - 1, total_pages)

    page_range = range(block_start, block_end + 1)

    context = {
        'books': list,
        'query': query,
        'page_range': page_range,
        'block_start': block_start,
        'block_end': block_end,
        'has_prev_block': block_start > 1,
        'has_next_block': block_end < total_pages,
        'prev_block_page': block_start - 1,
        'next_block_page': block_end + 1,
        'total_count': filtered_total_count,
    }


    return render(request, 'booksearch/booksearch.html', context)

def detail(request, title, author):
    print("넘어온 데이터 : ", title, author)
    try:
        book = Book.objects.get(title=title, author=author)
    except Book.DoesNotExist:
        return render(request, 'booksearch/404.html', status=404)

    return render(request, 'booksearch/bookdetail.html', {'book': book,})
