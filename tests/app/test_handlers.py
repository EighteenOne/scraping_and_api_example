import pytest

from tests.conftest import TEST_POSTS


async def test_get_posts_with_empty_ok(api_client, db_without_data):
    resp = await api_client.get('/posts')
    assert resp.status == 200
    data = await resp.json()
    assert [] == data


async def test_get_posts_with_default_params_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts')
    assert resp.status == 200
    data = await resp.json()
    assert len(data) == 5

    # default limit=5 offset=0 order=id order_type=asc
    assert data == TEST_POSTS[0:5]


async def test_get_posts_with_all_params_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=id:desc&limit=15&offset=1')
    assert resp.status == 200
    data = await resp.json()
    assert len(data) == 9

    expected_data = sorted(TEST_POSTS, key=lambda x: x['id'], reverse=True)

    assert data == expected_data[1:]


@pytest.mark.parametrize(
    "limit",
    [0, 1, 10, 30]
)
async def test_get_posts_with_limit_ok(api_client, db_with_10_posts, limit):
    resp = await api_client.get(f'/posts?limit={limit}')
    assert resp.status == 200
    data = await resp.json()

    expected_len = 10 if limit > 10 else limit  # 10 posts in current db

    assert len(data) == expected_len

    assert data == TEST_POSTS[0:expected_len]


@pytest.mark.parametrize(
    "offset",
    [0, 1, 10, 30]
)
async def test_get_posts_with_offset_ok(api_client, db_with_10_posts, offset):
    resp = await api_client.get(f'/posts?offset={offset}&limit=30')  # with max limit=30
    assert resp.status == 200
    data = await resp.json()

    expected_len = 0 if offset > 10 else 10 - offset  # 10 posts in current db

    assert len(data) == expected_len

    assert data == TEST_POSTS[offset:]


@pytest.mark.parametrize(
    "limit, offset, expected_len",
    [(0, 0, 0), (11, 1, 9), (30, 0, 10), (1, 30, 0), (10, 30, 0)]
)
async def test_get_posts_with_limit_and_offset_ok(api_client, db_with_10_posts, limit, offset, expected_len):
    resp = await api_client.get(f'/posts?offset={offset}&limit={limit}')
    assert resp.status == 200
    data = await resp.json()

    assert len(data) == expected_len


async def test_get_postst_with_order_by_id_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=id')
    assert resp.status == 200
    data = await resp.json()

    assert data == TEST_POSTS[0:5]


async def test_get_postst_with_order_by_title_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=title')
    assert resp.status == 200
    data = await resp.json()

    expected_data = sorted(TEST_POSTS, key=lambda x: x['title'])
    assert data == expected_data[0:5]


async def test_get_postst_with_order_by_url_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=url')
    assert resp.status == 200
    data = await resp.json()

    # sorting in postgres: 'https://test10.com' > 'https://test1.com'
    expected_data = [
        {'id': 10, 'title': 'Test 10', 'url': 'https://test10.com', 'created': '2020-05-01T00:16:22.350241'},
        {'id': 1, 'title': 'Test 1', 'url': 'https://test1.com', 'created': '2020-05-01T00:16:22.281146'},
        {'id': 2, 'title': 'Test 2', 'url': 'https://test2.com', 'created': '2020-05-01T00:16:22.306465'},
        {'id': 3, 'title': 'Test 3', 'url': 'https://test3.com', 'created': '2020-05-01T00:16:22.312315'},
        {'id': 4, 'title': 'Test 4', 'url': 'https://test4.com', 'created': '2020-05-01T00:16:22.317698'}]

    assert data == expected_data


async def test_get_posts_with_order_by_created_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=created')
    assert resp.status == 200
    data = await resp.json()

    expected_data = sorted(TEST_POSTS, key=lambda x: x['created'])
    assert data == expected_data[0:5]


async def test_get_posts_with_order_desc_ok(api_client, db_with_10_posts):
    resp = await api_client.get('/posts?order=title:desc')
    assert resp.status == 200
    data = await resp.json()

    expected_data = sorted(TEST_POSTS, key=lambda x: x['title'], reverse=True)
    assert data == expected_data[0:5]


async def test_get_posts_with_param_fail(api_client):
    resp = await api_client.get('/posts?ordered=1')
    text = await resp.text()
    assert resp.status == 400
    assert "Available params: " in text


@pytest.mark.parametrize(
    "limit, offset",
    [(-1, -1), ("2+4", 6), (42, True), (None, 'None'), (31, 0), (0, 31)]
)
async def test_get_posts_with_limit_offset_fail(api_client, limit, offset):
    resp = await api_client.get(f'/posts?limit={limit}&offset={offset}')
    text = await resp.text()
    assert resp.status == 400
    assert text == 'Limit and offset value must be in range 0..30'


async def test_get_posts_with_many_order_key_fail(api_client):
    resp = await api_client.get('/posts?order=id:asc:asc')
    text = await resp.text()
    assert resp.status == 400
    assert text == 'Many order type in one order key'


async def test_get_posts_with_order_key_fail(api_client):
    resp = await api_client.get('/posts?order=rating')
    text = await resp.text()
    assert resp.status == 400
    assert text == 'Order key not available'


async def test_get_posts_with_order_type_fail(api_client):
    resp = await api_client.get('/posts?order=title:descend')
    text = await resp.text()
    assert resp.status == 400
    assert text == 'Order type must be asc or desc'


@pytest.mark.parametrize(
    "url",
    ['/', '/get_posts']
)
async def test_get_posts_with_fake_url_fail(api_client, url):
    resp = await api_client.get(url)
    assert resp.status == 404
