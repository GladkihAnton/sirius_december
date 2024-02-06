from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'course_id',
        'title',
        'description',
        'author',
        'category',
        'difficulty',
        'course_status',
        'expected_status',
        'method',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            1,
            'Основы программирования на Python',
            'Этот курс представляет собой введение в программирование на языке Python. Он охватывает основы синтаксиса, структуры данных и основные концепции программирования.',
            'Алексей Иванов',
            'Программирование',
            'Начальный',
            'Активный',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            2,
            'Разработка веб-приложений с использованием Django',
            'Курс посвящен разработке веб-приложений на фреймворке Django. Студенты узнают о моделях, представлениях, шаблонах, формах и аутентификации.',
            'Мария Семенова',
            'Веб-разработка',
            'Средний',
            'Ожидающий',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            3,
            'Продвинутые техники в JavaScript',
            'Этот курс знакомит с продвинутыми техниками программирования в JavaScript, включая асинхронное программирование, замыкания, паттерны проектирования и модульность.',
            'Дмитрий Петров',
            'Программирование',
            'Продвинутый',
            'Завершенный',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            1,
            'Основы программирования на Python',
            'Этот курс представляет собой введение в программирование на языке Python. Он охватывает основы синтаксиса, структуры данных и основные концепции программирования.',
            'Алексей Иванов',
            'Программирование',
            'Средний',
            'Активный',
            status.HTTP_403_FORBIDDEN,
            'put',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            2,
            'Разработка веб-приложений с использованием Django',
            'Курс посвящен разработке веб-приложений на фреймворке Django. Студенты узнают о моделях, представлениях, шаблонах, формах и аутентификации.',
            'Мария Семенова',
            'Веб-разработка',
            'Средний',
            'Завершенный',
            status.HTTP_200_OK,
            'put',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            3,
            'Продвинутые техники в JavaScript (обновленный)',
            'Этот курс знакомит с продвинутыми техниками программирования в JavaScript, включая асинхронное программирование, замыкания, паттерны проектирования и модульность.',
            'Дарья Дмитрова',
            'Программирование',
            'Продвинутый',
            'Активный',
            status.HTTP_200_OK,
            'put',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            1,
            'Основы программирования на Python',
            'Этот курс представляет собой введение в программирование на языке Python. Он охватывает основы синтаксиса, структуры данных и основные концепции программирования.',
            'Алексей Иванов',
            'Программирование',
            'Средний',
            'Активный',
            status.HTTP_403_FORBIDDEN,
            'del',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            2,
            'Разработка веб-приложений с использованием Django',
            'Курс посвящен разработке веб-приложений на фреймворке Django. Студенты узнают о моделях, представлениях, шаблонах, формах и аутентификации.',
            'Мария Семенова',
            'Веб-разработка',
            'Средний',
            'Завершенный',
            status.HTTP_204_NO_CONTENT,
            'del',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            3,
            'Продвинутые техники в JavaScript (обновленный)',
            'Этот курс знакомит с продвинутыми техниками программирования в JavaScript, включая асинхронное программирование, замыкания, паттерны проектирования и модульность.',
            'Дарья Дмитрова',
            'Программирование',
            'Продвинутый',
            'Активный',
            status.HTTP_204_NO_CONTENT,
            'del',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_put_delete_course(
    client: AsyncClient,
    username: str,
    password: str,
    course_id: int,
    title: str,
    description: str,
    author: str,
    category: str,
    difficulty: str,
    course_status: str,
    expected_status: int,
    method,
    access_token: str,
) -> None:
    if method == 'get':
        response = await client.get(
            URLS['course']['get_put_del_course_by_id'].format(course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        response_data = response.json()
        assert response_data['title'] == title
        assert response_data['description'] == description
        assert response_data['author'] == author
        assert response_data['category'] == category
        assert response_data['difficulty'] == difficulty
        assert response_data['status'] == course_status
    if method == 'put':
        response = await client.put(
            URLS['course']['get_put_del_course_by_id'].format(course_id=course_id),
            json={
                'title': title,
                'description': description,
                'author': author,
                'category': category,
                'difficulty': difficulty,
                'status': course_status,
            },
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        if response.status_code == 200:
            response_data = response.json()
            assert response_data['title'] == title
            assert response_data['description'] == description
            assert response_data['author'] == author
            assert response_data['category'] == category
            assert response_data['difficulty'] == difficulty
            assert response_data['status'] == course_status
    if method == 'del':
        response = await client.delete(
            URLS['course']['get_put_del_course_by_id'].format(course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        if response.status_code == 204:
            response = await client.get(
                URLS['course']['get_put_del_course_by_id'].format(course_id=course_id),
                headers={'Authorization': f'Bearer Bearer {access_token}'},
            )
            assert response.status_code == status.HTTP_404_NOT_FOUND
