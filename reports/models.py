from dataclasses import dataclass
from datetime import datetime
from typing import List

from django.db import models
import uuid

from accounts.models import BaseModel, Authority


class Category(BaseModel):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ReportType(BaseModel):
    @dataclass
    class ReportTypeData:
        id: uuid.UUID
        updated_at: datetime

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    definition = models.JSONField()
    authorities = models.ManyToManyField(
        Authority,
        related_name="reportTypes",
    )

    @staticmethod
    def filter_by_authority(authority: Authority):
        return ReportType.objects.filter(authorities__in=authority.all_inherits_up())

    @staticmethod
    def check_updated_report_types_by_authority(
        authority: Authority,
        own_report_types: List[ReportTypeData],
    ):
        existing_items = ReportType.filter_by_authority(authority)
        updated_list = []
        removed_list = []
        for report_type in existing_items:
            found = False
            for item in own_report_types:
                if report_type.id == item.id:
                    found = True
                    if report_type.updated_at != item.updated_at:
                        updated_list.append(report_type)
            if not found:
                updated_list.append(report_type)
        for item in own_report_types:
            found = False
            for report_type in existing_items:
                if report_type.id == item.id:
                    found = True
            if not found:
                removed_list.append(report_type)

        return {
            "updated_list": updated_list,
            "removed_list": removed_list,
        }

    def to_data(self):
        return ReportType.ReportTypeData(id=self.id, updated_at=self.updated_at)
