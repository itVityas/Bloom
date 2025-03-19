from django.db import models


class Order(models.Model):
    """
    Model representing an order.
    """
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Order."""
        return self.name


class Container(models.Model):
    """
    Model representing a container.
    """
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='containers'
    )
    name = models.CharField(max_length=30)
    suppose_date = models.DateField()
    load_date = models.DateField(blank=True, null=True)
    exit_date = models.DateField()
    delivery = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20, default="Created")
    notice = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Container."""
        return self.name


class Content(models.Model):
    """
    Model representing content associated with a container.
    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    count = models.PositiveIntegerField()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name='contents'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Content."""
        return self.shot_name
