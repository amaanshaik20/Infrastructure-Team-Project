USE master;
GO

IF EXISTS (SELECT * FROM sys.databases WHERE name = 'InfraDB')
BEGIN
    ALTER DATABASE InfraDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE InfraDB;
END
GO




create database InfraDB;

use InfraDB;


SELECT * FROM ITEM_MASTER;
SELECT * FROM Inventory_Onhand;
SELECT * FROM PO_HEADER;
SELECT * FROM PO_LINES;
SELECT * FROM Lookup_Type;
SELECT * FROM Lookup_Values;



-- Create ITEM_MASTER table
CREATE TABLE ITEM_MASTER (
    ITEM_ID INT Identity(1, 1) PRIMARY KEY,
    ITEM_NUMBER VARCHAR(50) NOT NULL UNIQUE,
    ITEM_DESCRIPTION VARCHAR(1000) NOT NULL,
    ITEM_TYPE VARCHAR(20),
    MANUFACTURER_CODE VARCHAR(20),
    ITEM_CATEGORY VARCHAR(20),
    CPU VARCHAR(100),
    MEMORY VARCHAR(100),
    DISKS VARCHAR(100),
    UOM VARCHAR(20),
    ENABLED_FLAG VARCHAR(1) NOT NULL,
    CREATION_DATE DATETIME ,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),
    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 NUMERIC,
    ATTRIBUTE_NUM2 NUMERIC,
    ATTRIBUTE_NUM3 NUMERIC,
    ATTRIBUTE_DATE1 DATETIME,
    ATTRIBUTE_DATE2 DATETIME
);


-- Create Inventory_Onhand1 table
CREATE TABLE Inventory_Onhand (
    INVENTORY_ID INT IDENTITY(1,1) PRIMARY KEY,
    ITEM_ID INT FOREIGN KEY REFERENCES ITEM_MASTER(ITEM_ID),
    INSTALL_LOCATION VARCHAR(200),
    PROJECT_CODE VARCHAR(20),
    QUANTITY INT,
    IP_ADDRESS VARCHAR(200),
    SUBNET_MASK VARCHAR(200),
    GATEWAY VARCHAR(200),
    COMMENTS VARCHAR(1000),
    LAST_PO_NUM INT,
    LAST_PO_PRICE DECIMAL(18, 2),
    RENEWAL_DATE DATE,
    NOTES VARCHAR(MAX),
    CREATION_DATE DATETIME,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),

    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 NUMERIC,
    ATTRIBUTE_NUM2 NUMERIC,
    ATTRIBUTE_NUM3 NUMERIC,
    ATTRIBUTE_DATE1 DATETIME,
    ATTRIBUTE_DATE2 DATETIME
);




-- Create PO_Header table
CREATE TABLE PO_HEADER (
    PO_HEADER_ID INT IDENTITY(1,1) PRIMARY KEY,
    PO_NUMBER VARCHAR(50) NOT NULL UNIQUE,
    PO_TYPE VARCHAR(20),
    PO_DESCRIPTION VARCHAR(1000),
    VENDOR_NAME VARCHAR(100) NOT NULL,
    VENDOR_LOCATION VARCHAR(100),
    QUOTE_REQUESTED VARCHAR(1),
    QUOTE_NUMBER VARCHAR(20),
    PO_STATUS VARCHAR(30) CHECK (PO_STATUS IN ('Entered', 'Approved', 'Received', 'Invoiced', 'Closed', 'Cancelled')) NOT NULL,
    PO_DATE DATE,
    PO_APPROVED_DATE DATE,
    PO_APPROVED_BY VARCHAR(20),
    PO_REQUESTED VARCHAR(1),
    PO_REQUESTED_BY VARCHAR(20),
    INVOICE_NUMBER VARCHAR(50),
    INVOICE_LINE_NUMBER INT,
    INVOICE_AMOUNT INT,
    INVOICE_PAID VARCHAR(1),
    SUPPORT_START_DATE DATE,
    SUPPORT_END_DATE DATE,
    CREATION_DATE DATETIME,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),

    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 INT,
    ATTRIBUTE_NUM2 INT,
    ATTRIBUTE_NUM3 INT,
    ATTRIBUTE_DATE1 DATETIME,
    ATTRIBUTE_DATE2 DATETIME
);

