
USE AuthS;

SELECT * FROM AuthS.Users;
UPDATE AuthS.Users SET userDisabledPwd = 0 WHERE id = 1;
DELETE FROM AuthS.Users WHERE id = 4 OR id = 5;
SELECT * FROM AuthS.LogLoginActivities;
DELETE FROM AuthS.LogLoginActivities WHERE id = 30;

INSERT INTO Users (username, email, pwd, lastPwd, pwdExpired, dtPwdChanged, tokenChgPwd, dtRegistration, userDisabledPwd, userDisabled, usabilityTime, usabilityDays, token, userID_OP)
VALUES 
('testUser3', 'testuser3@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, TRUE, NULL, NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL),
('testUser4', 'testuser4@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, '20241011', NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL);

('testUser2', 'testuser2@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, NULL, NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL),
('testUser1', 'testuser1@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, NULL, NULL, NOW(), FALSE, FALSE, NULL, NULL, NULL, NULL),
('harsh-admin', 'mkharris9910@gmail.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehO/Z8WnSgwoetNTB8r5beHr0p5EJvtwB6', NULL, FALSE, NULL, NULL, NOW(), FALSE, FALSE, NULL, NULL, NULL, NULL);

# password testUser1: funziona123
# password harsh-admin: funziona123!

