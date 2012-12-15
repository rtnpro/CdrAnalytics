import json
from django import template
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(is_safe=True)
def render_chart(value):
    if value is None:
        return ""
    template_obj = get_template("raphycharts/charts.html")
    context = Context({
        "plot_data": mark_safe(value.get_json_for_plot()),
        "chart_id": value.chart_id
    })
    return template_obj.render(context)