
ALTER USER 'admin'@'localhost' IDENTIFIED BY 'new_password';

GRANT ALL PRIVILEGES ON banking_system.* TO 'admin'@'localhost';



-- FOR FORMALITY (baka hanapin ng teacher namin sa dbms)
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

CREATE TABLE checkings_account(
  checkings_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  balance DECIMAL(20, 2),
  CONSTRAINT fk_custID FOREIGN KEY(customer_id) REFERENCES customer_information(customer_id)
);


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


-- VIEW for Customer ID, Fullname, Email, and Checkings ID
CREATE VIEW Customer_Info_CheckingID AS
SELECT 
  customer_information.customer_id, 
  CONCAT(customer_information.first_name, ' ', customer_information.last_name) AS FullName, 
  customer_information.email, 
  checkings_account.checkings_id
FROM 
  customer_information
INNER JOIN 
  checkings_account ON customer_information.customer_id = checkings_account.customer_id;


SELECT * FROM Customer_Info_CheckingID;





-- Insert data into customer_information table
INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income)
VALUES
  ('pass1', 'John', 'Doe', 'john.doe@example.com', '123 Main St', 'Driver License', 'Engineer', 75000.00),
  ('pass2', 'Jane', 'Smith', 'jane.smith@example.com', '456 Oak St', 'Passport', 'Teacher', 60000.00),
  ('pass3', 'Mike', 'Johnson', 'mike.johnson@example.com', '789 Pine St', 'SSN', 'Doctor', 100000.00),
  ('pass4', 'Emily', 'Williams', 'emily.williams@example.com', '101 Elm St', 'Passport', 'Artist', 50000.00),
  ('pass5', 'Chris', 'Miller', 'chris.miller@example.com', '202 Birch St', 'Driver License', 'IT Specialist', 80000.00),
  ('pass6', 'Linda', 'Brown', 'linda.brown@example.com', '303 Cedar St', 'SSN', 'Lawyer', 120000.00),
  ('pass7', 'Mark', 'Taylor', 'mark.taylor@example.com', '404 Maple St', 'Passport', 'Accountant', 90000.00),
  ('pass8', 'Sarah', 'Clark', 'sarah.clark@example.com', '505 Pine St', 'Driver License', 'Marketing Specialist', 70000.00),
  ('pass9', 'Brian', 'Anderson', 'brian.anderson@example.com', '606 Oak St', 'SSN', 'Sales Manager', 110000.00),
  ('pass10', 'Amy', 'Roberts', 'amy.roberts@example.com', '707 Birch St', 'Passport', 'Writer', 60000.00);

-- Insert data into checkings_account table
INSERT INTO checkings_account (customer_id, balance)
VALUES
  (1, 5000.00),
  (2, 8000.00),
  (3, 12000.00),
  (4, 3000.00),
  (5, 10000.00),
  (6, 15000.00),
  (7, 6000.00),
  (8, 9000.00),
  (9, 11000.00),
  (10, 7500.00);

-- Insert data into bank_asset table
INSERT INTO bank_asset (checkings_id, checkings_balance)
VALUES
  (1, 5000.00),
  (2, 8000.00),
  (3, 12000.00),
  (4, 3000.00),
  (5, 10000.00),
  (6, 15000.00),
  (7, 6000.00),
  (8, 9000.00),
  (9, 11000.00),
  (10, 7500.00);

-- Insert data into transactions table
INSERT INTO transactions (checkings_id, transaction_date, amount, transaction_type)
VALUES
  (1, '2023-01-01', 1000.00, 'Deposit'),
  (2, '2023-01-02', 500.00, 'Withdrawal'),
  (3, '2023-01-03', 1500.00, 'Deposit'),
  (4, '2023-01-04', 200.00, 'Withdrawal'),
  (5, '2023-01-05', 800.00, 'Deposit'),
  (6, '2023-01-06', 1200.00, 'Withdrawal'),
  (7, '2023-01-07', 300.00, 'Deposit'),
  (8, '2023-01-08', 600.00, 'Withdrawal'),
  (9, '2023-01-09', 1000.00, 'Deposit'),
  (10, '2023-01-10', 400.00, 'Withdrawal');

