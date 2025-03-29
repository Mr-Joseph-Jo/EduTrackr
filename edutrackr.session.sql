INSERT INTO semester (semester_id, batch_id, semester_name)
VALUES (2, 1, '2nd');
INSERT INTO sem (semester_id, batch_name, semester_name) 
VALUES 
(1, '2021-2025', 'S1'),
(2, '2021-2025', 'S2'),
(3, '2021-2025', 'S3'),
(4, '2021-2025', 'S4'),
(5, '2021-2025', 'S5'),
(6, '2021-2025', 'S6'),
(7, '2021-2025', 'S7'),
(8, '2021-2025', 'S8');
CREATE TABLE s1 (
    UID VARCHAR(50),
    Batch VARCHAR(50),
    Semester_id INT,
    Semester_name VARCHAR(50),
    Name VARCHAR(100),
    LAC_Marks INT,
    LAC_grade VARCHAR(5),
    Engg_Chem_Marks INT,
    Engg_Chem_grade VARCHAR(5),
    Engg_Graphics_Marks INT,
    Engg_Graphics_Grade VARCHAR(5),
    Basics_CE_ME_Marks INT,
    Basics_CE_ME_Grade VARCHAR(5),
    LS_Marks INT,
    LS_Grade VARCHAR(5),
    Chem_Lab_Marks INT,
    Chem_Lab_Grade VARCHAR(5),
    Workshop_Marks INT,
    Workshop_Grade VARCHAR(5),
    sgpa FLOAT,
    cgpa FLOAT,
    FOREIGN KEY (semester_id) REFERENCES sem(semester_id)
);

CREATE TABLE s2 (
    UID VARCHAR(50),
    Batch VARCHAR(50),
    Semester_id INT,
    Semester_name VARCHAR(50),
    Name VARCHAR(100),
    Vector_calculus_Marks INT,
    Vector_calculus_grade VARCHAR(5),
    Engg_Physics_Marks INT,
    Engg_Physics_grade VARCHAR(5),
    Engg_Mechanics_Marks INT,
    Engg_Mechanics_grade VARCHAR(5),
    Professional_Communication_Marks INT,
    Professional_Communication_Grade VARCHAR(5),
    Basics_of_Electronic_and_Electricals_Marks INT,
    Basics_of_Electronic_and_Electricals_grade VARCHAR(5),
    Programming_in_C_Marks INT,
    Programming_in_C_grade VARCHAR(5),
    engg_physics_lab_Marks INT,
    engg_physics_lab_grade VARCHAR(5),
    Electrical_electronic_lab_mark INT,
    Electrical_electronic_lab_grade VARCHAR(5),
    sgpa FLOAT,
    cgpa FLOAT,
    FOREIGN KEY (semester_id) REFERENCES sem(semester_id)
);
