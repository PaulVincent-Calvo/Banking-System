

-- NOTE: version and last_modified columns are implemented for concurrency control purposes, 
--       more specifically for editing/updating queries.




-- Tables
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



