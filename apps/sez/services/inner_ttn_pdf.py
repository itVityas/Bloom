from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from num2words import num2words

from apps.sez.models import InnerTTN, InnerTTNItems


def get_ttn_pdf(id: int) -> str:
    ttn = InnerTTN.objects.filter(id=id).first()
    if not ttn:
        return None
    items = InnerTTNItems.objects.filter(inner_ttn=ttn)

    quantity = 0
    price = 0
    weight = 0
    full_price = 0
    for item in items:
        quantity += item.quantity
        item.price = item.price_pcs * item.quantity
        price += item.price
        weight += item.weight
        item.nds_sum = price * item.nds / 100
        item.full_price = item.nds_sum + item.price
        full_price += item.full_price

    coin = int((full_price % 1) * 100)
    rub = int(full_price)
    rub_text = num2words(rub, lang='ru')
    weight_text = num2words(int(weight*1000), lang='ru')

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
    }

    html_message = render_to_string(
        "innerttn.html",
        context,
    )
    font_config = FontConfiguration()

    file_path = 'tmp/' + f'inner_ttn_{ttn.id}.pdf'
    HTML(string=html_message).write_pdf(file_path, font_config=font_config)
    return file_path
