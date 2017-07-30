from django.contrib import admin
import models
# Register your models here.
admin.site.register(models.BandwidthDelay)
admin.site.register(models.HTTPCode)
admin.site.register(models.ReTran)
admin.site.register(models.Source)
admin.site.register(models.PlayRecord)
admin.site.register(models.VideoQuality)