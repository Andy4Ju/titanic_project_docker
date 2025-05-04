CREATE TABLE IF NOT EXISTS passengers (
    PassengerId INT PRIMARY KEY,
    Survived TINYINT,
    Pclass INT,
    Name VARCHAR(100),
    Sex VARCHAR(10),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(50),
    Embarked VARCHAR(10)
);