from django.contrib import admin
from .models import Post
from django.db.models import Count

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'tag_count')
    date_hierarchy = 'pub_date'
    list_filter = ('pub_date', )
    search_fields = ('title', 'text')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'text')
        }),
        ('Related', {
            'fields': ('tags', 'startups')
        }),
    )
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('startups',)
    filter_vertical = ('tags', )


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(tag_number=Count('tags'))

    def tag_count(self, post):
        return post.tags.count()

    tag_count.short_description = 'Number of Tags'
    tag_count.admin_order_field = 'tag_number'