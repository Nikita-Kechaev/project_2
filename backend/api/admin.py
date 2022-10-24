from django.contrib import admin

from .models import (Comment, Gallery, GalleryComment, GalleryFile,
                     GalleryReview, Journal, JournalComment, JournalReview,
                     JournalTag, New, NewComment, NewReview, NewTag, Tag, User)

admin.site.register(User)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'created_at',
    ]
    search_fields = [
        'author',
    ]


@admin.register(JournalComment)
class JournlaCommentAdmin(admin.ModelAdmin):
    list_display = [
        'journal',
    ]


@admin.register(JournalReview)
class JournlaReviewAdmin(admin.ModelAdmin):
    list_display = [
        'journal',
        'user',
        'rate'
    ]


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'title',
        'created_at',
    ]
    search_fields = [
        'author',
    ]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'title',
        'created_at',
    ]
    search_fields = [
        'author',
    ]


@admin.register(GalleryComment)
class GalleryCommentAdmin(admin.ModelAdmin):
    list_display = [
        'comment'
    ]


@admin.register(GalleryReview)
class GalleryReviewAdmin(admin.ModelAdmin):
    list_display = [
        'gallery',
        'user',
        'rate'
    ]


@admin.register(GalleryFile)
class GalleryFileAdmin(admin.ModelAdmin):
    list_display = [
        'type'
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'text'
    ]


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created_at',
    ]
    search_fields = [
        'tags',
    ]


@admin.register(NewComment)
class NewCommentAdmin(admin.ModelAdmin):
    list_display = [
        'comment'
    ]


@admin.register(NewReview)
class NewReviewAdmin(admin.ModelAdmin):
    list_display = [
        'new',
        'user',
        'rate'
    ]


@admin.register(NewTag)
class NewTagAdmin(admin.ModelAdmin):
    list_display = [
        'new',
        'tag'
    ]


@admin.register(JournalTag)
class JournalTagAdmin(admin.ModelAdmin):
    list_display = [
        'journal',
        'tag'
    ]
