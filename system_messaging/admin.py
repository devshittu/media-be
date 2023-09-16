from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import MessageTemplate

class MessageTemplateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = MessageTemplate
        fields = '__all__'

class MessageTemplateAdmin(admin.ModelAdmin):
    
    form = MessageTemplateForm
    # Fields to be displayed in the list view
    list_display = ('code', 'message_type', 'subject', 'user')
    
    # Fields that can be used for searching
    search_fields = ('code', 'subject', 'description', 'body')
    
    # Filters to be added to the right sidebar
    list_filter = ('message_type', 'user')
    
    # Fields to be prepopulated based on other fields
    prepopulated_fields = {'code': ('subject',)}
    
    # Fields to be displayed in the form view in a specific order
    fields = ('message_type', 'code', 'description', 'subject', 'body', 'user', 'variables')
    
    # Add a rich text editor for the body (optional, requires a package like django-ckeditor)
    # formfield_overrides = {
    #     models.TextField: {'widget': RichTextEditorWidget},
    # }
    
    # Inline editing (if you have related models)
    # inlines = [RelatedModelInline]

admin.site.register(MessageTemplate, MessageTemplateAdmin)
