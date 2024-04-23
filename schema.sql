CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL,
    username VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    sockets_id integer[],
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY, 
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_content VARCHAR(255) NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);


CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, 
    username VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body VARCHAR(255) NOT NULL,
    post_date DATE NOT NULL,
    image_post VARCHAR(255) NOT NULL, -- idk if this is right but it is used for storing image paths
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE IF NOT EXISTS user_profile (
    user_id INT PRIMARY KEY, 
    first_name VARCHAR(255) NOT NULL,
    bio VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) NOT NULL, -- idk if this is right but it is used for storing image paths
    followers INTEGER[], 
    following_ INTEGER[],
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
);


CREATE TABLE IF NOT EXISTS favorites (
    user_id SERIAL,
    post_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    image_post VARCHAR(255) NOT NULL, --idk if this is correct bc its an image
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS explore (
    post_id SERIAL,
    title VARCHAR(255) NOT NULL,
    image_post VARCHAR(255) NOT NULL, --idk if this is correct bc its an image
    keywords VARCHAR(255)[]
    PRIMARY KEY (post_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS search_queries (
    query_id SERIAL PRIMARY KEY,
    user_id INT,
    query_text VARCHAR(255) NOT NULL,
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS search_results (
    result_id SERIAL PRIMARY KEY,
    query_id INT,
    post_id INT,
    relevance_score FLOAT,
    FOREIGN KEY (query_id) REFERENCES search_queries(query_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);


-- fake data
INSERT INTO users (username, user_password, email, first_name, last_name, sockets_id) 
VALUES 
    ('cindyn', '123456', 'cindy@gmail.com', 'Cindy', 'Nguyen', '{}'),
    ('johnd', 'abcdef', 'johnd@gmail.com', 'John', 'Doe', '{}'),
    ('janed', 'abc123', 'janed@gmail.com ', 'Jane', 'Doe', '{}');


