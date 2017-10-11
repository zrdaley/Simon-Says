CREATE TABLE Accounts(
	user_id VARCHAR(200) PRIMARY KEY NOT NULL, 
	username VARCHAR(50) NOT NULL,
	password VARCHAR(100) NOT NULL,
	high_score INT,
);