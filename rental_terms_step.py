import flet as ft

from translations import tr


FIELD_GROUPS = [
    (
        "rental_section_main",
        [
            "contract_number", "contract_day", "contract_month", "contract_year", "contract_city",
            "property_area", "property_area_words", "property_address", "property_use",
            "rent_until_date", "rent_amount_first", "rent_from_date", "rent_amount_second",
            "rent_charge_start_date", "actual_occupancy_date", "rent_free_start_date", "rent_free_end_date",
            "lease_start_date", "lease_end_date", "rent_amount", "deposit_amount", "payment_day",
        ],
    ),
    (
        "rental_section_tenant",
        [
            "tenant_business_name", "tenant_representative_name", "tenant_iin", "tenant_document_number",
            "tenant_address", "tenant_account", "tenant_bic", "tenant_phone",
        ],
    ),
    (
        "rental_section_landlord",
        [
            "landlord_business_name", "landlord_representative_name", "landlord_iin", "landlord_document_number",
            "landlord_address", "landlord_notice_number", "landlord_notice_date",
            "landlord_account", "landlord_bic", "landlord_phone",
        ],
    ),
]

FIELD_LABELS = {
    "ru": {
        "contract_number": "Номер договора", "contract_day": "День", "contract_month": "Месяц", "contract_year": "Год", "contract_city": "Город",
        "property_area": "Площадь помещения, м²", "property_area_words": "Площадь прописью", "property_address": "Адрес помещения", "property_use": "Назначение помещения",
        "rent_until_date": "Аренда до даты", "rent_amount_first": "Сумма аренды до даты, ₸", "rent_from_date": "Аренда с даты", "rent_amount_second": "Сумма аренды с даты, ₸",
        "rent_charge_start_date": "Начало начисления аренды", "actual_occupancy_date": "Дата фактического въезда", "rent_free_start_date": "Начало бесплатного периода", "rent_free_end_date": "Конец бесплатного периода",
        "lease_start_date": "Дата начала аренды", "lease_end_date": "Дата окончания аренды", "rent_amount": "Общая арендная плата, ₸", "deposit_amount": "Залог, ₸", "payment_day": "День оплаты",
        "tenant_business_name": "Наименование арендатора", "tenant_representative_name": "Представитель арендатора", "tenant_iin": "ИИН арендатора", "tenant_document_number": "Номер документа арендатора",
        "tenant_address": "Адрес арендатора", "tenant_account": "ИИК арендатора", "tenant_bic": "БИК арендатора", "tenant_phone": "Телефон арендатора",
        "landlord_business_name": "ИП арендодателя", "landlord_representative_name": "Представитель арендодателя", "landlord_iin": "ИИН арендодателя", "landlord_document_number": "Номер документа арендодателя",
        "landlord_address": "Адрес арендодателя", "landlord_notice_number": "№ уведомления ИП", "landlord_notice_date": "Дата уведомления", "landlord_account": "ИИК арендодателя", "landlord_bic": "БИК арендодателя", "landlord_phone": "Телефон арендодателя",
    },
    "en": {
        "contract_number": "Agreement number", "contract_day": "Day", "contract_month": "Month", "contract_year": "Year", "contract_city": "City",
        "property_area": "Premises area, sq. m", "property_area_words": "Area in words", "property_address": "Premises address", "property_use": "Permitted use",
        "rent_until_date": "Rent through date", "rent_amount_first": "Rent through date, KZT", "rent_from_date": "Rent from date", "rent_amount_second": "Rent from date, KZT",
        "rent_charge_start_date": "Rent charge start", "actual_occupancy_date": "Actual occupancy date", "rent_free_start_date": "Rent-free period start", "rent_free_end_date": "Rent-free period end",
        "lease_start_date": "Lease start date", "lease_end_date": "Lease end date", "rent_amount": "Monthly rent, KZT", "deposit_amount": "Security deposit, KZT", "payment_day": "Payment day",
        "tenant_business_name": "Lessee name", "tenant_representative_name": "Lessee representative", "tenant_iin": "Lessee IIN", "tenant_document_number": "Lessee ID document number",
        "tenant_address": "Lessee address", "tenant_account": "Lessee IBAN", "tenant_bic": "Lessee BIC", "tenant_phone": "Lessee phone",
        "landlord_business_name": "Lessor's sole proprietorship", "landlord_representative_name": "Lessor's representative", "landlord_iin": "Lessor IIN", "landlord_document_number": "Lessor ID document number",
        "landlord_address": "Lessor address", "landlord_notice_number": "Business notice number", "landlord_notice_date": "Notice date", "landlord_account": "Lessor IBAN", "landlord_bic": "Lessor BIC", "landlord_phone": "Lessor phone",
    },
    "kk": {
        "contract_number": "Шарт нөмірі", "contract_day": "Күні", "contract_month": "Айы", "contract_year": "Жылы", "contract_city": "Қала",
        "property_area": "Үй-жай ауданы, м²", "property_area_words": "Ауданы сөзбен", "property_address": "Үй-жай мекенжайы", "property_use": "Пайдалану мақсаты",
        "rent_until_date": "Күнге дейінгі жалдау", "rent_amount_first": "Күнге дейінгі жалдау ақысы, ₸", "rent_from_date": "Күннен бастап жалдау", "rent_amount_second": "Күннен бастап жалдау ақысы, ₸",
        "rent_charge_start_date": "Жалдау ақысы есептеле бастайтын күн", "actual_occupancy_date": "Нақты орналасқан күн", "rent_free_start_date": "Тегін кезеңнің басы", "rent_free_end_date": "Тегін кезеңнің соңы",
        "lease_start_date": "Жалдау басталатын күн", "lease_end_date": "Жалдау аяқталатын күн", "rent_amount": "Ай сайынғы жалдау ақысы, ₸", "deposit_amount": "Кепілдік жарна, ₸", "payment_day": "Төлем күні",
        "tenant_business_name": "Жалға алушының атауы", "tenant_representative_name": "Жалға алушының өкілі", "tenant_iin": "Жалға алушының ЖСН-і", "tenant_document_number": "Жалға алушының құжат нөмірі",
        "tenant_address": "Жалға алушының мекенжайы", "tenant_account": "Жалға алушының IBAN-ы", "tenant_bic": "Жалға алушының BIC-і", "tenant_phone": "Жалға алушының телефоны",
        "landlord_business_name": "Жалға беруші ЖК", "landlord_representative_name": "Жалға берушінің өкілі", "landlord_iin": "Жалға берушінің ЖСН-і", "landlord_document_number": "Жалға берушінің құжат нөмірі",
        "landlord_address": "Жалға берушінің мекенжайы", "landlord_notice_number": "ЖК қызметі туралы хабарлама №", "landlord_notice_date": "Хабарлама күні", "landlord_account": "Жалға берушінің IBAN-ы", "landlord_bic": "Жалға берушінің BIC-і", "landlord_phone": "Жалға берушінің телефоны",
    },
}

