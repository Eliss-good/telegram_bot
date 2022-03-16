import prep_text_pars
all_groups = []
for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
    all_groups.append(data['group'])
print(all_groups)