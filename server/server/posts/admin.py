from django.contrib import admin

from .models import Post, PostImage

admin.site.register(PostImage)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["slug", "creation_time", "event", "author", "content"]
    search_fields = [
        "content",
        "author",
    ]

    def content(self, obj):
        return f"{obj.post_content[:100]}..."
