from django.db import models


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Declaration(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    declaration_number = models.CharField(max_length=18)
    permit_number = models.CharField(max_length=23)
    declaration_date = models.DateTimeField()
    provision_date = models.DateTimeField()
    document_id = models.CharField(max_length=36)
    type_code = models.CharField(max_length=3)
    type = models.CharField(max_length=3)
    permit_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=17)
    sender = models.CharField(max_length=38)
    sender_address = models.CharField(max_length=250)
    sender_country_code = models.CharField(max_length=3)
    sender_country_name = models.CharField(max_length=17)
    sender_alpha_country_code = models.CharField(max_length=2)
    g15A_1 = models.CharField(max_length=4)
    delivery_terms = models.CharField(max_length=3)
    item_count = models.IntegerField()
    payment_currency_code = models.CharField(max_length=3)
    total_cost = models.DecimalField(max_digits=19, decimal_places=4)
    currency_rate = models.DecimalField(max_digits=19, decimal_places=4)
    dollar_rate = models.DecimalField(max_digits=19, decimal_places=4)
    euro_rate = models.DecimalField(max_digits=19, decimal_places=4)
    foreign_economic_code = models.CharField(max_length=2)
    payment_type_code = models.CharField(max_length=3)
    paid_payment_details_count = models.SmallIntegerField()
    receiver = models.CharField(max_length=38)
    receiver_address = models.CharField(max_length=250)
    declarant_position = models.CharField(max_length=250)
    declarant_FIO = models.CharField(max_length=250)
    outgoing_number = models.CharField(max_length=50)

    def __str__(self):
        return self.declaration_number or "Unnamed Declaration"
