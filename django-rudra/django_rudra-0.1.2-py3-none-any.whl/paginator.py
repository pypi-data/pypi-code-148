from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet
from rudra.settings import RudraBaseSettings
from django.conf import settings

rudrasettings: RudraBaseSettings = settings.RUDRASETTINGS

class PaginatorService:

    def __init__(self, queryset: QuerySet, page: int=1, page_size: int=10, orphans: int=0):
        self.queryset = queryset
        self.page_size = int(f"{page_size}")
        self.page = int(f"{page}")
        self.orphans = orphans
        self.page_obj = None
        self.fixed_page_number = rudrasettings.fixed_page_number
    
    def get_page(self):
        if self.page_obj:
            return self.page_obj

        paginator = Paginator(self.queryset, self.page_size, orphans=self.orphans)
        try:
            page_obj = paginator.page(self.page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        self.page_obj = page_obj
        return self.page_obj
    
    def get_query_set(self):
        return self.get_page().object_list
    
    def get_query_set_count(self):
        if self.fixed_page_number:
            return self.fixed_page_number * self.page_size
        return self.get_page().object_list.count()
    
    def has_next(self):
        if self.fixed_page_number:
            return True
        return self.get_page().has_next()
    
    def pages(self):
        if self.fixed_page_number:
            return self.fixed_page_number
        return self.get_page().paginator.num_pages