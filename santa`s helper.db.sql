--
-- ���� ������������ � ������� SQLiteStudio v3.2.1 � �� ��� 4 15:20:09 2024
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: Characters
CREATE TABLE Characters (level INT, rod INT, picture TEXT, special INT, gift TEXT, phrase TEXT, dop_phrase TEXT, sadpicture TEXT);
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, 'girl2.png', 0, 'all', '� ����� �������� ����� ���������� ����������, ��� ��� ���������� �������� � ������� ���� ��� �����������.', NULL, 'sadgirl2.png');
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, 'girl4.png', 0, NULL, NULL, NULL, NULL);
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, 'sadgirl1.png', 0, NULL, '� �������� ��� ����� ���. ��� ����� �������� �������� �� �����.', NULL, NULL);
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, 'woman1.png', 0, NULL, '� �� ������ �������, � ������� ���� ������� �����.', '����, �������, �����, ������, ������� ������ ���� � ��� �������.', 'sadwoman1.png');
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, NULL, 0, NULL, NULL, NULL, NULL);
INSERT INTO Characters (level, rod, picture, special, gift, phrase, dop_phrase, sadpicture) VALUES (1, NULL, NULL, 0, NULL, NULL, NULL, NULL);

-- �������: player
CREATE TABLE player (name TEXT PRIMARY KEY UNIQUE, password INT, level INT);
INSERT INTO player (name, password, level) VALUES ('hjhjhj', 1234, 1);
INSERT INTO player (name, password, level) VALUES ('fjfk', 1508, 1);
INSERT INTO player (name, password, level) VALUES ('jjjjjj', 1652, 1);
INSERT INTO player (name, password, level) VALUES ('ghghgh', 1563, 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
