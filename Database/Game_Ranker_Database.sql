CREATE DATABASE IF NOT EXISTS gamerank;
USE gamerank;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS User_Games CASCADE;
DROP TABLE IF EXISTS Games CASCADE;

CREATE TABLE Users (
    user_id int4  NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    birth_date varchar(11),
    first_name varchar(40) NOT NULL,
    last_name varchar(40) NOT NULL,
    PRIMARY KEY (user_id)
); 
CREATE TABLE User_Games (
    user_id int4 NOT NULL,
    game_id int4 NOT NULL AUTO_INCREMENT,
    game_name varchar(255) NOT NULL UNIQUE,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id)
);
