-- User insert example
INSERT INTO users (login, password_hash, first_name, email)
VALUES ('tsalikhov', '$2b$10$OwmvNOfj1/r6L02v8Y.tdexuiOvoEeUzCZ/iyM4Njy7.q6DPml1rG', 'admin', 'Tim', 'tim@mai.ru')

-- Movies insert example
INSERT INTO movies (name, genres, year, preview, file)
VALUES ('Avengers', '{"action", "blockbuster"}', 2012, 'acde070d-8c4c-4f0d-9d8a-162843c10333','acde070d-8c4c-4f0d-9d8a-162843c10333')

-- Score insert
INSERT INTO scores (user_id, movie_id, score)
VALUES (1, 1, 4)

-- Watched insert
INSERT INTO watched (user_id, movie_id)
VALUES (1, 1)
