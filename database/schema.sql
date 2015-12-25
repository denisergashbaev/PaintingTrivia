/*drop table if exists painting;*/


CREATE TABLE IF NOT EXISTS painting (
  id integer primary key autoincrement,
  fk_painter_id integer not null,
  title text not null,
  file_name text not null,
  FOREIGN KEY(fk_painter_id) REFERENCES painter(id)
);

CREATE TABLE IF NOT EXISTS painter
(
  id integer primary key,
  name TEXT NOT NULL
);