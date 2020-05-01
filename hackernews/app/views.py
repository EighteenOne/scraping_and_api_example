from typing import Iterable, List, Dict, Any

from hackernews.app.models import Post


def json_posts(posts: Iterable[Post]) -> List[Dict[str, Any]]:
    """
    Views of posts from database models for API
    Args:
        posts: list with Post objects

    Returns: list with Post as dict

    """
    result = []

    for post in posts:
        result.append({
            'id': post.id,
            'title': post.title,
            'url': post.url,
            'created': post.created.isoformat()
        })

    return result
