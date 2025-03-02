CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    pwd CHAR(60) NOT NULL,
    lastPwd CHAR(60) NULL,
    dtRegistration DATETIME NOT NULL,
    dtChangedPwd DATETIME NULL,
    userDisabled BOOLEAN DEFAULT FALSE,
	usabilityTime,
	usabilityDays,
	userID_OP INTEGER NULL
);

-- define indexes for username and password
CREATE INDEX idx_users_usrnm ON Users(username);
CREATE INDEX idx_users_email ON Users(email);