import arrow
from django import template


register = template.Library()


@register.filter
def accreditation_validity(accreditation, event):
    if accreditation is None or accreditation.date is None:
        return ""
    event_end = arrow.get(event["end"])
    last_valid = event_end.shift(months=-18).date()
    if accreditation.date < last_valid:
        return "bg bg-danger"
    elif (accreditation.date - last_valid).days < 10:
        return "bg bg-warning"
    return ""
