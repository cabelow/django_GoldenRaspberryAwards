from django.contrib import admin
from Core.Movies.models import Movie
from Core.Producers.models import Producer
from Core.Studio.models import Studio


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year", "get_producers", "get_studios")
    search_fields = ("title",)
    list_filter = ("year", "studio")

    @staticmethod
    def get_producers(obj):
        return ", ".join([producer.name for producer in obj.producer.all()])

    @staticmethod
    def get_studios(obj):
        return ", ".join([studio.name for studio in obj.studio.all()])

    get_producers.short_description = "Producers"
    get_studios.short_description = "Studios"
