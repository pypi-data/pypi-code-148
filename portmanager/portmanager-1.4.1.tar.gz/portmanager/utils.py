
def get_object_or_none(queryset, *args, **kwargs):
    try:
        return queryset.get(*args, **kwargs)
    except:
        return None