USE AuthS;

SELECT * FROM Users;
SELECT * FROM AuthS.LogLoginActivity;

SELECT a;

SELECT id, username, email, dtRegistration, userDisabled
FROM AuthS.Users AS a
WHERE a.pwd = '$2b$12$2D7Cdb8dd4Ng.YLMZVvehOIFg48Eh2r7J/B.sudfguFE/W82mBfH.' AND
  (a.username = 'bobsmith' 
   OR 
   a.email = 'bob.smith@company.com')
LIMIT 1

SELECT logslogin.id, logslogin.loginResult, logslogin.attemptNum, logslogin.dtLogin
FROM AuthS.Users AS usr
 INNER JOIN AuthS.LogLoginActivity AS logslogin ON logslogin.userId = usr.id
        AND usr.email = 'bob.smith@company.com'
WHERE logslogin.dtLogin >= '2024-10-13 22:10:00'
ORDER BY logslogin.dtLogin DESC
LIMIT 1

, dtLogin = '2024-10-13 23:30:00'
UPDATE AuthS.LogLoginActivity
SET attemptNum = 4, loginResult = 'WP'
WHERE id = 27

UPDATE AuthS.Users
SET userID_OP = 6
WHERE id = 4

SELECT *
FROM Users;

INSERT INTO Users (username, email, pwd, dtRegistration, dtChangedPwd, userID_OP)
VALUES ('admin-HV', 'vikram.harshit@protonmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lS', '2024-11-09 15:15:00', CURRENT_TIMESTAMP, 6);

SELECT A.*
FROM AuthS.Users AS A
limit 2