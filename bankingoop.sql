
ALTER USER 'admin'@'localhost' IDENTIFIED BY 'new_password';

GRANT ALL PRIVILEGES ON banking_system.* TO 'admin'@'localhost';