CREATE TABLE LogLoginActivities (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    userId INTEGER NOT NULL,
    loginResult ENUM("OK", "WP") NOT NULL,
    dtLogin DATETIME NOT NULL,
    attemptNum INT DEFAULT 0,
    token VARCHAR(255) NULL,
    FOREIGN KEY (userId) REFERENCES Users(id)
);

-- define indexes for username and password
CREATE INDEX idx_lla_userId ON LogLoginActivities(userId);

/*
    loginResult:
      .OK - user authenticated correctly
      .WP - wrong password
*/