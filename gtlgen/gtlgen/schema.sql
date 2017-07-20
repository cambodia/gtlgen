drop table if exists gtlgen;
create table gtlgen (
  id integer IDENTITY(100,100) primary key,
  del_note varchar,
  del_note_pos varchar,
  del_note_date varchar,
  plant_code varchar,
  unloading_point varchar,
  mat_number varchar,
  mat_desc varchar,
  order_number varchar,
  order_pos varchar,
  qty varchar,
  batch_number varchar,
  eng_level varchar,
  pickup_date date,
  delivery_date date
);