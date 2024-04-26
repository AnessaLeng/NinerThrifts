DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS users CASCADE;


CREATE TABLE IF NOT EXISTS users (
    username            VARCHAR(255)    NOT NULL    UNIQUE,
    email               VARCHAR(255)    NOT NULL    UNIQUE,
    pass            VARCHAR(255)    NOT NULL,
    biography           VARCHAR(255),
    first_name          VARCHAR(255)    NOT NULL,
    last_name           VARCHAR(255)    NOT NULL,
    dob                 DATE            NOT NULL,
    profile_picture     BYTEA           NOT NULL,
    sockets_id          INTEGER         NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE IF NOT EXISTS posts (
    username        VARCHAR(255)    NOT NULL,
    post_id         SERIAL          NOT NULL,
    title           VARCHAR(255)    NOT NULL,
    body            VARCHAR(255)    NOT NULL,
    price           DECIMAL(10,2)   NOT NULL,
    condition       VARCHAR(255)    NOT NULL,
    post_image      BYTEA           NOT NULL,
    posted_date     TIMESTAMP       DEFAULT     CURRENT_TIMESTAMP,
    PRIMARY KEY(post_id),
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS messages (
    username        VARCHAR(255)    NOT NULL,
    message         VARCHAR(255)    NOT NULL,
    time            TIMESTAMP       DEFAULT     CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(username)
);

