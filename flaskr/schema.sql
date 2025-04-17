--not being used

-- User Table
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(225) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- ConferenceSlot Table
CREATE TABLE ConferenceSlot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    time DATETIME NOT NULL,
    isbooked BOOLEAN NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES User(id)
);

-- Booking Table
CREATE TABLE Booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    time DATETIME NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES User(id),
    FOREIGN KEY (slot_id) REFERENCES ConferenceSlot(id)
);