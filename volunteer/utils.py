import datetime
from volunteer.models import Tag, Recruitment, DailyRecruitmentStatus


def update_tag(tags: str, recruitment: Recruitment):
    tags = tags.split(',')
    for tag in tags:
        if not tag:
            break
        elif len(tag) < 2:
            continue
        else:
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(text=tag)
            recruitment.tags.add(tag)


def save_daily_recruitment_objects(shelter, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    while start_date <= end_date:
        DailyRecruitmentStatus.objects.get_or_create(shelter=shelter, date=start_date)
        start_date += datetime.timedelta(days=1)
