from django.shortcuts import render
import requests
from .models import Book
from bs4 import BeautifulSoup
from django.core.paginator import Paginator


def search(request):
    query = request.GET.get('query', '').strip() or '행복'
    query_lower = query.lower()
    books = []
    apipage = 1

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
                cover = doc.get('thumbnail', '')
                book_url = doc.get('url', '')

                # 날짜 정제: 2017-01-10T00:00:00.000+09:00 → 2017-01-10
                pub_date_raw = doc.get('datetime', '')
                pub_date = pub_date_raw[:10] if pub_date_raw else None

                # ISBN 정제: 978로 시작하는 13자리만 저장
                isbn_raw = doc.get('isbn', '')
                isbn = isbn_raw.split()[-1] if isbn_raw else None

                # 검색 키워드 포함 확인
                if query_lower in title.lower() or query_lower in author.lower():
                    # 중복 저장 방지
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

            if data.get('meta', {}).get('is_end'):
                break

            apipage += 1

    # ✅ 페이지네이션 적용
    page = int(request.GET.get('page', 1))
    qs = Book.objects.all().order_by('title')
    paginator = Paginator(qs, 20)
    list = paginator.get_page(page)

    block_size = 5  # 5개씩 묶음
    block_num = (page - 1) // block_size  # 현재 몇 번째 블록?
    block_start = block_num * block_size + 1
    block_end = min(block_start + block_size - 1, paginator.num_pages)

    page_range = range(block_start, block_end + 1)

    context = {
        'books': list,
        'query': query,
        'page_range': page_range,
        'block_start': block_start,
        'block_end': block_end,
        'has_prev_block': block_start > 1,
        'has_next_block': block_end < paginator.num_pages,
        'prev_block_page': block_start - 1,
        'next_block_page': block_end + 1,
    }


    return render(request, 'booksearch/booksearch.html', context)

def detail(request):
    return render(request, 'booksearch/bookdetail.html')
    