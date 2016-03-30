CREATE DATABASE sinadb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE sinadb;
CREATE TABLE Hot_1_user (
  userurl varchar(50) NOT NULL,
  userid varchar(50) NOT NULL,
  userfansamount integer NOT NULL,
  userwatchamount integer NOT NULL,
  userweiboamount integer NOT NULL,
  issuper tinyint(1) NOT NULL,
  iscertificated tinyint(1) NOT NULL,
  isvip tinyint(1) NOT NULL,
  issthelse tinyint(1) NOT NULL,
  PRIMARY KEY (userurl)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Hot_1_user_weibo (
  userurl varchar(50) NOT NULL,
  weibotext varchar(200) NOT NULL,
  support integer NOT NULL,
  relay integer NOT NULL,
  comment integer NOT NULL,
  time varchar(50) NOT NULL,
  client varchar(50) NOT NULL,
  PRIMARY KEY (userurl, time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;