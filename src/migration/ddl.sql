CREATE TABLE "users"(
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(255) NULL,
    "password_hash" VARCHAR(255) NULL,
    "first_name" VARCHAR(255) NULL,
    "email" VARCHAR(255) NULL
);

CREATE TABLE "movies"(
    "movie_id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "genres" VARCHAR(255) ARRAY[10] NOT NULL,
    "year" BIGINT NOT NULL
);

CREATE TABLE "scores"(
    "user_id" BIGINT NOT NULL REFERENCES "users"("user_id")
        ON DELETE CASCADE,
    "movie_id" BIGINT NOT NULL REFERENCES "movies"("movie_id")
        ON DELETE CASCADE,
    "score" BIGINT NOT NULL
);

CREATE TABLE "watched"(
    "user_id" BIGINT NOT NULL REFERENCES "users"("user_id")
        ON DELETE CASCADE,
    "movie_id" BIGINT NOT NULL REFERENCES "movies"("movie_id")
        ON DELETE CASCADE
);