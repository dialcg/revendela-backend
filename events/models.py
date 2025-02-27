from django.db import models


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "Venue"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Organizer"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Nombre"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Descripción"
    )
    start_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de inicio", null=False, blank=False
    )
    end_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de finalización", null=False, blank=False
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lugar del evento",
    )
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Categoria",
    )
    image = models.ImageField(
        upload_to="event-images/",
        null=True,
        blank=True,
        verbose_name="Imagen del evento",
    )
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Organizador",
    )

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = "Event"

    def __str__(self):
        return self.name