-- Create PO_Lines table
CREATE TABLE PO_LINES (
    PO_LINE_ID INT IDENTITY(1,1) PRIMARY KEY,
    PO_HEADER_ID INT,
    PO_LINE_NUMBER INT NOT NULL,
    ITEM_ID INT,
    PO_LINE_DESCRIPTION VARCHAR(1000),
    QUANTITY INT NOT NULL,
    UNIT_PRICE INT NOT NULL,
    LINE_TAX_AMOUNT INT,
    SUPPORT_START_DATE DATE,
    SUPPORT_END_DATE DATE,
    NEED_BY_DATE DATE,
    PO_LINE_STATUS VARCHAR(30) NOT NULL,
    SHIP_LOCATION VARCHAR(200),
    INVOICE_NUMBER VARCHAR(50),
    INVOICE_LINE_NUMBER INT,
    INVOICE_DATE DATE,
    INVOICE_PAID VARCHAR(1),
    INVOICE_AMOUNT INT,
    PO_LINE_COMMENTS VARCHAR(1000),
    CREATION_DATE DATETIME,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),

    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 INT,
    ATTRIBUTE_NUM2 INT,
    ATTRIBUTE_NUM3 INT,
    ATTRIBUTE_DATE1 DATE,
    ATTRIBUTE_DATE2 DATE,
    FOREIGN KEY (PO_HEADER_ID) REFERENCES PO_HEADER(PO_HEADER_ID),
    FOREIGN KEY (ITEM_ID) REFERENCES ITEM_MASTER(ITEM_ID)
);


CREATE TABLE Lookup_Type (
    LOOKUP_TYPE_ID INT IDENTITY(1,1) PRIMARY KEY,
    LOOKUP_TYPE VARCHAR(150) NOT NULL UNIQUE,
    TYPE_DESCRIPTION VARCHAR(1000),
    ENABLED_FLAG VARCHAR(1) NOT NULL,
    CREATION_DATE DATETIME,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),

    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 INT,
    ATTRIBUTE_NUM2 INT,
    ATTRIBUTE_NUM3 INT,
    ATTRIBUTE_DATE1 DATE,
    ATTRIBUTE_DATE2 DATE
);

-- Create Lookup_Values table 
CREATE TABLE Lookup_Values (
    LOOKUP_VALUE_ID INT IDENTITY(1,1) PRIMARY KEY,
    LOOKUP_TYPE_ID INT,
    LOOKUP_CODE VARCHAR(20) NOT NULL,
    LOOKUP_VALUE VARCHAR(200) NOT NULL,
    VALUE_DESCRIPTION VARCHAR(1000),
    ENABLED_FLAG VARCHAR(1) NOT NULL,
    CREATION_DATE DATETIME,
    CREATED_BY_USER VARCHAR(20),
    LAST_UPDATE_DATE DATETIME,
    LAST_UPDATED_BY_USER VARCHAR(20),

    ATTRIBUTE_CHAR1 VARCHAR(150),
    ATTRIBUTE_CHAR2 VARCHAR(150),
    ATTRIBUTE_CHAR3 VARCHAR(150),
    ATTRIBUTE_CHAR4 VARCHAR(150),
    ATTRIBUTE_CHAR5 VARCHAR(150),
    ATTRIBUTE_NUM1 INT,
    ATTRIBUTE_NUM2 INT,
    ATTRIBUTE_NUM3 INT,
    ATTRIBUTE_DATE1 DATE,
    ATTRIBUTE_DATE2 DATE,
    FOREIGN KEY (LOOKUP_TYPE_ID) REFERENCES Lookup_Type(LOOKUP_TYPE_ID)
);



