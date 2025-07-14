from django import template

register = template.Library()

@register.simple_tag
def first_error(form):
    for field in form:
        if field.errors:
            return field.errors[0]

    if form.non_field_errors():
        return form.non_field_errors()[0]

    return "Ocorreu um erro inesperado, por favor tente mais tarde."
