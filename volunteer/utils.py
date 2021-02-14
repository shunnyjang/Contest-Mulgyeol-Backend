from volunteer.models import Tag, Recruitment


def update_tag(tags: str, recruitment: Recruitment):
    tags = tags.split(',')
    for tag in tags:
        if not tag:
            continue
        else:
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(text=tag)
            recruitment.tags.add(tag)
