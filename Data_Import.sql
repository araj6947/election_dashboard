 load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Indian_Election_Data/ALL_STATES_GE_1.csv'
 into table lokshabha
 fields terminated by ','
 enclosed by '"'
 lines terminated by '\n'
 ignore 1 rows;