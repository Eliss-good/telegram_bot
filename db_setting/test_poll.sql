CREATE TABLE  question_tb(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    question_name varchar(128)
);

CREATE TABLE groupquestion_tb(
    q_id int REFERENCES question_tb(id) NOT NULL,
    gp_question_id int NOT NULL
);

CREATE TABLE survay_tb(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name_survay varchar(128),
    from_id varchar(32) NOT NULL,
    to_group varchar(32) NOT NULL,
    gp_question_id int NOT NULL
);

CREATE TABLE answer_tb(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    q_id int REFERENCES question_tb(id) NOT NULL,
    answer_name varchar(128),
    survay_id int REFERENCES survay_tb(id) NOT NULL
);