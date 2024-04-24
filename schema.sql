

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


-- Inserting sample data into the users table
INSERT INTO users (username, email, password, first_name, last_name, dob, sockets_id, profile_picture)
VALUES
    ('user1', 'user1@example.com', 'password1', 'John', 'Doe', '1990-01-01',  12345, 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg'),
    ('user2', 'user2@example.com', 'password2', 'Jane', 'Smith', '1995-05-15', 54321, 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg'),
    ('user3', 'user3@example.com', 'password3', 'Alice', 'Johnson', '1988-11-30',  98765, 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg'),
    ('cindyn', 'cindyn@example.com', 'cindyn1' ,'Cindy', 'Nguyen', '2000-03-20',  01234, 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg');
    

-- Inserting sample data into the post table
INSERT INTO posts (username, title, body, price, condition, post_image) 
VALUES
    ('cindyn', 'textbook', 'This is the first is a calc textbook', 10.00, 'New', 'https://www.vitalsource.com/assets/coachme-b968423a61925be222b18375290bfa6756a7ea30a3bd3b65db4c0a2ceab97324.jpg'),
    ('user2', 'shoe', 'size 6 sneakers', 20.00, 'Like New', 'https://www.vitalsource.com/assets/coachme-b968423a61925be222b18375290bfa6756a7ea30a3bd3b65db4c0a2ceab97324.jpg'),
    ('user3', 'calculator', 'new ti-86 calc', 30.00, 'New', 'https://www.vitalsource.com/assets/coachme-b968423a61925be222b18375290bfa6756a7ea30a3bd3b65db4c0a2ceab97324.jpg');

-- Inserting sample data into the profiles table
INSERT INTO profiles (username, biography, profile_picture, followers, following)
VALUES
    ('cindyn', 'I am a student at UNCC comp sci student', 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg', 10, 110),
    ('user2', 'looking for a new home for my stuff', 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg', 40, 40),
    ('user3', 'uncc alumni looking to get rid of old supplies', 'https://www.apologia.com/wp-content/uploads/2020/07/Advanced-Biology-Textbook-Module-7.jpg', 30, 50);