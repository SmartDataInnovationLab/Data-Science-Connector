--- name: get_by_token^
SELECT *
FROM users
WHERE token = :token;