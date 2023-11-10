
CREATE TABLE UserPersonalInfo(
  CustomerID VARCHAR(30) PRIMARY KEY UNIQUE,
  UserFName VARCHAR(50),
  UserLName VARCHAR(50)
);


CREATE TABLE UserIdentityInfo(
  IDNumber VARCHAR(30) PRIMARY KEY UNIQUE NOT NULL,
  IDType VARCHAR(50),
  SupportingDocs VARCHAR(50),
  CustomerID VARCHAR(30),
  CONSTRAINT fk_customerID FOREIGN KEY(CustomerID) REFERENCES UserPersonalInfo(CustomerID)
);


CREATE TABLE UserFinanceInfo(
  CustomerID VARCHAR(30),
  IDNumber VARCHAR(30),
  Occupation VARCHAR(50),
  AnnualGrossIncome DECIMAL(20, 10),
  CONSTRAINT fk2_customerID FOREIGN KEY(CustomerID) REFERENCES UserPersonalInfo(CustomerID),
  CONSTRAINT fk_idNumber FOREIGN KEY(IDNumber) REFERENCES UserIdentityInfo(IDNumber)
);


CREATE TABLE CustomerMainAccount(
  AccountNumber VARCHAR(30) PRIMARY KEY UNIQUE NOT NULL,
  AccountType VARCHAR(30),
  Balance DECIMAL(50, 20),
  Status VARCHAR(20),
  OpenedDate DATE,
  CustomerID VARCHAR(30),
  CONSTRAINT fk3_customerID FOREIGN KEY(CustomerID) REFERENCES UserPersonalInfo(CustomerID)
);


-- TO EASILY ACCESS ALL RECORDS W/OUT THE NEED OF putting the actual query in the python code: (Note: to access a view: SELECT * FROM all_records)
CREATE VIEW all_records AS
SELECT 
  P.CustomerID, 
  C.accountnumber, 
  C.AccountType, 
  P.UserFName, 
  P.UserLName, 
  FORMAT(C.Balance, 2) AS Balance, 
  C.Status, 
  I.IDNumber, 
  I.IDType, 
  F.Occupation, 
  FORMAT(F.AnnualGrossIncome, 2) AS AnnualGrossIncome 
FROM 
  CustomerMainAccount AS C  
JOIN UserPersonalInfo AS P ON C.CustomerID = P.CustomerID 
JOIN UserIdentityInfo AS I ON C.CustomerID = I.CustomerID AND C.CustomerID = I.CustomerID 
JOIN UserFinanceInfo AS F ON C.CustomerID = F.CustomerID AND I.IDNumber = F.IDNumber;


INSERT INTO UserPersonalInfo (CustomerID, UserFName, UserLName)
VALUES
  ('Cust001', 'John', 'Doe'),
  ('Cust002', 'Alice', 'Smith'),
  ('Cust003', 'Bob', 'Johnson'),
  ('Cust004', 'Eva', 'Brown'),
  ('Cust005', 'David', 'Williams'),
  ('Cust006', 'Sarah', 'Wilson'),
  ('Cust007', 'Michael', 'Lee'),
  ('Cust008', 'Olivia', 'Davis'),
  ('Cust009', 'James', 'Miller'),
  ('Cust010', 'Emily', 'Garcia');


INSERT INTO UserIdentityInfo (IDNumber, IDType, SupportingDocs, CustomerID)
VALUES
  ('ID001', 'Passport', 'Passport scan', 'Cust001'),
  ('ID002', 'Driver License', 'License scan', 'Cust002'),
  ('ID003', 'Social Security', 'SSN scan', 'Cust003'),
  ('ID004', 'Passport', 'Passport scan', 'Cust004'),
  ('ID005', 'Driver License', 'License scan', 'Cust005'),
  ('ID006', 'Social Security', 'SSN scan', 'Cust006'),
  ('ID007', 'Passport', 'Passport scan', 'Cust007'),
  ('ID008', 'Driver License', 'License scan', 'Cust008'),
  ('ID009', 'Social Security', 'SSN scan', 'Cust009'),
  ('ID010', 'Passport', 'Passport scan', 'Cust010');


INSERT INTO UserFinanceInfo (CustomerID, IDNumber, Occupation, AnnualGrossIncome)
VALUES
  ('Cust001', 'ID001', 'Engineer', 75000.00),
  ('Cust002', 'ID002', 'Teacher', 55000.00),
  ('Cust003', 'ID003', 'Doctor', 100000.00),
  ('Cust004', 'ID004', 'Accountant', 60000.00),
  ('Cust005', 'ID005', 'Lawyer', 90000.00),
  ('Cust006', 'ID006', 'Nurse', 52000.00),
  ('Cust007', 'ID007', 'Software Developer', 80000.00),
  ('Cust008', 'ID008', 'Artist', 45000.00),
  ('Cust009', 'ID009', 'Dentist', 110000.00),
  ('Cust010', 'ID010', 'Architect', 72000.00);


INSERT INTO CustomerMainAccount (AccountNumber, AccountType, Balance, Status, OpenedDate, CustomerID)
VALUES
  ('Acc001', 'Savings', 5000.00, 'Active', '2023-01-01', 'Cust001'),
  ('Acc002', 'Checking', 2500.00, 'Active', '2023-02-15', 'Cust002'),
  ('Acc003', 'Savings', 7500.00, 'Active', '2023-03-20', 'Cust003'),
  ('Acc004', 'Checking', 3200.00, 'Active', '2023-04-10', 'Cust004'),
  ('Acc005', 'Savings', 9800.00, 'Active', '2023-05-05', 'Cust005'),
  ('Acc006', 'Checking', 4500.00, 'Active', '2023-06-12', 'Cust006'),
  ('Acc007', 'Savings', 6800.00, 'Active', '2023-07-17', 'Cust007'),
  ('Acc008', 'Checking', 2900.00, 'Active', '2023-08-22', 'Cust008'),
  ('Acc009', 'Savings', 10500.00, 'Active', '2023-09-25', 'Cust009'),
  ('Acc010', 'Checking', 5200.00, 'Active', '2023-10-10', 'Cust010');
