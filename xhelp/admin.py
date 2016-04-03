from django.contrib import admin

from .models import Help, Comment
class HelpAdmin(admin.ModelAdmin):
	class Meta:
		model = Help

admin.site.register(Help,HelpAdmin)
admin.site.register(Comment)



# Register your models here.
