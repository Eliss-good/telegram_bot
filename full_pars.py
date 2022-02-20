import prep_text_pars

def parse_group(index):
    full_prep_list = []
    begin_week = 1
    end_week = 30
    for week in range(begin_week, end_week):
        curr_week = prep_text_pars.get_prepods_text_list_page('https://mai.ru/education/studies/schedule/index.php?group={1}&week={0}#'.format(week, index))
        for prep in curr_week:
            if prep not in full_prep_list:
                full_prep_list.append(prep)

    return full_prep_list


def parse_group_today(index):
    full_prep_list = []
    
    curr_week = prep_text_pars.get_prepods_text_list_page('https://mai.ru/education/studies/schedule/index.php?group={0}#'.format(index))
    for prep in curr_week:
        if prep not in full_prep_list:
            full_prep_list.append(prep)

    return full_prep_list


# print(parse_group('М3О-221Б-20'))
print(parse_group_today('М3О-221Б-20'))