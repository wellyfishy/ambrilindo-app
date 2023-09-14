from django import template

register = template.Library()

@register.filter
def get_total(detail_medali):
    if detail_medali and hasattr(detail_medali, 'id_detailbagan'):
        total_score = detail_medali.id_detailbagan.id_score.first().id_totalscore.filter(number=1).first()
        return total_score.total if total_score else None
    return None