CREATE DATABASE indexing_schema;

CREATE USER 'tutturu'@'localhost' IDENTIFIED BY '1';

GRANT ALL PRIVILEGES ON indexing_schema. * TO 'newuser'@'localhost';

FLUSH PRIVILEGES;
