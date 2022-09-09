-- name: change-busy!
INSERT OR REPLACE INTO busyness(busy, user_token)
VALUES (:busy, :user_token);