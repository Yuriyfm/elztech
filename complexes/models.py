from django.db import models

import uuid


class Complex(models.Model):
    """Модель сущности Complex"""

    name = models.CharField(max_length=150, verbose_name='Имя комплекса')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "complexes"
