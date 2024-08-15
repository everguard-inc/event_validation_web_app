from django.contrib import admin

from events.models import Project, Tag, Event, EventDownloadBatch


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    fieldsets = (
        ('Metadata', {
            'fields': (
                'name',
                'slug',
                'validation_guide_link',
                'is_deleted',
            )
        }),
        ('Date & Time', {
            'fields': (
                'created_at',
                'updated_at'
            )
        })
    )
    list_display = ('name', 'validation_guide_link')
    ordering = ('slug', 'updated_at')
    readonly_fields = ('updated_at', 'created_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
            'fields': (
                'id',
                'name',
                'project',
                'is_deleted',
            )
        }),
        ('Date & Time', {
            'fields': (
                'created_at',
                'updated_at',
            )
        })
    )
    list_display = ('name', 'project')
    ordering = ('id', )
    readonly_fields = ('id', 'updated_at', 'created_at')


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
                'is_deleted',
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
        }),
        ('Date & Time', {
            'fields': (
                'created_at',
                'updated_at'
            )
        })
    )
    list_display = ('id', 'uid', 'link', 'datetime', 'validated', 'project', 'created_at', 'updated_at')
    list_filter = ('portal_status', 'internal_status')
    search_fields = ('uid', 'project__name')
    ordering = ('-datetime', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(EventDownloadBatch)
class EventDownloadBatchAdmin(admin.ModelAdmin):
    list_display = ('requester', 'link', 'status', 'is_deleted')
    list_filter = ('status', )
    ordering = ('id', )
    readonly_fields = ('id', 'updated_at', 'created_at')
