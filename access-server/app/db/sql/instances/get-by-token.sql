--- name: get-by-token^
SELECT *
FROM instances
WHERE user_token = :token;