-- # -- Insert test USERS
-- User 1: New registration
INSERT INTO Users (username, email, pwd, dtRegistration, dtChangedPwd)
VALUES ('johndoe', 'john.doe@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', CURRENT_TIMESTAMP, NULL);

-- User 2: Existing user changing password
INSERT INTO Users (username, email, pwd, dtRegistration, dtChangedPwd)
VALUES ('janedoe', 'jane.doe@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '2023-05-15 14:30:00', CURRENT_TIMESTAMP);

-- User 3: Disabled account
INSERT INTO Users (username, email, pwd, dtRegistration, dtChangedPwd, userDisabled)
VALUES ('bobsmith', 'bob.smith@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '2023-03-01 09:45:00', '2023-06-01 10:00:00', TRUE);

-- User 4: User who changed password recently
INSERT INTO Users (username, email, pwd, lastPwd, dtRegistration, dtChangedPwd)
VALUES ('alicebrown', 'alice.brown@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '2023-02-20 11:15:00', '2023-07-15 13:30:00');

-- User 5: User with recent password change and disabled account
INSERT INTO Users (username, email, pwd, lastPwd, dtRegistration, dtChangedPwd, userDisabled)
VALUES ('emilywhite', 'emily.white@school.edu', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '2023-04-10 08:00:00', '2023-08-25 16:45:00', TRUE);

-- # --  Check users: 
SELECT * FROM Users LIMIT 2;

-- # -- Insert di tanti login activities
-- Successful login for User 1 (johndoe)
INSERT INTO LogLoginActivity (userId, loginResult, dtLogin, attemptNum, token)
VALUES (1, 'OK', CURRENT_TIMESTAMP(), 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');

-- Failed login attempt for User 2 (janedoe)
INSERT INTO LogLoginActivity (userId, loginResult, dtLogin, attemptNum)
VALUES (2, 'WP', CURRENT_TIMESTAMP() - INTERVAL 30 MINUTE, 2);

-- Successful login with token for User 3 (bobsmith)
INSERT INTO LogLoginActivity (userId, loginResult, dtLogin, attemptNum, token)
VALUES (3, 'OK', CURRENT_TIMESTAMP() + INTERVAL 1 HOUR, 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');

-- Multiple failed login attempts for User 4 (alicebrown)
INSERT INTO LogLoginActivity (userId, loginResult, dtLogin, attemptNum)
VALUES 
(4, 'WP', CURRENT_TIMESTAMP() - INTERVAL 15 MINUTES, 1),
(4, 'WP', CURRENT_TIMESTAMP() - INTERVAL 10 MINUTES, 2),
(4, 'WP', CURRENT_TIMESTAMP() - INTERVAL 5 MINUTES, 3);

-- Successful login after failed attempts for User 5 (emilywhite)
INSERT INTO LogLoginActivity (userId, loginResult, dtLogin, attemptNum, token)
VALUES (5, 'OK', CURRENT_TIMESTAMP() + INTERVAL 2 HOURS, 4, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');