-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2023 at 04:02 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


-- Table structure for table `checkings_account`
--

CREATE TABLE `checkings_account` (
  `checkings_id` varchar(10) NOT NULL,
  `account_password` varchar(20) NOT NULL,
  `balance` decimal(20,2) DEFAULT NULL,
  `account_status` varchar(10) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT current_timestamp(),
  `version` int(11) DEFAULT 0,
  `customer_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `checkings_account`
--

INSERT INTO `checkings_account` (`checkings_id`, `account_password`, `balance`, `account_status`, `last_modified`, `version`, `customer_id`) VALUES
('ATC231', 'pass123', 5000.00, 'Active', '2023-12-08 02:43:01', 2, 21),
('ATC232', 'secure456', 20000.00, 'Active', '2023-12-08 02:43:03', 1, 22),
('ATC233', 'mysecret', 7500.00, 'Inactive', '2023-12-07 15:22:14', 0, 23),
('ATC234', 'safe789', 12000.00, 'Active', '2023-12-07 15:22:14', 0, 24),
('ATC235', 'hidden567', 3000.00, 'Inactive', '2023-12-07 15:22:14', 0, 25),
('ATCIEB', 'ATCRIF', 0.00, '9888', '2023-12-07 18:49:55', 0, 29),
('ATCJEV', 'ATCFJT', 98.00, 'Active', '2023-12-07 17:09:43', 0, 26),
('ATCQZ5', 'ATCHVT', 0.00, '98', '2023-12-07 18:24:00', 0, 28);

-- --------------------------------------------------------

--
-- Stand-in structure for view `checkings_account_view`
-- (See below for the actual view)
--
CREATE TABLE `checkings_account_view` (
`checkings_id` varchar(10)
,`account_password` varchar(20)
,`balance` decimal(20,2)
,`account_status` varchar(10)
,`customer_id` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `customer_checkings_view`
-- (See below for the actual view)
--
CREATE TABLE `customer_checkings_view` (
`customer_id` int(11)
,`customer_name` varchar(61)
,`email` varchar(40)
,`address` varchar(60)
,`id_type` varchar(30)
,`occupation` varchar(30)
,`annual_gross_income` decimal(20,2)
,`checkings_id` varchar(10)
,`account_password` varchar(20)
,`balance` decimal(20,2)
,`account_status` varchar(10)
);

-- --------------------------------------------------------

--
-- Table structure for table `customer_information`
--

CREATE TABLE `customer_information` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `address` varchar(60) DEFAULT NULL,
  `id_type` varchar(30) DEFAULT NULL,
  `occupation` varchar(30) DEFAULT NULL,
  `annual_gross_income` decimal(20,2) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT current_timestamp(),
  `version` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_information`
--

INSERT INTO `customer_information` (`customer_id`, `first_name`, `last_name`, `email`, `address`, `id_type`, `occupation`, `annual_gross_income`, `last_modified`, `version`) VALUES
(21, 'John', 'Doe', 'john.doe@email.com', '123 Main St, Cityville', 'Driver\'s License', 'Engineer', 75000.00, '2023-12-07 15:18:44', 0),
(22, 'Jane', 'Smith', 'jane.smith@email.com', '456 Oak St, Townsville', 'Passport', 'Teacher', 60000.00, '2023-12-07 15:18:44', 0),
(23, 'Alice', 'Johnson', 'alice.johnson@email.com', '789 Pine St, Villageton', 'ID Card', 'Doctor', 100000.00, '2023-12-07 15:18:44', 0),
(24, 'Bob', 'Williams', 'bob.williams@email.com', '101 Cedar St, Hamletville', 'Passport', 'Accountant', 80000.00, '2023-12-07 15:18:44', 0),
(25, 'Eva', 'Jones', 'eva.jones@email.com', '202 Birch St, Settlement City', 'Driver\'s License', 'Artist', 50000.00, '2023-12-07 15:18:44', 0),
(26, 'Ace', 'Doe', 'john.doe@email.com', '123 Main St, Cityville', 'Driver\'s License', 'Engineer', 75000.00, '2023-12-07 17:03:06', 0),
(27, 'Kim', 'Doe', 'kimdoe@gmail.com', 'Wawa', 'Passport', 'Nurse', 98.00, '2023-12-07 18:10:59', 0),
(28, 'Ace', 'Gadores', 'acegado@gmail.come', 'Wawa', 'Passport', 'Nurse', 98.00, '2023-12-07 18:22:45', 0),
(29, 'Lisa', 'Manoban', 'lisa@gmail.com', 'SoKor', 'Passport', 'KPOP Idol', 8999999.00, '2023-12-07 18:49:24', 0),
(30, 'Kim', 'Sana', 'kimsana@gmail.com', 'Brgy. Wawa', 'Passport', 'Idol', 1111111.00, '2023-12-08 02:13:12', 0);

-- --------------------------------------------------------

--
-- Stand-in structure for view `customer_information_view`
-- (See below for the actual view)
--
CREATE TABLE `customer_information_view` (
`customer_id` int(11)
,`first_name` varchar(30)
,`last_name` varchar(30)
,`email` varchar(40)
,`address` varchar(60)
,`id_type` varchar(30)
,`occupation` varchar(30)
,`annual_gross_income` decimal(20,2)
);

-- --------------------------------------------------------

--
-- Table structure for table `employee_admin`
--

CREATE TABLE `employee_admin` (
  `employee_id` varchar(6) NOT NULL,
  `employee_password` varchar(20) NOT NULL,
  `emp_fname` varchar(30) DEFAULT NULL,
  `emp_lname` varchar(30) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT current_timestamp(),
  `version` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_admin`
--

INSERT INTO `employee_admin` (`employee_id`, `employee_password`, `emp_fname`, `emp_lname`, `email`, `phone`, `address`, `last_modified`, `version`) VALUES
('ETC231', 'oneinamillion', 'Ace', 'Gadores', 'acepenaflorida@gmail.com', '09919394735', 'Mars St. Golden Country Homes Brgy. Alangilan, Bat', '2023-11-25 08:00:22', 0);

-- --------------------------------------------------------

--
-- Stand-in structure for view `fetch_username`
-- (See below for the actual view)
--
CREATE TABLE `fetch_username` (
`checkings_id` varchar(10)
,`first_name` varchar(30)
);

-- --------------------------------------------------------

--
-- Table structure for table `session_log`
--

CREATE TABLE `session_log` (
  `session_log_id` int(11) NOT NULL,
  `employee_id` varchar(6) DEFAULT NULL,
  `session_date` date DEFAULT curdate(),
  `session_type` varchar(30) DEFAULT NULL,
  `table_involved` varchar(15) DEFAULT NULL,
  `column_involved` varchar(15) DEFAULT NULL,
  `modified_value` varchar(30) DEFAULT NULL,
  `stored_value` varchar(30) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT current_timestamp(),
  `version` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `session_log`
--

INSERT INTO `session_log` (`session_log_id`, `employee_id`, `session_date`, `session_type`, `table_involved`, `column_involved`, `modified_value`, `stored_value`, `status`, `last_modified`, `version`) VALUES
(650, 'ETC231', '2023-12-07', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-06 16:59:15', 0),
(651, 'ETC231', '2023-12-07', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-06 17:20:17', 0),
(652, 'ETC231', '2023-12-07', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-06 17:25:07', 0),
(653, 'ETC231', '2023-12-07', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-06 17:28:05', 0),
(654, 'ETC231', '2023-12-07', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-06 17:32:20', 0),
(741, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 19:45:31', 0),
(742, 'ETC231', '2023-12-08', 'Edit User', 'transactions', 'transactions_id', 'TTCYCO', 'TTCUB4', 'Successful', '2023-12-07 19:45:59', 0),
(743, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 19:51:54', 0),
(744, 'ETC231', '2023-12-08', 'Edit User', 'transactions', 'transactions_id', 'TTCIAT', 'TTCCOP', 'Successful', '2023-12-07 19:52:51', 0),
(745, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 20:04:16', 0),
(746, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 20:06:24', 0),
(747, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 23:53:35', 0),
(748, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 23:55:00', 0),
(749, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-07 23:58:41', 0),
(750, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 00:00:29', 0),
(751, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 00:05:35', 0),
(752, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 00:09:05', 0),
(753, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 00:15:37', 0),
(754, 'etc231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 00:22:19', 0),
(755, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 01:24:18', 0),
(756, 'ETC231', '2023-12-08', 'View User', 'customer_inform', NULL, NULL, NULL, 'Successful', '2023-12-08 02:11:14', 0),
(757, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'first_name', 'None', 'Kim', 'Successful', '2023-12-08 02:13:13', 0),
(758, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'last_name', 'None', 'Sana', 'Successful', '2023-12-08 02:13:13', 0),
(759, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'email', 'None', 'kimsana@gmail.com', 'Successful', '2023-12-08 02:13:13', 0),
(760, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'address', 'None', 'Brgy. Wawa', 'Successful', '2023-12-08 02:13:13', 0),
(761, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'id_type', 'None', 'Passport', 'Successful', '2023-12-08 02:13:13', 0),
(762, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'occupation', 'None', 'Idol', 'Successful', '2023-12-08 02:13:13', 0),
(763, 'ETC231', '2023-12-08', 'Add User', 'Customer Inform', 'annual_gross_in', 'None', '1111111', 'Successful', '2023-12-08 02:13:13', 0);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `transactions_id` varchar(10) NOT NULL,
  `checkings_id` varchar(6) DEFAULT NULL,
  `transaction_type` varchar(15) DEFAULT NULL,
  `receiving_account` varchar(6) NOT NULL,
  `transaction_date` date DEFAULT curdate(),
  `amount` decimal(20,2) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT current_timestamp(),
  `version` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`transactions_id`, `checkings_id`, `transaction_type`, `receiving_account`, `transaction_date`, `amount`, `last_modified`, `version`) VALUES
('TTC1PQ', 'ATC231', 'Deposit', 'None', '2023-12-08', 10000.00, '2023-12-08 02:42:45', 0),
('TTC231', 'ATC231', 'Deposit', 'ATC231', '2023-12-07', 2000.00, '2023-12-07 15:31:15', 0),
('TTC232', 'ATC232', 'Withdrawal', 'ATC232', '2023-12-07', 1500.00, '2023-12-07 15:31:15', 0),
('TTC233', 'ATC233', 'Transfer', 'ATC234', '2023-12-07', 500.00, '2023-12-07 15:31:15', 0),
('TTC234', 'ATC234', 'Deposit', 'ATC234', '2023-12-07', 3000.00, '2023-12-07 15:31:15', 0),
('TTC3TV', 'ATC235', 'Withdrawal', 'ATC235', '2023-12-07', 1000.00, '2023-12-07 15:31:15', 0),
('TTCCOP', 'ATC231', 'Withdraw', 'None', '2009-01-09', 69.00, '2023-12-07 17:41:08', 0),
('TTCUB4', 'ATCQZ5', 'Deposit', 'None', '2009-08-01', 65.00, '2023-12-07 18:25:10', 0),
('TTCXLK', 'ATC231', 'Transfer', 'ATC232', '2023-12-08', 10000.00, '2023-12-08 02:43:03', 0);

-- --------------------------------------------------------

--
-- Stand-in structure for view `transactions_view`
-- (See below for the actual view)
--
CREATE TABLE `transactions_view` (
`transactions_id` varchar(10)
,`checkings_id` varchar(6)
,`transaction_type` varchar(15)
,`receiving_account` varchar(6)
,`transaction_date` date
,`amount` decimal(20,2)
);

-- --------------------------------------------------------

--
-- Structure for view `checkings_account_view`
--
DROP TABLE IF EXISTS `checkings_account_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `checkings_account_view`  AS SELECT `checkings_account`.`checkings_id` AS `checkings_id`, `checkings_account`.`account_password` AS `account_password`, `checkings_account`.`balance` AS `balance`, `checkings_account`.`account_status` AS `account_status`, `checkings_account`.`customer_id` AS `customer_id` FROM `checkings_account` ;

-- --------------------------------------------------------

--
-- Structure for view `customer_checkings_view`
--
DROP TABLE IF EXISTS `customer_checkings_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_checkings_view`  AS SELECT `c`.`customer_id` AS `customer_id`, concat(`c`.`first_name`,' ',`c`.`last_name`) AS `customer_name`, `c`.`email` AS `email`, `c`.`address` AS `address`, `c`.`id_type` AS `id_type`, `c`.`occupation` AS `occupation`, `c`.`annual_gross_income` AS `annual_gross_income`, `ca`.`checkings_id` AS `checkings_id`, `ca`.`account_password` AS `account_password`, `ca`.`balance` AS `balance`, `ca`.`account_status` AS `account_status` FROM (`customer_information` `c` join `checkings_account` `ca` on(`c`.`customer_id` = `ca`.`customer_id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `customer_information_view`
--
DROP TABLE IF EXISTS `customer_information_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_information_view`  AS SELECT `customer_information`.`customer_id` AS `customer_id`, `customer_information`.`first_name` AS `first_name`, `customer_information`.`last_name` AS `last_name`, `customer_information`.`email` AS `email`, `customer_information`.`address` AS `address`, `customer_information`.`id_type` AS `id_type`, `customer_information`.`occupation` AS `occupation`, `customer_information`.`annual_gross_income` AS `annual_gross_income` FROM `customer_information` ;

-- --------------------------------------------------------

--
-- Structure for view `fetch_username`
--
DROP TABLE IF EXISTS `fetch_username`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `fetch_username`  AS SELECT `check_acc`.`checkings_id` AS `checkings_id`, `cust`.`first_name` AS `first_name` FROM (`customer_information` `cust` join `checkings_account` `check_acc` on(`cust`.`customer_id` = `check_acc`.`customer_id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `transactions_view`
--
DROP TABLE IF EXISTS `transactions_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `transactions_view`  AS SELECT `transactions`.`transactions_id` AS `transactions_id`, `transactions`.`checkings_id` AS `checkings_id`, `transactions`.`transaction_type` AS `transaction_type`, `transactions`.`receiving_account` AS `receiving_account`, `transactions`.`transaction_date` AS `transaction_date`, `transactions`.`amount` AS `amount` FROM `transactions` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `checkings_account`
--
ALTER TABLE `checkings_account`
  ADD PRIMARY KEY (`checkings_id`),
  ADD UNIQUE KEY `checkings_id` (`checkings_id`),
  ADD KEY `fk_customerID` (`customer_id`);

--
-- Indexes for table `customer_information`
--
ALTER TABLE `customer_information`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `employee_admin`
--
ALTER TABLE `employee_admin`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `session_log`
--
ALTER TABLE `session_log`
  ADD PRIMARY KEY (`session_log_id`),
  ADD KEY `fk_employee_id` (`employee_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transactions_id`),
  ADD KEY `fk_checkingsID_2` (`checkings_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer_information`
--
ALTER TABLE `customer_information`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `session_log`
--
ALTER TABLE `session_log`
  MODIFY `session_log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=764;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `checkings_account`
--
ALTER TABLE `checkings_account`
  ADD CONSTRAINT `fk_customerID` FOREIGN KEY (`customer_id`) REFERENCES `customer_information` (`customer_id`);

--
-- Constraints for table `session_log`
--
ALTER TABLE `session_log`
  ADD CONSTRAINT `fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee_admin` (`employee_id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_checkingsID_2` FOREIGN KEY (`checkings_id`) REFERENCES `checkings_account` (`checkings_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
