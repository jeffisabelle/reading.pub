import re
import math
from collections import Counter
from nltk.corpus import stopwords

from models.models import Post
from models.models import Relation

WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    stops = stopwords.words('english') + stopwords.words('turkish')
    words = [w for w in words if w not in stops]
    return Counter(words)


def get_category_point(p1, p2):
    common_tags = set(p1.tags).intersection(p2.tags)
    if len(common_tags) > 2:
        return 0.35
    elif len(common_tags) == 2:
        return 0.30
    elif len(common_tags) == 1:
        return 0.15
    else:
        return 0


def build_relation_db():
    """
    Build a relation collection that includes
    every similarity between posts.

    Only includes relation when similarity > 0.2

    This takes a lot of time, run this periodically.
    Eg. once a week or everynight.

    Use insert_new_relation() for new posts

    """
    posts = Post.objects()
    posts2 = Post.objects()
    Relation.drop_collection()
    counter = 0
    print counter
    for p1 in posts:
        for p2 in posts2:
            if p1.url != p2.url:
                if p1.post_type != "pdf" and p2.post_type != "pdf":
                    counter = counter + 1

                    # text similarity
                    text1 = p1.content.lower()
                    text2 = p2.content.lower()
                    vector1 = text_to_vector(text1)
                    vector2 = text_to_vector(text2)
                    content_cosine = get_cosine(vector1, vector2)
                    # title similarity
                    title1 = p1.title.lower()
                    title2 = p2.title.lower()
                    tvector1 = text_to_vector(title1)
                    tvector2 = text_to_vector(title2)
                    title_cosine = get_cosine(tvector1, tvector2)

                    category_point = get_category_point(p1, p2)
                    cosine = content_cosine + title_cosine + category_point

                    if cosine > 0.1:
                        relation = Relation(p1, p2, cosine)
                        relation.save()
    print counter


def insert_new_relation(post1):
    """

    Arguments:
    - `post1`: newly added post
    """
    posts = Post.objects()
    if post1.post_type == "pdf":
        return None

    for post2 in posts:
        if post2.post_type != "pdf" and post2.url != post1.url:
            # text similarity
            text1 = post1.content.lower()
            text2 = post2.content.lower()
            vector1 = text_to_vector(text1)
            vector2 = text_to_vector(text2)
            content_cosine = get_cosine(vector1, vector2)
            # title similarity
            title1 = post1.title.lower()
            title2 = post2.title.lower()
            tvector1 = text_to_vector(title1)
            tvector2 = text_to_vector(title2)
            title_cosine = get_cosine(tvector1, tvector2)

            category_point = get_category_point(post1, post2)
            cosine = content_cosine + title_cosine + category_point

            if cosine > 0.1:
                relation = Relation(post1, post2, cosine)
                relation.save()

                relation = Relation(post2, post1, cosine)
                relation.save()


def after_tagging_calculation(post1):
    """

    Arguments:
    - `post1`: tag added to this post
    """
    relation = Relation.objects(post1=post1)
    if post1.post_type == "pdf":
        return None

    for r in relation:
        category_point = get_category_point(r.post1, r.post2)
        r.similarity += category_point
        r.save()

    relation = Relation.objects(post2=post1)
    for r in relation:
        category_point = get_category_point(r.post1, r.post2)
        r.similarity += category_point
        r.save()


def get_related_posts(post1):
    related_posts = Relation.objects(post1=post1).order_by("-similarity")[:4]
    return related_posts


if __name__ == '__main__':
    build_relation_db()
