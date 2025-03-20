INSERT INTO teacher_login (username, password ) VALUES ('teacher', 'teacher');
INSERT INTO admin_login (username, password ) VALUES ('admin', 'admin');

create table teacher_login (
    teacher_id int primary key,
    username varchar(50),
    password varchar(50)
);

INSERT INTO teacher_login (username, password, teacher_id, teacher_id)
VALUES (
    'username:varchar',
    'password:varchar',
    teacher_id:int,
    teacher_id:int
  );