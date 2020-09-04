DROP TABLE IF EXISTS Bets;
DROP TABLE IF EXISTS Odds;
DROP TABLE IF EXISTS Predictions;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Teams;
DROP TABLE IF EXISTS Leagues;

CREATE TABLE Leagues (
    league_id INT GENERATED ALWAYS AS IDENTITY,
    league_name VARCHAR(50)   NOT NULL,
    country    VARCHAR(50),
    league_size INT,
    PRIMARY KEY(league_id)
);

CREATE TABLE Teams (
    team_id INT GENERATED ALWAYS AS IDENTITY,
    team_name VARCHAR(50) NOT NULL,
    abbreviation CHAR(3) NOT NULL,
    league_id INT NOT NULL,
    PRIMARY KEY(team_id),
    CONSTRAINT fk_league
        FOREIGN KEY(league_id)
            REFERENCES leagues(league_id)
);

CREATE TABLE Matches (
    match_id INT GENERATED ALWAYS AS IDENTITY,
    season INT NOT NULL,
    match_date DATE NOT NULL,
    start_time TIME NOT NULL,
    league_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score INT,
    away_score INT,
    PRIMARY KEY(match_id),
    CONSTRAINT fk_league_id
        FOREIGN KEY(league_id)
            REFERENCES leagues(league_id),
    CONSTRAINT fk_home_t
        FOREIGN KEY(home_team_id)
            REFERENCES teams(team_id),
    CONSTRAINT fk_away_t
        FOREIGN KEY(away_team_id)
            REFERENCES teams(team_id)
);

CREATE TABLE Predictions (
    pred_id INT GENERATED ALWAYS AS IDENTITY,
    match_id INT NOT NULL,
    home_prob DECIMAL(4,4) NOT NULL,
    away_prob DECIMAL(4,4) NOT NULL,
    tie_prob DECIMAL(4,4) NOT NULL,
    h_score_pred DECIMAL(3,2),
    a_score_pred DECIMAL(3,2),
    PRIMARY KEY(pred_id),
    CONSTRAINT fk_match_id
        FOREIGN KEY(match_id)
            REFERENCES matches(match_id)
);

CREATE TABLE Odds (
    odds_id INT GENERATED ALWAYS AS IDENTITY,
    match_id INT NOT NULL,
    h_team_odds INT NOT NULL,
    a_team_odds INT NOT NULL,
    tie_odds INT NOT NULL,
    source VARCHAR(50) NOT NULL,
    pull_date TIMESTAMP NOT NULL,
    PRIMARY KEY(odds_id),
    CONSTRAINT fk_match_id
        FOREIGN KEY(match_id)
            REFERENCES matches(match_id)
);

CREATE TABLE Bets (
    bet_id INT GENERATED ALWAYS AS IDENTITY,
    home_bet BOOLEAN NOT NULL,
    away_bet BOOLEAN NOT NULL,
    tie_bet BOOLEAN NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    odds_id INT NOT NULL,
    PRIMARY KEY(bet_id),
    CONSTRAINT fk_odds_id
        FOREIGN KEY(odds_id)
            REFERENCES odds(odds_id)
);