

DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP DATABASE IF EXISTS ninerthrifts;


CREATE TABLE IF NOT EXISTS users (
    user_id             SERIAL          NOT NULL,
    username            VARCHAR(255)    NOT NULL    UNIQUE,
    email               VARCHAR(255)    NOT NULL    UNIQUE,
    password            VARCHAR(255)    NOT NULL,
    first_name          VARCHAR(255)    NOT NULL,
    last_name           VARCHAR(255)    NOT NULL,
    dob                 DATE            NOT NULL,
    profile_picture     BYTEA           NOT NULL,
    sockets_id          INTEGER         NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS profiles (
    user_id             SERIAL            NOT NULL,
    username            VARCHAR(255)    NOT NULL,
    biography           VARCHAR(255),
    profile_picture     BYTEA           NOT NULL,
    followers           INTEGER         DEFAULT     0,
    following           INTEGER         DEFAULT     0,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS posts (
    user_id         SERIAL          NOT NULL,
    username        VARCHAR(255)    NOT NULL,
    post_id         SERIAL          NOT NULL,
    title           VARCHAR(255)    NOT NULL,
    body            VARCHAR(255)    NOT NULL,
    price           DECIMAL(10,2)   NOT NULL,
    condition       VARCHAR(255)    NOT NULL,
    post_image      BYTEA           NOT NULL,
    posted_date     TIMESTAMP       DEFAULT     CURRENT_TIMESTAMP,
    PRIMARY KEY(post_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id      SERIAL          NOT NULL,
    username        VARCHAR(255)    NOT NULL,
    receiver_id     SERIAL            NOT NULL,
    sender_id       SERIAL            NOT NULL,
    message         VARCHAR(255)    NOT NULL,
    time            TIMESTAMP       DEFAULT     CURRENT_TIMESTAMP,
    PRIMARY KEY(message_id),
    FOREIGN KEY(receiver_id) REFERENCES users(user_id),
    FOREIGN KEY(sender_id) REFERENCES users(user_id)
);

