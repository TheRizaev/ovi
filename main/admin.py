from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsCategory, Partner, JobApplication, ContactMessage

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Содержание', {
            'fields': ('excerpt', 'content', 'image')
        }),
        ('Настройки', {
            'fields': ('is_featured', 'is_published')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новая запись
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'logo')
        }),
        ('Описание', {
            'fields': ('description', 'services', 'contact_info')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'profession', 'experience', 'status', 'created_at']
    list_filter = ['profession', 'experience', 'status', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Личные данные', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Профессиональная информация', {
            'fields': ('profession', 'experience', 'education', 'availability')
        }),
        ('Дополнительно', {
            'fields': ('message', 'status', 'created_at')
        }),
    )
    
    actions = ['mark_as_in_review', 'mark_as_accepted', 'mark_as_rejected']
    
    def mark_as_in_review(self, request, queryset):
        queryset.update(status='in_review')
    mark_as_in_review.short_description = "Отметить как 'На рассмотрении'"
    
    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
    mark_as_accepted.short_description = "Отметить как 'Принята'"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = "Отметить как 'Отклонена'"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'is_read', 'created_at']
    list_filter = ['subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Контактные данные', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Сообщение', {
            'fields': ('subject', 'message')
        }),
        ('Статус', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанные"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Отметить как непрочитанные"

# Кастомизация админки
admin.site.site_header = 'OVI Admin'
admin.site.site_title = 'OVI'
admin.site.index_title = 'Панель управления OVI'