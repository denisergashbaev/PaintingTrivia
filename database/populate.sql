/**populate painter*/
insert into painter(id, name) values (1, 'Van Gogh1');
insert into painter(id, name) values (2, 'Van Gogh2');
insert into painter(id, name) values (3, 'Van Gogh3');
insert into painter(id, name) values (4, 'Van Gogh4');

/**populate with initial data*/

insert into painting(fk_painter_id, title, file_name) values (1, 'Starry Night', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
insert into painting(fk_painter_id, title, file_name) values (2, 'Starry Night2', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
insert into painting(fk_painter_id, title, file_name) values (3, 'Starry Night3', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
insert into painting(fk_painter_id, title, file_name) values (3, 'Starry Night4', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
insert into painting(fk_painter_id, title, file_name) values (4, 'Starry Night5', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg');
