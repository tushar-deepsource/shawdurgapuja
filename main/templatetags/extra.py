from django import template

register = template.Library() 

@register.filter(name='give_correct_object')
def give_correct_object(objects, slice_no):
    object_list = [i for i in objects]
    return object_list[slice_no-1]