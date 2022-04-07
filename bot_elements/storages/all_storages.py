registerData = {}  # {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}}

edited_register_data = {} # {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role}}

temp_form_recipient_data = {}  # {*form_creator_user_id*: {recip data}}

temp_mem_for_form_creator = {}  # {*form_creator_user_id*: [form data], ...}

temp_mem_for_answers = {} # {user_id: [{answer1}, {answer2}, ...]}

mem_for_created_forms = {}  # {*form_id*: [form data], ...}

send_forms_mem = {} # {sent_form_id: {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [ids], 'send_to_groups': [groups],'got_answers_from': [ids]}, ...}
                    
completing_forms_dispatcher = {} # {user_id: {''unique_form_id'': id, 'unique_sent_form_id': id, 'current_question': num, 'form_copy': [form_data]}, ...}

choosing_groups_dispatcher = {} #  {user_id: {0: {'poll_id': , 'poll_options': }, 1: ...}, ...}   
temp_chosen_groups_data = {} # {user_id: [chosen groups]}

temp_form_index_data = {} # {user_id: form_index}

unique_form_id = 0
unique_sent_form_id = 0

unconfirmed_register_users = 0
unconfirmed_edit_users = 0
# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher
