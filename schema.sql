CREATE DATABASE ninerthrifts;

CREATE TABLE IF NOT EXISTS users (
    user_id             UUID            DEFAULT uuid(),
    email               VARCHAR(255)    NOT NULL    UNIQUE,
    first_name          VARCHAR(255)    NOT NULL,
    last_name           VARCHAR(255)    NOT NULL,
    password            VARCHAR(255)    NOT NULL,
    dob                 DATE            NOT NULL,
    profile_image     BLOB            NOT NULL,
    PRIMARY KEY(user_id)
);