CREATE DATABASE sinadb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE sinadb;
CREATE TABLE Hot_1 (
  userid varchar(50) NOT NULL,
  issuper tinyint(1) NOT NULL,
  iscertificated tinyint(1) NOT NULL,
  isvip tinyint(1) NOT NULL,
  issthelse tinyint(1) NOT NULL,
  weibotext varchar(200) NOT NULL,
  support integer NOT NULL,
  relay integer NOT NULL,
  comment integer NOT NULL,
  time varchar(50) NOT NULL,
  client varchar(50) NOT NULL,
  primary key (userid, time)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;