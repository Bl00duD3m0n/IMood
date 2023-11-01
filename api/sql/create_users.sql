CREATE TABLE Users (
    UserID INT AUTO_INCREMENT NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Status_emoji INT,
    Status_txt   VARCHAR(64),
    PasswordHash VARCHAR(512) NOT NULL,
    Salt VARCHAR(512) NOT NULL,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID),
    FOREIGN KEY(Status_emoji) REFERENCES Emoji_types(EmojiID)
);
