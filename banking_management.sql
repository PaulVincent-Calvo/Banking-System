-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 08, 2023 at 08:44 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `banking_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `customermainaccount`
--

CREATE TABLE `customermainaccount` (
  `AccountNumber` varchar(30) NOT NULL,
  `AccountType` varchar(30) DEFAULT NULL,
  `Balance` decimal(9,2) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `OpenedDate` date DEFAULT NULL,
  `CustomerID` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customermainaccount`
--

INSERT INTO `customermainaccount` (`AccountNumber`, `AccountType`, `Balance`, `Status`, `OpenedDate`, `CustomerID`) VALUES
('Acc001', 'Savings', 923.00, 'Active', '2023-01-01', 'Cust001'),
('Acc002', 'Checking', 2500.00, 'Active', '2023-02-15', 'Cust002'),
('Acc003', 'Savings', 7500.00, 'Active', '2023-03-20', 'Cust003'),
('Acc004', 'Savings', 3200.00, 'Active', '2023-04-10', 'Cust004');

-- --------------------------------------------------------

--
-- Table structure for table `userfinanceinfo`
--

CREATE TABLE `userfinanceinfo` (
  `CustomerID` varchar(30) DEFAULT NULL,
  `IDNumber` varchar(30) DEFAULT NULL,
  `Occupation` varchar(50) DEFAULT NULL,
  `AnnualGrossIncome` decimal(9,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userfinanceinfo`
--

INSERT INTO `userfinanceinfo` (`CustomerID`, `IDNumber`, `Occupation`, `AnnualGrossIncome`) VALUES
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

-- --------------------------------------------------------

--
-- Table structure for table `useridentityinfo`
--

CREATE TABLE `useridentityinfo` (
  `IDNumber` varchar(30) NOT NULL,
  `IDType` varchar(50) DEFAULT NULL,
  `SupportingDocs` varchar(50) DEFAULT NULL,
  `CustomerID` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `useridentityinfo`
--

INSERT INTO `useridentityinfo` (`IDNumber`, `IDType`, `SupportingDocs`, `CustomerID`) VALUES
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

-- --------------------------------------------------------

--
-- Table structure for table `userpersonalinfo`
--

CREATE TABLE `userpersonalinfo` (
  `CustomerID` varchar(30) NOT NULL,
  `UserFName` varchar(50) DEFAULT NULL,
  `UserLName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userpersonalinfo`
--

INSERT INTO `userpersonalinfo` (`CustomerID`, `UserFName`, `UserLName`) VALUES
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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customermainaccount`
--
ALTER TABLE `customermainaccount`
  ADD PRIMARY KEY (`AccountNumber`),
  ADD KEY `fk3_customerID` (`CustomerID`);

--
-- Indexes for table `userfinanceinfo`
--
ALTER TABLE `userfinanceinfo`
  ADD KEY `fk2_customerID` (`CustomerID`),
  ADD KEY `fk_idNumber` (`IDNumber`);

--
-- Indexes for table `useridentityinfo`
--
ALTER TABLE `useridentityinfo`
  ADD PRIMARY KEY (`IDNumber`),
  ADD KEY `fk_customerID` (`CustomerID`);

--
-- Indexes for table `userpersonalinfo`
--
ALTER TABLE `userpersonalinfo`
  ADD PRIMARY KEY (`CustomerID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customermainaccount`
--
ALTER TABLE `customermainaccount`
  ADD CONSTRAINT `fk3_customerID` FOREIGN KEY (`CustomerID`) REFERENCES `userpersonalinfo` (`CustomerID`);

--
-- Constraints for table `userfinanceinfo`
--
ALTER TABLE `userfinanceinfo`
  ADD CONSTRAINT `fk2_customerID` FOREIGN KEY (`CustomerID`) REFERENCES `userpersonalinfo` (`CustomerID`),
  ADD CONSTRAINT `fk_idNumber` FOREIGN KEY (`IDNumber`) REFERENCES `useridentityinfo` (`IDNumber`);

--
-- Constraints for table `useridentityinfo`
--
ALTER TABLE `useridentityinfo`
  ADD CONSTRAINT `fk_customerID` FOREIGN KEY (`CustomerID`) REFERENCES `userpersonalinfo` (`CustomerID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
