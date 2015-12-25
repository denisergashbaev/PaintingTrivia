/*drop table if exists painting;*/


CREATE TABLE IF NOT EXISTS painting (
  id integer primary key,
  title text not null,
  file_name text not null
);

CREATE TABLE IF NOT EXISTS painter
(
  id integer primary key autoincrement,
  name TEXT NOT NULL
);