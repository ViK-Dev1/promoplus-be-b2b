CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    pwd CHAR(60) NOT NULL,
    lastPwd CHAR(60) NULL,
    pwdExpired BOOLEAN DEFAULT FALSE,
    dtPwdChanged DATETIME NULL,
    tokenChgPwd VARCHAR(255) NULL,
    dtRegistration DATETIME NOT NULL,
    userDisabledPwd BOOLEAN DEFAULT FALSE,
    userDisabled BOOLEAN DEFAULT FALSE,
	usabilityTime VARCHAR(200) NULL,
	usabilityDays VARCHAR(200) NULL,
    token VARCHAR(255) NULL,
	userID_OP INTEGER NULL
);

-- define indexes for username and password
CREATE INDEX idx_users_usrnm ON Users(username);
CREATE INDEX idx_users_email ON Users(email);