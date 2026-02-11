from django.db import models


class ModelNames(models.Model):
    """
    Represents model names with their full and short versions.
    Used as a reference table for product models.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'model_names'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Production_codes(models.Model):
    """
    Stores production codes with their associated names and nameplate indicators.
    """
    code = models.IntegerField(db_column='code', primary_key=True)
    name = models.CharField(max_length=70, db_column='name')
    nameplate = models.BooleanField(db_column='nameplate')

    class Meta:
        managed = False
        db_table = 'production_codes'
        ordering = ['-code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Models(models.Model):
    """
    Main product model containing all technical specifications and attributes.
    Relates to ModelNames and Production_codes.
    """
    omega_model_id = models.IntegerField()
    omega_variant_id = models.IntegerField()
    production_code = models.ForeignKey(Production_codes, on_delete=models.CASCADE, db_column='production_code')
    code = models.IntegerField()
    name = models.ForeignKey(ModelNames, on_delete=models.CASCADE, db_column='name_id')
    diagonal = models.FloatField()
    weight = models.IntegerField()
    quantity = models.IntegerField()
    product_warranty = models.IntegerField()
    storage_warranty = models.IntegerField()
    variant_code = models.CharField(max_length=20)
    design_code = models.CharField(max_length=20)
    letter_part = models.CharField(max_length=25)
    numeric_part = models.CharField(max_length=20)
    execution_part = models.CharField(max_length=10)
    relevance = models.BooleanField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'models'
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} (Code: {self.code})"


class Consignments(models.Model):
    """
    Represents product consignments with import declaration information.
    """
    model_name = models.ForeignKey(ModelNames, on_delete=models.CASCADE, db_column='model_name_id')
    quantity = models.IntegerField()
    used_quantity = models.IntegerField()
    declaration_number = models.CharField(max_length=50)
    declaration_date = models.DateTimeField()
    G32 = models.SmallIntegerField()
    is_gift = models.BooleanField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'consignments'
        ordering = ['id']

    def __str__(self):
        return f"Consignment {self.declaration_number}"


class Colors(models.Model):
    """
    Color reference table containing color codes and their descriptions.
    """
    color_code = models.CharField(
        max_length=4, db_column='color_code', blank=True, null=True)
    russian_title = models.CharField(
        max_length=50, db_column='russian_title', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colors'
        ordering = ['id']

    def __str__(self):
        return f"{self.color_code} - {self.russian_title}"


class Products(models.Model):
    """
    Individual product items with barcodes, colors, and inventory information.
    """
    barcode = models.CharField(max_length=18)
    color_id = models.ForeignKey(Colors, on_delete=models.CASCADE, db_column='color_id')
    model = models.ForeignKey(Models, on_delete=models.CASCADE, db_column='model_id')
    consignment = models.ForeignKey(
        Consignments,
        on_delete=models.CASCADE,
        db_column='consignment_id',
        blank=True,
        null=True)
    state = models.IntegerField()
    nameplate = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    cleared = models.ForeignKey(
        'sez.ClearanceInvoice',
        on_delete=models.SET_NULL,
        db_column='cleared',
        null=True,
        blank=True,
        related_name='products',
        db_constraint=False
    )

    class Meta:
        managed = False
        db_table = 'products'
        ordering = ['-id']

    def __str__(self):
        return f"Product {self.barcode}"


class Modules(models.Model):
    """
    Module reference table for product components.
    """
    number = models.IntegerField(db_column='number')
    digit = models.IntegerField(db_column='digit')

    class Meta:
        managed = False
        db_table = 'modules'
        ordering = ['-id']

    def __str__(self):
        return f"Module {self.number}-{self.digit}"


class ModelColors(models.Model):
    """
    Junction table linking Models to their available Colors (many-to-many relationship).
    """
    model_id = models.ForeignKey(Models, on_delete=models.CASCADE, db_column='model_id')
    color_id = models.ForeignKey(Colors, on_delete=models.CASCADE, db_column='color_id')

    class Meta:
        managed = False
        db_table = 'model_colors'
        ordering = ['-id']

    def __str__(self):
        return f"{self.model_id} - {self.color_id}"


class TypesOfWork(models.Model):
    """
    Type of work reference table for product components.
    """
    name = models.CharField(max_length=20, db_column='name')
    order = models.SmallIntegerField(db_column='order')

    class Meta:
        managed = False
        db_table = 'types_of_work'
        ordering = ['id']


class Workplaces(models.Model):
    """
    Workplace reference table for product components.
    """
    housing = models.CharField(max_length=3, db_column='housing')
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, db_column='module_id')
    type_of_work = models.ForeignKey(TypesOfWork, on_delete=models.CASCADE, db_column='type_of_work_id')
    computer_number = models.CharField(max_length=2, db_column='computer_number')
    create_at = models.DateTimeField(db_column='create_at')
    version = models.CharField(max_length=10, db_column='version')

    class Meta:
        managed = False
        db_table = 'workplaces'
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}"


class invoices(models.Model):
    """
    Invoices
    """
    invoice_number = models.IntegerField(db_column='invoice_number')
    recipient = models.SmallIntegerField(db_column='recipient_id')

    class Meta:
        managed = False
        db_table = 'invoices'
        ordering = ['-id']

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class Protocols(models.Model):
    """
    Protocol reference table for product components.
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='product_id')
    workplace = models.ForeignKey(Workplaces, on_delete=models.CASCADE, db_column='workplace_id')
    work_date = models.DateField(db_column='work_date')
    shift = models.CharField(max_length=1, db_column='shift')
    invoice = models.ForeignKey(invoices, on_delete=models.CASCADE, db_column='invoice_id')
    create_at = models.DateTimeField(db_column='create_at')

    class Meta:
        managed = False
        db_table = 'protocols'
        ordering = ['-id']

    def __str__(self):
        return f"Protocol {self.id}"


class ProductTransitions(models.Model):
    """
    Table that contain change product barcode
    """
    old_product = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        db_column='old_product_id',
        related_name='old_product_transitions',
        primary_key=True,
    )
    new_product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        db_column='new_product_id',
        related_name='new_product_transitions'
    )
    # action = models.ForeignKey()

    class Meta:
        managed = False
        db_table = 'product_transitions'
        auto_created = False

    def __str__(self):
        return f"Transition {self.old_product} {self.new_product}"


class ScoreboardView(models.Model):
    """
    Score board view
ALTER VIEW scoreboard_data AS
SELECT
    p.[shift],
    m.[digit] as module_digit,
    p.[work_date],
    COUNT(DISTINCT p.[product_id]) as quantity
FROM [protocols] p
JOIN [products] pr ON p.[product_id] = pr.[id]
JOIN [workplaces] w ON p.[workplace_id] = w.[id]
JOIN [modules] m ON w.[module_id] = m.[id]
WHERE
    pr.[state] = 0
    AND w.type_of_work_id = 2
    AND NOT EXISTS (
        SELECT 1
        FROM [product_transitions] pt
        WHERE (pt.old_product_id = pr.id OR
               (pt.new_product_id = pr.id AND pt.action_id = 2))
    )
GROUP BY
    p.[shift],
    m.[digit],
    p.[work_date];
    """
    shift = models.CharField(max_length=1, db_column='shift')
    module_digit = models.IntegerField(db_column='module_digit')
    work_date = models.DateField(db_column='work_date')
    quantity = models.IntegerField(db_column='quantity', primary_key=True)

    class Meta:
        managed = False
        db_table = 'scoreboard_data'
        ordering = ['module_digit']

    def __str__(self):
        return f"Scoreboard {self.shift} {self.module_digit} {self.work_date} {self.quantity}"
