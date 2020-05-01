from hackernews.app import parser


async def test_extract_post_ok(api_client, db_without_data, html_15_items_test):
    resp = await api_client.get('/posts')
    assert resp.status == 200
    data = await resp.json()
    assert len(data) == 0

    await parser.extract_posts(html_15_items_test)

    resp = await api_client.get('/posts?limit=30')
    assert resp.status == 200
    data = await resp.json()
    assert len(data) == 15



