SELECT * FROM batch_students WHERE student_name = Alice Smith;

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



CREATE TABLE S1 (
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

CREATE TABLE S2 (
    UID VARCHAR(50) primary key,
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

CREATE TABLE S3 (
    UID VARCHAR(50),
    Batch VARCHAR(50),
    Semester_id INT,
    Semester_name VARCHAR(50),
    Name VARCHAR(100),
    DMS_Marks INT,
    DMS_grade VARCHAR(5),
    DS_Marks INT,
    DS_grade VARCHAR(5),
    DSD_Marks INT,
    DSD_grade VARCHAR(5),
    Python_Marks INT,
    Python_grade VARCHAR(5),
    Design_and_engineering_Marks INT,
    Design_and_engineering_grade VARCHAR(5),
    Sustainable_engineering_Marks INT,
    Sustainable_engineering_grade VARCHAR(5),
    DS_lab_Marks INT,
    DS_lab_grade VARCHAR(5),
    Python_lab_mark INT,
    Python_lab_grade VARCHAR(5),
    sgpa FLOAT,
    cgpa FLOAT,
    FOREIGN KEY (semester_id) REFERENCES sem(semester_id)
);

CREATE TABLE S4 (
    UID VARCHAR(50),
    Batch VARCHAR(50),
    Semester_id INT,
    Semester_name VARCHAR(50),
    Name VARCHAR(100),
    Principles_Of_Object_Oriented_Techniques_Marks INT,
    Principles_Of_Object_Oriented_Techniques_Grade VARCHAR(5),
    Graph_Theory_Marks INT NULL,
    Graph_Theory_grade VARCHAR(5),
    Computer_Organization_Marks INT NULL,
    Computer_Organization_grade VARCHAR(5),
    Database_Management_Systems_Marks INT NULL,
    Database_Management_Systems_grade VARCHAR(5),
    Professional_Ethics_Marks INT NULL,
    Professional_Ethics_grade VARCHAR(5),
    Constitution_Of_India_Marks INT NULL,
    Constitution_Of_India_grade VARCHAR(5),
    Object_Oriented_Techniques_Lab_Marks INT NULL,
    Object_Oriented_Techniques_Lab_grade VARCHAR(5),
    Database_Management_Systems_Lab_Marks INT NULL,
    Database_Management_Systems_Lab_grade VARCHAR(5),
    sgpa FLOAT NULL,
    cgpa FLOAT NULL,
    FOREIGN KEY (Semester_id) REFERENCES sem(Semester_id)
);


CREATE TABLE S5 (
    UID VARCHAR(10) PRIMARY KEY,
    Batch VARCHAR(10),
    Semester_id INT,
    Semester_Name VARCHAR(5),
    Name VARCHAR(100),
    Web_Application_Development_Marks INT,
    Web_Application_Development_grade VARCHAR(5),
    Operating_System_Concepts_Marks INT,
    Operation_System_Concepts_grade VARCHAR(5),
    Data_Communication_and_Networking_Marks INT,
    Data_Communication_and_Networking_grade VARCHAR(5),
    Formal_Languages_and_Automata_Theory_Marks INT,
    Formal_Languages_and_Automata_Theory_grade VARCHAR(5),
    Management_For_Software_Engineers_Marks INT,
    Management_For_Software_Engineers_grade VARCHAR(5),
    Disaster_Management_Marks INT,
    Disaster_Management_grade VARCHAR(5),
    Operating_System_and_Network_Programming_Lab_Marks INT,
    Operating_System_and_Network_Programming_Lab_grade VARCHAR(5),
    Web_Application_Development_Lab_Marks INT,
    Web_Application_Development_Lab_grade VARCHAR(5),
    SGPA DECIMAL(3,1),
    CGPA DECIMAL(3,1),
    FOREIGN KEY (Semester_id) REFERENCES sem(Semester_id)

);

CREATE TABLE S6 (
    UID VARCHAR(10) PRIMARY KEY,
    Batch VARCHAR(10),
    Semester_id INT,
    Semester_Name VARCHAR(5),
    Name VARCHAR(100),
    Internetworking_with_TCP_IP_Marks INT,
    Internetworking_with_TCP_IP_Grade VARCHAR(5),
    Algorithm_Analysis_and_Design_Marks INT,
    Algorithm_Analysis_and_Design_Grade VARCHAR(10),
    Data_Science_Marks INT,
    Data_Science_Grade VARCHAR(10),
    Soft_Computing_Marks INT,
    Soft_Computing_Grade VARCHAR(10),
    Digital_Image_Processing_Marks INT,
    Digital_Image_Processing_Grade VARCHAR(10),
    Industrial_Economics_and_Foreign_Trade_Marks INT,
    Industrial_Economics_and_Foreign_Trade_Grade VARCHAR(10),
    Computer_Networks_Lab_Marks INT,
    Computer_Networks_Lab_Grade VARCHAR(10),
    Miniproject_Marks INT,
    Miniproject_Grade VARCHAR(10),
    SGPA DECIMAL(3,1),
    CGPA DECIMAL(3,1),
    FOREIGN KEY (Semester_id) REFERENCES sem(Semester_id)

);

CREATE TABLE S7 (
    UID VARCHAR(10) primary key,
    Batch VARCHAR(10),
    Semester_id INT,
    Semester_Name VARCHAR(5),
    Name VARCHAR(100),
    Data_Analytics_Marks INT,
    Data_Analytics_Grade CHAR(1),
    Mobile_Computing_Marks INT,
    Mobile_Computing_Grade CHAR(1),
    Artificial_Intelligence_Marks INT,
    Artificial_Intelligence_Grade CHAR(1),
    Industrial_Safety_Engineering_Marks INT,
    Industrial_Safety_Engineering_Grade CHAR(1),
    Data_Analytics_Lab_Marks INT,
    Data_Analytics_Lab_Grade CHAR(1),
    Seminar_Marks INT,
    Seminar_Grade CHAR(1),
    Project_Phase1_Marks INT,
    Project_Phase1_Grade CHAR(1),
    SGPA DECIMAL(3,1),
    CGPA DECIMAL(3,1),
    FOREIGN KEY (Semester_id) REFERENCES sem(Semester_id)

);
CREATE TABLE S8 (
    UID VARCHAR(10) primary key,
    Batch VARCHAR(10),
    Semester_id INT,
    Semester_Name VARCHAR(5),
    Name VARCHAR(100),
    CRYPTOGRAPHY_AND_NETWORK_SECURITY_Marks INT,
    CRYPTOGRAPHY_AND_NETWORK_SECURITY_Grade CHAR(1),
    COMPUTER_VISION_Marks INT,
    COMPUTER_VISION_Grade CHAR(1),
    Cloud_Computing_Marks INT,
    Cloud_Computing_Grade CHAR(1),
    INTERNET_OF_THINGS_Marks INT,
    INTERNET_OF_THINGS_Grade CHAR(1),
    ADHOC_AND_WIRELESS_SENSOR_NETWORKS_Marks INT,
    ADHOC_AND_WIRELESS_SENSOR_NETWORKS_Grade CHAR(1),
    SOFTWARE_ARCHITECTURE_Marks INT,
    SOFTWARE_ARCHITECTURE_Grade CHAR(1),
    NATURAL_LANGUAGE_PROCESSING_Marks INT,
    NATURAL_LANGUAGE_PROCESSING_Grade CHAR(1),
    Project_Phase2_Marks INT,
    Project_Phase2_Grade CHAR(1),
    SGPA DECIMAL(3,1),
    CGPA DECIMAL(3,1),
    FOREIGN KEY (Semester_id) REFERENCES sem(Semester_id)

);


-- Create the batches table
CREATE TABLE batches (
    batch_id INT PRIMARY KEY,
    batch_name VARCHAR(255) NOT NULL
);

-- Create the batch_students table
CREATE TABLE batch_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    uid VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id)
);