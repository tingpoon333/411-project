CREATE DATABASE IF NOT EXISTS gamerank;
USE gamerank;
DROP TABLE IF EXISTS User_Games CASCADE;
DROP TABLE IF EXISTS recs CASCADE;
DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE Users (
uid int4 NOT NULL AUTO_INCREMENT,
email varchar(255) NOT NULL UNIQUE,
primary key (uid)
);

CREATE TABLE User_Games (
game_id int4 NOT NULL AUTO_INCREMENT,
game_name varchar(255) NOT NULL,
date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (game_id)
);

CREATE TABLE recs (
rid int4 NOT NULL AUTO_INCREMENT,
rec_game_name varchar(255) NOT NULL,
PRIMARY KEY(rid)
);
