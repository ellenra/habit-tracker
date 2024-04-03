CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    email TEXT,
    password TEXT
);

CREATE TABLE Habits (
    id SERIAL PRIMARY KEY,
    habit_name TEXT NOT NULL,
    user_id INTEGER REFERENCES Users(id),
    track_number_value BOOLEAN
);

CREATE TABLE UsersHabits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id),
    habit_id INTEGER REFERENCES Habits(id),
    habit_name TEXT,
    date DATE,
    track_number_value BOOLEAN,
    number_value INTEGER,
    boolean_value BOOLEAN,
    form_submitted BOOLEAN
);
