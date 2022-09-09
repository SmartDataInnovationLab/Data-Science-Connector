--- name: get-busy-by-token$
SELECT busy
FROM busyness
WHERE user_token = :token;