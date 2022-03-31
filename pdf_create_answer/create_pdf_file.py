from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.document.document import Document
from decimal import Decimal
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from datetime import datetime


from db_setting.all_con_bot_bd import get_data_form, get_tg_creator_form, get_name_form, find_role_us, find_fio_us
import create_statick_data


def math_stat(one_res: float, all_user_send : float):
    """Подсчёт доли ответа"""
    return (one_res / all_user_send) * 100


def create_pdf(name_user : str, role_user: str, name_form: str,result_answer: dict):
    """Создание pdf документа"""
    doc: Document = Document()

    page: Page = Page()
    doc.append_page(page)
    layout: PageLayout = SingleColumnLayout(page)

    m: Decimal = Decimal(10)

    layout.add(FixedColumnWidthTable(number_of_columns=2, number_of_rows=4)
        .add(Paragraph("Author: ")) .add(Paragraph(name_user))
        .add(Paragraph("Role user: ")) .add(Paragraph(role_user))
        .add(Paragraph("Time: ")) .add(Paragraph(str(datetime.now())))
        .add(Paragraph("Name form: ")) .add(Paragraph(name_form))

        .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        .no_borders()
    )

    count_qes = 1
    for ques, answer in result_answer.items():
        layout.add(FixedColumnWidthTable(number_of_columns=2, number_of_rows=2, margin_top=10)
            .add(Paragraph('Question'+str(count_qes))) .add(Paragraph(ques))
            .add(Paragraph('Type_ques', )) .add(Paragraph(answer['!!type!!']))

            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            .no_borders()
        )

        count_qes += 1

        all_user_send = 0
        for ans, result in answer.items():
            if ans != '!!type!!':
                all_user_send += result

        for ans, result in answer.items():
            if ans != '!!type!!':
                layout.add(FixedColumnWidthTable(number_of_columns=2, number_of_rows=1)
                    .add(Paragraph(ans)) .add(Paragraph(str(math_stat(result, all_user_send)) + '%'))
                    .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
                )
    # store
    with open("output.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, doc)


def pars_json_answer(form_id: int):
    """Получение ответов из json"""
    forms = get_data_form('one', form_id=form_id)
    result_answer = create_statick_data.formatting_answer(forms)

    tg_id = get_tg_creator_form(form_id)
    name_user = find_fio_us(tg_id)
    role_user = find_role_us(tg_id)

    name_form = get_name_form(form_id)

    if name_form:
        create_pdf(name_user, role_user, name_form, result_answer)
    else:
        print("ERORR fun", pars_json_answer.__name__)

