from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from num2words import num2words

from apps.sez.models import InnerTTN, InnerTTNItems
from apps.omega.models import OBJ_ATTR_VALUES_1000004


def get_ttn_pdf(id: int) -> str:
    ttn = InnerTTN.objects.filter(id=id).first()
    if not ttn:
        return None
    items = InnerTTNItems.objects.filter(inner_ttn=ttn)

    quantity = 0
    price = 0
    weight = 0
    full_price = 0
    cargo_spaces = 0
    for item in items:
        short_name = item.model_name.short_name if item.model_name.short_name else item.model_name.name
        omega_obj = OBJ_ATTR_VALUES_1000004.objects.using('oracle_db').filter(
            A_3607=short_name).first()
        item.full_name = omega_obj.А_3173 if omega_obj else item.model_name.name
        quantity += item.quantity
        item.price = item.price_pcs * item.quantity
        price += item.price
        weight += item.weight_brutto * item.quantity
        item.nds_sum = price * item.nds / 100
        item.full_price = item.nds_sum + item.price
        full_price += item.full_price
        cargo_spaces += item.cargo_space

    coin = int((full_price % 1) * 100)
    rub = int(full_price)
    rub_text = num2words(rub, lang='ru')
    weight_text = num2words(int(weight), lang='ru')

    context = {
        "date": ttn.date.strftime("%d.%m.%Y"),
        "ttn": ttn,
        "items": items,
        "quantity": quantity,
        "price": price,
        "full_price": full_price,
        "weight": weight,
        "coin": coin,
        "rub_text": rub_text,
        "weight_text": weight_text,
        "cargo_spaces": cargo_spaces,
    }

    html_message = render_to_string(
        "innerttn.html",
        context,
    )
    font_config = FontConfiguration()

    file_path = 'tmp/' + f'inner_ttn_{ttn.id}.pdf'
    HTML(string=html_message).write_pdf(file_path, font_config=font_config)
    return file_path
