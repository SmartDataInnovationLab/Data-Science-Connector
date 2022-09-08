--- name: create-schema#
-- storing ssh_pass/user here (and also in plaintext) is not necessary and bad from a security perspective, but its convenient, and for our purposes secure enough
CREATE TABLE IF NOT EXISTS instances (
    id integer PRIMARY KEY,
    path text NOT NULL,
    start_date text NOT NULL,
    end_date text NOT NULL,
    user_token text NOT NULL UNIQUE,
    ssh_user text NOT NULL,
    ssh_pass text NOT NULL,
    FOREIGN KEY (user_token) REFERENCES users (token)
);
