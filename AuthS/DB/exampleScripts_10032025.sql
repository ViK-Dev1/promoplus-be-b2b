
USE AuthS;

INSERT INTO Users (username, email, pwd, lastPwd, pwdExpired, dtPwdChanged, tokenChgPwd, dtRegistration, userDisabledPwd, userDisabled, usabilityTime, usabilityDays, token, userID_OP)
VALUES 
('testUser3', 'testuser3@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, TRUE, NULL, NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL),
('testUser4', 'testuser4@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, '20241011', NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL),
('testUser2', 'testuser2@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, NULL, NULL, NOW(), FALSE, TRUE, NULL, NULL, NULL, NULL),
('testUser1', 'testuser1@example.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE, NULL, NULL, NOW(), FALSE, FALSE, NULL, NULL, NULL, NULL),
('harsh', 'mkharris9910@gmail.com', '$2b$12$2D7Cdb8dd4Ng.YLMZVvehO/Z8WnSgwoetNTB8r5beHr0p5EJvtwB6', NULL, FALSE, NULL, NULL, NOW(), FALSE, FALSE, NULL, NULL, NULL, NULL);

# password per tutti i testUserNUM: funziona123
# password harsh-admin: funziona123!


INSERT INTO AuthS.Users (username, email, userType, pwd, lastPwd, pwdExpired, dtPwdChanged, tokenChgPwd, dtRegistration, userDisabledPwd, userDisabled, usabilityTime, usabilityDays, token, userID_OP)
VALUES 
;


('testUser5', 	'testuser1@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',TRUE,FALSE,NULL,NULL,NULL,0),
('harsh', 		'mkharris9910@gmail.com', 	1, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehO/Z8WnSgwoetNTB8r5beHr0p5EJvtwB6', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,NULL,NULL,NULL,0),
('testUser2', 	'testuser2@example.com', 	2, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,TRUE,NULL,NULL,NULL,0),
('testUser3', 	'testuser3@example.com', 	2, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, TRUE,NULL,NULL,'2024-11-10',FALSE,FALSE,NULL,NULL,NULL,0),
('testUser4', 	'testuser4@example.com', 	3, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,'2024-10-11',NULL,'2024-11-10',FALSE,FALSE,NULL,NULL,NULL,0),
('testUser5', 	'testuser5@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,NULL,"7",NULL,0),
('testUser6', 	'testuser6@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,"00:00-23:59","7",NULL,0),
('testUser7', 	'testuser7@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,"08:30-15:50;18:30-22:40","2;4;5;1",NULL,0),
('testUser8', 	'testuser8@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,"07:15-10:22;15:10-18:30","1;3;4;6",NULL,0),
('testUser9', 	'testuser9@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,"08:30-15:50;18:30-22:40","1;3;4;6",NULL,0),
('testUser10', 	'testuser10@example.com', 	0, '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOaJEZXWMQUSNgBrSkFBc4GakzICcY38a', NULL, FALSE,NULL,NULL,'2024-11-10',FALSE,FALSE,"08:30-10:05;13:30-22:40","1;3;4;6",NULL,0);

/* Query utili per preparare i dati per i test per il login */
SELECT * FROM AuthS.Users;	
UPDATE AuthS.Users SET userDisabledPwd = 0 WHERE id = 2; -- utile per fixare il primo record dopo ogni esecuzione dei test completa per riattivare l'utenza
-- per sicurezza pulire anche la logLoginActivities
UPDATE AuthS.Users SET userType = 3 WHERE id = 5;
DELETE FROM AuthS.Users WHERE id = 4 OR id = 5;
SELECT * FROM AuthS.LogLoginActivities;
DELETE FROM AuthS.LogLoginActivities WHERE id = 30;
/* Sezione per i test sugli orari di lavoro*/
-- sistemare gli orari in base alla data e ora in cui si eseguono i test
UPDATE AuthS.Users SET usabilityDays = "1;2;4;5" WHERE id = 9; -- giorno diverso da quello di oggi
UPDATE AuthS.Users SET usabilityTime = "07:15-10:22;20:15-21:30" WHERE id = 9; -- set dell'orario di lavoro
UPDATE AuthS.Users SET usabilityTime = "20:15-23:55;23:56-23:59" WHERE id = 10; -- set dell'orario di lavoro
UPDATE AuthS.Users SET usabilityTime = "09:05-12:15;22:30-23:50" WHERE id = 11; -- set dell'orario di lavoro

/* Test per controllare i dati  */
SELECT * FROM AuthS.Users;
SELECT * FROM AuthS.LogLoginActivities;	
