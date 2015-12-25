drop table if exists paintings;
create table if not exists paintings (
  id integer primary key autoincrement,
  title text not null,
  file_name text not null
);
/**populate with initial data*/
insert into paintings(title,file_name) values ('Starry Night', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg')