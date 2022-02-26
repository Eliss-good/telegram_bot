
CREATE TABLE global_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    gl_teleg_id varchar(32) NOT NULL
); 

CREATE TABLE lesson_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    lesson_name varchar(128) NOT NULL
);

CREATE TABLE group_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_name varchar(32) NOT NULL,
    group_approved bool DEFAULT False NOT NULL
);

CREATE TABLE teach_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    teach_name varchar(64) NOT NULL,
    teach_approved bool DEFAULT False NOT NULL,
    gl_id int REFERENCES global_tb(id)
);

CREATE TABLE student_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    gl_id int REFERENCES global_tb(id),
    group_id int REFERENCES group_tb(id)
);

CREATE TABLE connect_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_id int REFERENCES group_tb(id),
    teach_id int REFERENCES teach_tb(id),
    lesson_id int REFERENCES teach_tb(id),
    teach_role varchar(8)
);


INSERT INTO global_tb (gl_teleg_id,gl_role) VALUES ('@kamaz','teach');
INSERT INTO lesson_tb (lesson_name) VALUES ('koks');
INSERT INTO teach_tb (teach_name, teach_surname, lesson_id, gl_id,teach_role)
VALUES ('name', 'surname', (select id from lesson_tb where lesson_name = 'koks'), 1 ,'PZ' );

drop table connect_tb;
drop table teach_tb;
drop table lesson_tb;
drop table group_tb;

