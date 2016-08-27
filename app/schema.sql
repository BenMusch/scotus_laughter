drop table if exists cases;
create table cases (
  docket_num text primary key;
  title text not null;
  'date' date not null;
);

drop table if exists transcripts;
create table transcripts (
  id integer primary key autoincrement;
  url text not null;
  docket_num text not null;
  foreign key(docket_num) references cases;
);

drop table if exists speakers;
create table speakers (
  id integer primary key autoincrement;
  name text not null;
);

drop table if exists lines;
create table lines (
  id integer primary key autoincrement;
  audio_link text;
  audio_start integer;
  audio_end integer;
  has_laughter boolean default false;
  prev_line_id integer;
  next_line_id integer;
  docket_num text not null;
  speaker_id integer not null;
  foreign key(speaker_id) references speakers;
  foreign key(docket_num) references cases;
  foreign key(prev_line_id) references lines;
  foreign key(next_line_id) references lines;
);

