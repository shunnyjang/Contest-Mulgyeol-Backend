from volunteer.models import Tag


def update_tag(tags, recruitment):
    tags = tags.spilt(',')
    for tag in tags:
        if not tag:
            continue
        else:
            tag = tag.strip()
            tag_, created = Tag.objects.get_or_create(name=tag)
            recruitment.tags.add(tag_)
