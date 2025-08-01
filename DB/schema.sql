
--  Database design 

#






-- Roles table
CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL
);

-- Users table
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    RoleID INT NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID) ON DELETE CASCADE
);

-- ToDoList table
CREATE TABLE ToDoList (
    TaskID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Task TEXT NOT NULL,
    IsCompleted BOOLEAN DEFAULT FALSE,
    DueDate DATE,
    Priority VARCHAR(10) CHECK (Priority IN ('Low', 'Medium', 'High')),
    Category VARCHAR(50),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Calendar table
CREATE TABLE Calendar (
    EventID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Description TEXT,
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Notes TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Settings table
CREATE TABLE Settings (
    SettingID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Theme VARCHAR(10) CHECK (Theme IN ('Light', 'Dark')),
    NotificationPref BOOLEAN DEFAULT TRUE,
    Language VARCHAR(50) DEFAULT 'English',
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Resources table
CREATE TABLE Resources (
    ResourceID SERIAL PRIMARY KEY,
    ResourceName VARCHAR(100) NOT NULL,
    URL TEXT NOT NULL,
    Description TEXT
);
