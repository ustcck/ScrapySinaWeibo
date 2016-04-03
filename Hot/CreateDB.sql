CREATE DATABASE sinadb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE sinadb;
CREATE TABLE Hot_1_user (
  userurl varchar(50) NOT NULL,
  userid varchar(50) NOT NULL,
  userfansamount integer ,
  userwatchamount integer ,
  userweiboamount integer,
  issuper tinyint(1),
  iscertificated tinyint(1),
  isvip tinyint(1),
  PRIMARY KEY (userurl)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Hot_1_user_weibo (
  userurl varchar(50) NOT NULL,
  weibotext varchar(200) NOT NULL,
  support integer NOT NULL,
  relay integer NOT NULL,
  comment integer NOT NULL,
  time datetime NOT NULL,
  client varchar(50) NOT NULL,
  PRIMARY KEY (userurl, time),
  FOREIGN KEY (userurl) REFERENCES Hot_1_user(userurl)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;