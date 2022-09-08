-- name: insert!
INSERT INTO instances(id, path, start_date, end_date, user_token, ssh_user, ssh_pass, ssh_port)
VALUES (:id, :path, :start_date, :end_date, :user_token, :ssh_user, :ssh_pass, :ssh_port);