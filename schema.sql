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
    habit_name TEXT,
    date DATE,
    track_number_value BOOLEAN,
    number_value INTEGER,
    boolean_value BOOLEAN,
    form_submitted BOOLEAN
);

CREATE TABLE Challenges (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    goal TEXT,
    goal_frequency TEXT,
    duration TEXT,
    start_date DATE,
    end_date DATE,
    creator_id INTEGER REFERENCES Users(id)
);

CREATE TABLE UsersChallenges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id),
    challenge_id INTEGER REFERENCES Challenges(id),
    joined BOOLEAN
);

CREATE TABLE UsersChallengeLogs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id),
    challenge_id INTEGER REFERENCES Challenges(id),
    date DATE,
    completed BOOLEAN
)