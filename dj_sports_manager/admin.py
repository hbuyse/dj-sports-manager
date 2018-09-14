# coding=utf-8

"""Admin."""

from django.contrib import admin

from .models import (
    Category,
    Team,
    Practice,
    License,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'min_age',
        'max_age'
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'category',
        'level',
        'sex'
    )


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'type_practice',
        'day'
    )


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'team',
        'owner',
    )