SECTION_TITLES = {
    "ru": {
        "rental_section_main": "ДОГОВОР И УСЛОВИЯ АРЕНДЫ",
        "rental_section_tenant": "ДАННЫЕ АРЕНДАТОРА",
        "rental_section_landlord": "ДАННЫЕ АРЕНДОДАТЕЛЯ",
    },
    "en": {
        "rental_section_main": "AGREEMENT AND RENTAL TERMS",
        "rental_section_tenant": "TENANT DETAILS",
        "rental_section_landlord": "LANDLORD DETAILS",
    },
    "kk": {
        "rental_section_main": "ШАРТ ЖӘНЕ ЖАЛДАУ ТАЛАПТАРЫ",
        "rental_section_tenant": "ЖАЛҒА АЛУШЫ ТУРАЛЫ МӘЛІМЕТТЕР",
        "rental_section_landlord": "ЖАЛҒА БЕРУШІ ТУРАЛЫ МӘЛІМЕТТЕР",
    },
}


def _tenant_defaults(data):
    person_name = " ".join(
        str(data.get(key, "")).strip()
        for key in ("surname", "first_name", "patronymic")
        if str(data.get(key, "")).strip()
    )
    return {
        "tenant_business_name": person_name,
        "tenant_representative_name": person_name,
        "tenant_iin": data.get("iin", ""),
        "tenant_document_number": data.get("document_number", ""),
    }


def show_rental_terms_step(language="ru", data=None, on_back=None, on_next=None):
    data = data if data is not None else {}
    defaults = _tenant_defaults(data)
    autofilled_defaults = data.setdefault("_tenant_autofill_values", {})
    labels = FIELD_LABELS.get(language, FIELD_LABELS["ru"])
    section_titles = SECTION_TITLES.get(language, SECTION_TITLES["ru"])
    sections = []
    for section_key, fields in FIELD_GROUPS:
        controls = [ft.Text(section_titles[section_key], size=15, weight=ft.FontWeight.BOLD, color="#315b73")]
        for key in fields:
            if key in defaults:
                current = data.get(key, "")
                previous_default = autofilled_defaults.get(key)
                if not str(current or "").strip() or current == previous_default:
                    initial = defaults.get(key, "")
                    autofilled_defaults[key] = initial
                else:
                    initial = current
            else:
                initial = data.get(key, "")
            data[key] = initial
            controls.append(ft.TextField(
                label=labels[key], value=initial, expand=True,
                on_change=lambda e, field=key: data.__setitem__(field, e.control.value),
            ))
        sections.append(ft.Container(
            content=ft.Column(controls, spacing=8), padding=16,
            border=ft.Border.all(1, ft.Colors.GREY_300), border_radius=12,
        ))

    return ft.Column([
        ft.Text(tr(language, "rental_terms"), size=21, weight=ft.FontWeight.BOLD),
        ft.Text(tr(language, "optional_fields"), color=ft.Colors.BLUE_GREY_700),
        *sections,
        ft.Row([
            ft.Button(content=tr(language, "back_to_person"), icon=ft.Icons.ARROW_BACK, on_click=lambda _e: on_back()),
            ft.Container(expand=True),
            ft.Button(content=tr(language, "next"), icon=ft.Icons.ARROW_FORWARD, on_click=lambda _e: on_next()),
        ]),
    ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)
