CREATE USER 'admin'@'%' IDENTIFIED BY 'adminpassword';
GRANT ALL PRIVILEGES ON your_database.* TO 'admin'@'%';
FLUSH PRIVILEGES;