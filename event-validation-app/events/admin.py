from django.contrib import admin

from events.models import Project, Tag, Event, EventDownloadBatch


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ('name', 'validation_guide_link')
    list_display = ('name', 'validation_guide_link')
    ordering = ('id', )
    readonly_fields = ('id', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'project')
    list_display = ('name', 'project')
    ordering = ('id', )
    readonly_fields = ('id', )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
            'fields': (
                'id',
                'uid',
                'link',
                'cam_uid',
                'datetime',
                'project',
            )
        }),
        ('Statuses', {
            'fields': (
                'portal_status',
                'internal_status',
                'validated',
                'taken_for_annotation',
            )
        }),
        ('Comments', {
            'fields': (
                'portal_comment',
                'internal_comment'
            )
        }),
        ('Tags', {
            'fields': (
                'major_tag',
                'minor_tag1',
                'minor_tag2',
            )
        })
    )
    list_display = ('id', 'uid', 'link', 'datetime', 'validated', 'project')
    list_filter = ('portal_status', 'internal_status')
    search_fields = ('uid', 'project')
    ordering = ('-datetime', 'id')
    readonly_fields = ('id', )


@admin.register(EventDownloadBatch)
class EventDownloadBatchAdmin(admin.ModelAdmin):
    list_display = ('requester', 'link', 'status')
    list_filter = ('status', )
    ordering = ('id', )
    readonly_fields = ('id', )
