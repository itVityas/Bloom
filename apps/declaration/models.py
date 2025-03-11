from django.db import models


class Declaration(models.Model):
    """
    Model representing a customs declaration.
    The order of fields corresponds to the column order in the DBF file.
    """
    # Foreign key (not from DBF)
    container = models.ForeignKey(
        'arrival.Container',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='declarations'
    )

    # G011 / Customs declaration type code
    type_code = models.CharField(max_length=3)
    # G012_1 / Type of customs declaration
    type = models.CharField(max_length=3)
    # G022 / Sender company name
    sender = models.CharField(max_length=38)
    # G023 / Sender company address
    sender_address = models.CharField(max_length=250)
    # G20 / Delivery terms short name
    delivery_terms = models.CharField(max_length=3)
    # G05 / Total number of item types
    item_count = models.IntegerField()
    # G082 / Receiver
    receiver = models.CharField(max_length=38)
    # G083 / Receiver address
    receiver_address = models.CharField(max_length=250)
    # G15A / Sender country code
    sender_country_code = models.CharField(max_length=3)
    # G15A_0 / Sender alpha country code
    sender_alpha_country_code = models.CharField(max_length=2)
    # G15A_1 / Additional sender country code information
    g15A_1 = models.CharField(max_length=4)
    # G221 / Payment currency code
    payment_currency_code = models.CharField(max_length=3)
    # G222 / Total invoice cost
    total_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G23 / Foreign currency rate
    currency_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # G241 / Foreign economic operation code
    foreign_economic_code = models.CharField(max_length=2)
    # G242 / Payment type code for the deal
    payment_type_code = models.CharField(max_length=3)
    # G542 / Provision date for EGD
    provision_date = models.DateField()
    # GBN / Count of records in GB.dbf file
    paid_payment_details_count = models.SmallIntegerField()
    # DECL_ID / Unique declaration ID from customs
    declaration_id = models.IntegerField(unique=True)
    # NOM_REG / Declaration number (registration number)
    declaration_number = models.CharField(max_length=18)
    # GA / Permit number or certificate number
    permit_number = models.CharField(max_length=23)
    # G16 / Country of origin for goods
    country_name = models.CharField(max_length=17)
    # G545 / Declarant's position
    declarant_position = models.CharField(max_length=250)
    # G546 / Declarant's full name
    declarant_FIO = models.CharField(max_length=250)
    # DOCUMENTID / Unique document identifier
    document_id = models.CharField(max_length=36)
    # G15 / Sender country short name
    sender_country_name = models.CharField(max_length=17)
    # G544 / Outgoing number in applicant's files
    outgoing_number = models.CharField(max_length=50)
    # G47_KD / Dollar rate
    dollar_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # G47_KS / Euro rate
    euro_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # DATEC / Declaration date
    declaration_date = models.DateField()
    # G013 / Permit code for customs authorization
    permit_code = models.CharField(max_length=3)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Declaration."""
        return self.declaration_number or "Unnamed Declaration"


class DeclaredItem(models.Model):
    """
    Model representing an item declared in a customs declaration.
    Field names correspond to the columns from the DBF file.
    """
    # DECL_ID / Customs declaration number (FK)
    declaration = models.ForeignKey(
        Declaration, on_delete=models.CASCADE, related_name='declared_items'
    )
    # G312 / Commercial or contract item name
    name = models.CharField(max_length=250)
    # G32 / Item ordinal number
    ordinal_number = models.IntegerField()
    # G34 / Country code of origin for the item
    country_code = models.CharField(max_length=3)
    # G34A / Alpha country code of origin for the item
    alpha_country_code = models.CharField(max_length=3)
    # G38 / Gross weight in kg (net weight in kg for some cases)
    gross_weight = models.FloatField()
    # G41 / Quantity in additional measurement units
    quantity = models.FloatField(null=True, blank=True)
    # G41A / Code for additional measurement unit
    unit_code = models.CharField(max_length=10, null=True, blank=True)
    # G41B / Name of additional measurement unit
    unit_name = models.CharField(max_length=20, null=True, blank=True)
    # G42 / Invoice cost in payment currency as specified in G221
    cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G46 / Statistical cost in USD
    statistical_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G47N / Payment details count (related to G47.DBF)
    payment_details_count = models.IntegerField()
    # G44N / Count of records in G44.DBF file
    document_details_count = models.IntegerField()
    # G33 / Customs tariff code (HS code)
    code = models.CharField(max_length=50)
    # G16 / Country of origin as declared in the EGD
    country_name = models.CharField(max_length=17)
    # G37 / Additional field (meaning unclear)
    g37 = models.CharField(max_length=2)
    # G38A / Net weight in kg
    net_weight = models.FloatField()
    # G372 / Code for the previous customs regime
    previous_customs_regime_code = models.CharField(max_length=2)
    # G373 / Additional field (meaning unclear)
    g373 = models.CharField(max_length=3)
    # G45 / Customs cost in local currency
    customs_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G31STZ / Additional field (meaning unclear)
    g31stz = models.CharField(max_length=50)
    # G311STZ / Additional field (meaning unclear)
    g311stz = models.CharField(max_length=3)
    # G312STZ / Additional field (meaning unclear)
    g312STZ = models.CharField(max_length=13)
    # G43 / Valuation method code for customs cost determination
    valuation_method = models.CharField(max_length=2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the DeclaredItem."""
        return f'{self.declaration} - {self.ordinal_number}'