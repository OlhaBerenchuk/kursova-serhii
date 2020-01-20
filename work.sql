insert into orm_company (company_name, website, secret_key) values ('Intersog', 'intersog.com', 'intersog123');
insert into orm_company (company_name, website, secret_key) values ('TestCompany', 'test.com', 'test123');
insert into orm_company (company_name, website, secret_key) values ('TechnoMatix', 'technomatix.com', 'tech123');

insert into orm_project (project_name, description, company_id) values ('PreenMe', 'Managment', 1);
insert into orm_project (project_name, description, company_id) values ('TestProject', 'Managment2', 2);
insert into orm_project (project_name, description, company_id) values ('PreenMeWorld', 'ManagmentWorld', 2);

insert into orm_user (user_email, user_username, user_password, is_owner, company_id) values ('sergiygorodnyuk@gmail.com', 'SergFors', 'uwehwknvlweiv', 1, 1);
insert into orm_user (user_email, user_username, user_password, is_owner, company_id) values ('test@gmail.com', 'Test', 'wiuehfwefjwe', 0, 1);
insert into orm_user (user_email, user_username, user_password, is_owner, company_id) values ('Hello@gmail.com', 'World', '8fy384fhoiwif', 0, 2);

insert into orm_file (file_name, upload_time, documentation, user_username, project_id) values ('test.py', '2020-01-20', 'test_doc.html', 'SergFors', 1)
insert into orm_file (file_name, upload_time, documentation, user_username, project_id) values ('test2.py', '2020-01-21', 'test_doc2.html', 'SergFors', 1)
insert into orm_file (file_name, upload_time, documentation, user_username, project_id) values ('test3.py', '2020-01-22', 'test_doc3.html', 'SergFors', 1)