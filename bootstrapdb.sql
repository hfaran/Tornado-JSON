# Create a DB called **touchpoint**
    CREATE DATABASE IF NOT EXISTS touchpoint;

# Create and populate DB tables
    USE touchpoint;

    DROP TABLE IF EXISTS email_suffixes;
    CREATE TABLE email_suffixes (
        id INT NOT NULL AUTO_INCREMENT,
        suffix varchar(255) NOT NULL,
        PRIMARY KEY (id)
    );
    INSERT INTO email_suffixes (suffix) VALUES ("ubc.ca");

    CREATE TABLE IF NOT EXISTS persons (
        id INT NOT NULL AUTO_INCREMENT,
        first varchar(255) NOT NULL,
        last varchar(255) NOT NULL,
        password varchar(512) NOT NULL,
        salt varchar(255) NOT NULL,
        email varchar(255) NOT NULL,
        karma INT NOT NULL,
        time INT NOT NULL,
        PRIMARY KEY (id)
    );

# Create a user called **touchpt-dev** with password 'pooltable' and grant full permissions
    GRANT ALL ON touchpoint to 'touchpt-dev'@'localhost' IDENTIFIED BY 'pooltable';
    GRANT ALL PRIVILEGES ON *.* TO 'touchpt-dev'@'localhost' WITH GRANT OPTION;
