from django.db import models


class ModelNames(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'model_names'
        ordering = ['-id']

    def __str__(self):
        return self.shshtrih_consignmentsort_name


class Production_codes(models.Model):
    code = models.IntegerField(db_column='code', primary_key=True)
    name = models.CharField(max_length=70, db_column='name')
    nameplate = models.BooleanField(db_column='nameplate')

    class Meta:
        managed = False
        db_table = 'production_codes'
        ordering = ['-code']


class Models(models.Model):
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
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'models'
        ordering = ['-id']


class Consignments(models.Model):
    model_name = models.ForeignKey(ModelNames, on_delete=models.CASCADE, db_column='model_name_id')
    quantity = models.IntegerField()
    used_quantity = models.IntegerField()
    declaration_number = models.CharField(max_length=50)
    declaration_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'consignments'
        ordering = ['id']


class Colors(models.Model):
    color_code = models.CharField(
        max_length=4, db_column='color_code', blank=True, null=True)
    russian_title = models.CharField(
        max_length=50, db_column='russian_title', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colors'
        ordering = ['id']


class Products(models.Model):
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
    cleared = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'
        ordering = ['-id']


class Modules(models.Model):
    number = models.IntegerField(db_column='number')
    digit = models.IntegerField(db_column='digit')

    class Meta:
        managed = False
        db_table = 'modules'
        ordering = ['-id']
