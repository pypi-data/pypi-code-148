from datetime import datetime

from djangocms_blog.views import PostDetailView, PostListView


class AgendaDetailView(PostDetailView):
    ...


class AgendaAndPostListView(PostListView):
    def get_queryset(self):
        qs = super().get_queryset()
        if "agenda" in self.config.template_prefix:
            return qs.order_by("extension__event_date").filter(
                extension__event_date__gt=datetime.now()
            )
        return qs


class AgendaPreviousEventsListView(PostListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-extension__event_date").filter(
            extension__event_date__lt=datetime.now()
        )
