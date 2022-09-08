-- name: remove_by_token!
DELETE FROM instances
WHERE user_token = :token;