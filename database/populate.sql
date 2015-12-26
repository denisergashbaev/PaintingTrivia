/**populate painter*/
insert into painter(id, name) values (1, 'Vincent van Gogh');
insert into painter(id, name) values (2, 'Pierre-Auguste Renoir');
insert into painter(id, name) values (3, 'Édouard Manet');
insert into painter(id, name) values (4, 'Claude Monet');

/**populate with initial data*/

insert into painting(fk_painter_id, title, file_name) values (1, 'Starry Night', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
insert into painting(fk_painter_id, title, file_name) values (2, 'Bal du moulin de la Galette', 'Bal_moulin_Galette_renoir.jpg');
insert into painting(fk_painter_id, title, file_name) values (3, 'Chez le père Lathuille', 'at-father-lathuille.jpg');
insert into painting(fk_painter_id, title, file_name) values (4, 'Le Déjeuner sur l’herbe', 'Monet_dejeunersurlherbe.jpg');