-- Insert records into ITEM_MASTER table
INSERT INTO ITEM_MASTER (ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE, ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM, ENABLED_FLAG, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
VALUES 
('ITEM001', 'Laptop', 'Electronics', 'MAN001', 'Electronics', 'Intel Core i5', '8GB', '256GB SSD', 'Each', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('ITEM002', 'Desktop Computer', 'Electronics', 'MAN002', 'Electronics', 'Intel Core i7', '16GB', '1TB HDD', 'Each', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('ITEM003', 'Smartphone', 'Electronics', 'MAN003', 'Electronics', 'Snapdragon 888', '12GB', '256GB', 'Each', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('ITEM004', 'Printer', 'Electronics', 'MAN004', 'Electronics', 'N/A', 'N/A', 'N/A', 'Each', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('ITEM005', 'Tablet', 'Electronics', 'MAN005', 'Electronics', 'Apple A15 Bionic', '8GB', '128GB', 'Each', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin');

-- Insert records into Inventory_Onhand table
INSERT INTO Inventory_Onhand (ITEM_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
VALUES 
(1, 'Office 101', 'PROJ001', 10, '192.168.1.101', '255.255.255.0', '192.168.1.1', 'Office use', 1001, 1200.00, '2024-03-22', 'None', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'Office 102', 'PROJ002', 5, '192.168.1.102', '255.255.255.0', '192.168.1.1', 'Office use', 1002, 1500.00, '2024-03-22', 'None', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(3, 'Office 103', 'PROJ003', 20, '192.168.1.103', '255.255.255.0', '192.168.1.1', 'Office use', 1003, 800.00, '2024-03-22', 'None', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(4, 'Warehouse 1', 'PROJ004', 3, '192.168.2.101', '255.255.255.0', '192.168.2.1', 'Warehouse use', 1004, 300.00, '2024-03-22', 'None', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(5, 'Warehouse 2', 'PROJ005', 7, '192.168.2.102', '255.255.255.0', '192.168.2.1', 'Warehouse use', 1005, 500.00, '2024-03-22', 'None', GETDATE(), 'Admin', GETDATE(), 'Admin');


-- Insert records into PO_Header table
INSERT INTO PO_HEADER (PO_NUMBER, PO_TYPE, PO_DESCRIPTION, VENDOR_NAME, VENDOR_LOCATION, QUOTE_REQUESTED, QUOTE_NUMBER, PO_STATUS, PO_DATE, PO_APPROVED_DATE, PO_APPROVED_BY, PO_REQUESTED, PO_REQUESTED_BY, INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_AMOUNT, INVOICE_PAID, SUPPORT_START_DATE, SUPPORT_END_DATE, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
VALUES 
('PO001', 'Standard', 'Purchase of laptops', 'Vendor A', 'Location A', 'Y', 'QUOTE001', 'Entered', '2024-03-22', NULL, NULL, 'Y', 'User1', NULL, NULL, NULL, NULL, NULL, NULL, GETDATE(), 'Admin', GETDATE(), 'Admin'),
('PO002', 'Standard', 'Purchase of desktop computers', 'Vendor B', 'Location B', 'Y', 'QUOTE002', 'Approved', '2024-03-22', '2024-03-23', 'Approver1', 'Y', 'User2', NULL, NULL, NULL, NULL, '2024-03-25', '2024-03-30', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('PO003', 'Standard', 'Purchase of smartphones', 'Vendor C', 'Location C', 'N', NULL, 'Received', '2024-03-22', '2024-03-24', 'Approver2', 'N', NULL, 'INV001', 1, 1200.00, 'Y', '2024-03-25', '2024-03-30', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('PO004', 'Standard', 'Purchase of printers', 'Vendor D', 'Location D', 'Y', 'QUOTE003', 'Invoiced', '2024-03-22', '2024-03-25', 'Approver3', 'N', NULL, 'INV002', 2, 1500.00, 'Y', '2024-03-25', '2024-03-30', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('PO005', 'Standard', 'Purchase of tablets', 'Vendor E', 'Location E', 'Y', 'QUOTE004', 'Closed', '2024-03-22', '2024-03-26', 'Approver4', 'N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETDATE(), 'Admin', GETDATE(), 'Admin');

-- Inserting at least 5 records into PO_LINES table
INSERT INTO PO_LINES (
    PO_HEADER_ID,
    PO_LINE_NUMBER,
    ITEM_ID,
    PO_LINE_DESCRIPTION,
    QUANTITY,
    UNIT_PRICE,
    LINE_TAX_AMOUNT,
    SUPPORT_START_DATE,
    SUPPORT_END_DATE,
    NEED_BY_DATE,
    PO_LINE_STATUS,
    SHIP_LOCATION,
    INVOICE_NUMBER,
    INVOICE_LINE_NUMBER,
    INVOICE_DATE,
    INVOICE_PAID,
    INVOICE_AMOUNT,
    PO_LINE_COMMENTS,
    CREATION_DATE,
    CREATED_BY_USER,
    LAST_UPDATE_DATE,
    LAST_UPDATED_BY_USER
)
VALUES
    (1, 1, 1, 'Sample Description 1', 10, 100, 10, NULL, NULL, NULL, 'Open', 'Location 1', 'INV001', 1, '2024-03-22', 'Y', 1000, 'Sample Comments 1', GETDATE(), 'Admin', GETDATE(), 'Admin'),
    (1, 2, 2, 'Sample Description 2', 5, 200, 20, NULL, NULL, NULL, 'Open', 'Location 2', 'INV002', 2, '2024-03-23', 'Y', 1500, 'Sample Comments 2', GETDATE(), 'Admin', GETDATE(), 'Admin'),
    (2, 1, 3, 'Sample Description 3', 8, 150, 15, NULL, NULL, NULL, 'Open', 'Location 3', 'INV003', 3, '2024-03-24', 'Y', 1200, 'Sample Comments 3', GETDATE(), 'Admin', GETDATE(), 'Admin'),
    (3, 1, 4, 'Sample Description 4', 12, 120, 12, NULL, NULL, NULL, 'Open', 'Location 4', 'INV004', 4, '2024-03-25', 'Y', 1440, 'Sample Comments 4', GETDATE(), 'Admin', GETDATE(), 'Admin'),
    (3, 2, 5, 'Sample Description 5', 15, 180, 18, NULL, NULL, NULL, 'Open', 'Location 5', 'INV005', 5, '2024-03-26', 'Y', 2700, 'Sample Comments 5', GETDATE(), 'Admin', GETDATE(), 'Admin');



-- Insert records into Lookup_Type table
INSERT INTO Lookup_Type (LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
VALUES 
('ITEM_CATEGORY', 'Item Categories', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
('PO_STATUS', 'Purchase Order Status', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin');


-- Insert records into Lookup_Values table
INSERT INTO Lookup_Values (LOOKUP_TYPE_ID, LOOKUP_CODE, LOOKUP_VALUE, VALUE_DESCRIPTION, ENABLED_FLAG, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
VALUES 
(1, 'ELEC', 'Electronics', 'Electronic Items', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(1, 'STAT', 'Stationery', 'Stationery Items', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(1, 'FURN', 'Furniture', 'Furniture Items', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'ENTERED', 'Entered', 'PO Entered', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'APPROVED', 'Approved', 'PO Approved', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'RECEIVED', 'Received', 'PO Received', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'INVOICED', 'Invoiced', 'PO Invoiced', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'CLOSED', 'Closed', 'PO Closed', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin'),
(2, 'CANCELLED', 'Cancelled', 'PO Cancelled', 'Y', GETDATE(), 'Admin', GETDATE(), 'Admin');



create table admin(username varchar(255) unique, password varchar(255));

insert into admin values('amaan_shaik','ksrm@2024');

insert into admin values('Hussain','ksrm@2024');

select * from admin;

select @@SERVERNAME;

use InfraDB;

create table users;

DELETE FROM ITEM_MASTER where ITEM_ID > 11;

select *from Inventory_Onhand;
select * from ITEM_MASTER;

CREATE TABLE Users (
    username NVARCHAR(100),
    email NVARCHAR(100),
    password NVARCHAR(100),
    phonenumber NVARCHAR(20)
);

-- Inserting two records at once
INSERT INTO Users (username, email, password, phonenumber) 
VALUES 
    ('Hussain', 'smdh4321@gmail.com', 'ksrm@2024', '9701381026'),
    ('Amaan', 'smdamaan20@gmail.com', 'ksrm@2024', '7288838904');

select * from Users;

drop table Users;


select *from LOOKUP_VALUES;

select *from Lookup_Type;

select *from PO_HEADER;

select *from PO_LINES;
select * from ITEM_MASTER;

use InfraDB;

ALTER TABLE Inventory_Onhand
ALTER COLUMN LAST_PO_PRICE INT;

select * from users1;


CREATE TABLE users1 (
    name VARCHAR(100) not null,
    email VARCHAR(100) not null,
    phonenumber VARCHAR(20),
    username VARCHAR(50) not null ,
    password VARCHAR(100) not null
);
insert into users1 values('Amaan Shaik','smdamaan20@gmail.com','7288838904','amaan_shaik','amaan123');
insert into users1 values('Hussain Sunkara','smdh@gmail.com','7288838904','hussain','amaan123');

select * from ITEM_MASTER ORDER BY ITEM_NUMBER;

delete from ITEM_MASTER where ITEM_NUMBER='1';

delete from users1 where name='zakiya';

select * from users1;
