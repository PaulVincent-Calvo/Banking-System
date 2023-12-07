

-- VIEWS:


CREATE VIEW customer_information_view AS
SELECT
  customer_id,
  first_name,
  last_name,
  email,
  address,
  id_type,
  occupation,
  annual_gross_income
FROM
  customer_information;






CREATE TABLE employee_admin( -- ETC231(Employee Treasury Citadel, year, number)
  employee_id VARCHAR(6) NOT NULL UNIQUE PRIMARY KEY,
  employee_password VARCHAR(20) NOT NULL,
  emp_fname VARCHAR(30),
  emp_lname VARCHAR(30),
  email VARCHAR(40),
  phone VARCHAR(11),
  address VARCHAR(50),
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT DEFAULT 0
);


CREATE VIEW transactions_view AS
SELECT
  transactions_id,
  checkings_id,
  transaction_type,
  receiving_account,
  transaction_date,
  amount
FROM transactions;




INSERT INTO employee_admin(employee_id, employee_password, emp_fname, emp_lname, email, phone, address)
VALUES("ETC231", "oneinamillion", "Ace", "Gadores", "acepenaflorida@gmail.com", "09919394735", "Mars St. Golden Country Homes Brgy. Alangilan, Batangas City");


CREATE TABLE session_log(
  session_log_id INT AUTO_INCREMENT PRIMARY KEY,
  employee_id VARCHAR(6), -- foreign key
  session_date DATE DEFAULT CURRENT_DATE(),
  session_type VARCHAR(30),
  table_involved VARCHAR(15),
  column_involved VARCHAR(15),
  modified_value VARCHAR(30),
  stored_value VARCHAR(30),
  status VARCHAR(10),
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT DEFAULT 0,
  CONSTRAINT fk_employee_id FOREIGN KEY(employee_id) REFERENCES employee_admin(employee_id)
);




CREATE TABLE customer_information(
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  email VARCHAR(40),
  address VARCHAR(60),
  id_type VARCHAR(30),
  occupation VARCHAR(30),
  annual_gross_income DECIMAL(20,2),
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT DEFAULT 0
);



INSERT INTO customer_information(first_name, last_name, email, address, id_type, occupation, annual_gross_income)
VALUES("Paul", "Calvo", "paulcalvo@gmail.com", "Somewhere in Bauan nearby the sea", "National ID", "Pabigat daw sya", "100000");

INSERT INTO customer_information(first_name, last_name, email, address, id_type, occupation, annual_gross_income)
VALUES
  ("Ace", "Gadores", "ace@gmail.com", "Somewhere in Nasugbu nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("Aaron", "Crisologo", "aeroncrisologo@gmail.com", "Somewhere in Lipa nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("John Benedict", "Dunno", "john_bene@gmail.com", "Somewhere in Bauan nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("Nielle", "Barcelona", "niellebarcelona@gmail.com", "Somewhere in Rosario nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("Franz", "Ramos", "franzramossheesh@gmail.com", "Somewhere in Bauan nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("Czynon", "De Torres", "czy_detor_panget_niGunwookjk@gmail.com", "Somewhere in Bauan nearby the sea", "National ID", "Pabigat daw sya", "100000"),
  ("Princess", "Delos Santos", "princess_thea_sakalam@gmail.com", "Somewhere in Lian nearby the sea", "National ID", "Pabigat daw sya", "100000");



CREATE TABLE checkings_account( -- ATC231(Account Treasury Citadel, year, number)
  checkings_id VARCHAR(10) UNIQUE NOT NULL PRIMARY KEY,
  account_password VARCHAR(20) NOT NULL,
  balance DECIMAL(20, 2),
  account_status VARCHAR(10),
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT DEFAULT 0,
  customer_id INT,
  CONSTRAINT fk_customerID FOREIGN KEY(customer_id) REFERENCES customer_information(customer_id)
);

CREATE VIEW checkings_account_view AS
SELECT
  checkings_id,
  account_password,
  balance,
  account_status,
  customer_id
FROM
  checkings_account;

CREATE VIEW fetch_username AS
SELECT 
  check_acc.checkings_id,
  cust.first_name
FROM customer_information cust
JOIN checkings_account check_acc ON cust.customer_id = check_acc.customer_id;

SELECT * FROM fetch_username;

DROP VIEW fetch_username;



SELECT * FROM checkings_account;


SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.address,
    c.id_type,
    c.occupation,
    c.annual_gross_income,
    ca.checkings_id,
    ca.account_password,
    ca.balance,
    ca.account_status
FROM
    customer_information c
JOIN
    checkings_account ca ON c.customer_id = ca.customer_id;


SELECT * FROM customer_information;


ALTER TABLE checkings_account
MODIFY COLUMN checkings_id VARCHAR(10) UNIQUE NOT NULL;

INSERT INTO checkings_account(checkings_id, account_password, balance, account_status, customer_id)
VALUES
  ("ATC233", "stankissoflife", 10009, "Active", 4),
  ("ATC234", "pengedos", 9231987.15, "Active", 5),
  ("ATC235", "nakakapuntangina", 9232.15, "Active", 6),
  ("ATC236", "tatlong_bilyo", 921.15, "Active", 7),
  ("ATC237", "ikaw lang aking gusto", 200, "Active", 8),
  ("ATC238", "ediwow_", 32099, "Active", 9),
  ("ATC239", "penge_decibel_tix", 120.00, "Inactive", 10),
  ("ATC2310", "ediwow_", 32099, "Active", 11);




CREATE TABLE transactions(
  transactions_id INT AUTO_INCREMENT PRIMARY KEY, -- TTC-23-1 (Transaction Treasury Citadel - year - number())
  checkings_id VARCHAR(6), -- FOREIGN key(it's also the sending_account in transfer)
  transaction_type VARCHAR(15),
  receiving_account VARCHAR(6) NOT NULL,
  transaction_date DATE DEFAULT CURRENT_DATE,
  amount DECIMAL(20,2),
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT DEFAULT 0,
  CONSTRAINT fk_checkingsID_2 FOREIGN KEY(checkings_id) REFERENCES checkings_account(checkings_id)
);

DROP TABLE transactions;

INSERT INTO transactions(transactions_id, checkings_id, transaction_type, receiving_account, amount)
VALUES("TTC231", "ATC231", "Withdraw", "None", 9882.32);




SELECT * FROM employee_admin;
SELECT * FROM session_log;
SELECT * FROM customer_information;
SELECT * FROM checkings_account;
SELECT * FROM transactions;


-- DONE: view, edit, Delete, add
-- DONE: transactions log





















CREATE TABLE session_log(
  session_log_id INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
  session_type VARCHAR(10),
  table_involved VARCHAR(20),
  column_involved VARCHAR(15),
  modified_value VARCHAR(30),
  stored_value VARCHAR(30),
  session_date DATE,
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  version INT NOT NULL DEFAULT 0
);



CREATE TABLE employees(
  employee_id INT AUTO_INCREMENT UNIQUE NOT NULl PRIMARY KEY,
  employee_password VARCHAR(30),
  emp_fname VARCHAR(30),
  emp_lname VARCHAR(30),
  email VARCHAR(30) UNIQUE,
  address VARCHAR(50),
  salary DECIMAL(10,2)
);


CREATE TABLE customer_information(
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_password VARCHAR(20) NOT NULL,
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  email VARCHAR(40),
  address VARCHAR(60),
  id_type VARCHAR(30),
  occupation VARCHAR(30),
  annual_gross_income DECIMAL(20,2)
);


INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income)
VALUES("020304", "Ace", "Gadores", "ace@email.com", "GCH", "Passport", "Pabigat", "90"), 
      ("12345", "Aeron", "Lol", "ace@email.com", "GCH", "Passport", "Pabigat", "90");



CREATE TABLE checkings_account(
  checkings_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  balance DECIMAL(20, 2),
  CONSTRAINT fk_custID FOREIGN KEY(customer_id) REFERENCES customer_information(customer_id)
);


SELECT customer_information.customer_id, checkings_account.checkings_id, customer_password, first_name, last_name
FROM customer_information
JOIN checkings_account ON customer_information.customer_id = checkings_account.customer_id
WHERE checkings_account.checkings_id = 2;



CREATE TABLE bank_asset(
  asset_id INT AUTO_INCREMENT PRIMARY KEY,
  checkings_id INT,
  checkings_balance DECIMAL(20,2),
  CONSTRAINT fk_checkingsID FOREIGN KEY(checkings_id) REFERENCES checkings_account(checkings_id)
);


CREATE TABLE transactions(
  transactions_id INT AUTO_INCREMENT PRIMARY KEY,
  checkings_id INT, -- FOREIGN key
  transaction_date DATE,
  amount DECIMAL(20,2),
  transaction_type VARCHAR(15),
  CONSTRAINT fk_checkingsID_2 FOREIGN KEY(checkings_id) REFERENCES checkings_account(checkings_id)
);





SELECT * FROM checkings_account;

ALTER TABLE customer_information 
ADD COLUMN version INT NOT NULL DEFAULT 0;

ALTER TABLE customer_information 
ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;


ALTER TABLE checkings_account 
ADD COLUMN version INT NOT NULL DEFAULT 0;

ALTER TABLE checkings_account 
ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE bank_asset 
ADD COLUMN version INT NOT NULL DEFAULT 0;

ALTER TABLE bank_asset 
ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE transactions 
ADD COLUMN version INT NOT NULL DEFAULT 0;

ALTER TABLE transactions 
ADD COLUMN last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE checkings_account
MODIFY COLUMN customer_id INT UNIQUE;

ALTER TABLE bank_asset 
MODIFY COLUMN checkings_id INT UNIQUE;

ALTER TABLE transactions
MODIFY COLUMN checkings_id INT;


ALTER TABLE transactions
ADD CONSTRAINT unique_checkings_id UNIQUE (checkings_id);



-- VIEW for all records
CREATE VIEW all_records AS
SELECT
    ci.customer_id,
    ci.first_name,
    ci.last_name,
    ci.email,
    ci.address,
    ci.id_type,
    ci.occupation,
    ci.annual_gross_income,
    ca.checkings_id,
    ca.balance AS checkings_balance,
    ba.asset_id,
    ba.checkings_balance AS bank_asset_balance,
    t.transactions_id,
    t.transaction_date,
    t.amount,
    t.transaction_type
    FROM
        customer_information ci
    JOIN
        checkings_account ca ON ci.customer_id = ca.customer_id
    JOIN
        bank_asset ba ON ca.checkings_id = ba.checkings_id
    JOIN
        transactions t ON ca.checkings_id = t.checkings_id;

SELECT * FROM all_records;






-- Insert data into customer_information table
INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income)
VALUES
  ('pass1', 'John', 'Doe', 'john.doe@example.com', '123 Main St', 'Driver License', 'Engineer', 75000.00),
  ('pass2', 'Jane', 'Smith', 'jane.smith@example.com', '456 Oak St', 'Passport', 'Teacher', 60000.00);



-- Insert data into checkings_account table
INSERT INTO checkings_account (customer_id, balance)
VALUES
  (1, 5000.00),
  (2, 8000.00);



-- Insert data into bank_asset table
INSERT INTO bank_asset (checkings_id, checkings_balance)
VALUES
  (1, 5000.00),
  (2, 8000.00);

-- Insert data into transactions table
INSERT INTO transactions (checkings_id, transaction_date, amount, transaction_type)
VALUES
  (1, '2023-01-01', 1000.00, 'Deposit'),
  (2, '2023-01-02', 500.00, 'Withdrawal');

SELECT * FROM customer_information;
