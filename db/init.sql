CREATE TABLE IF NOT EXISTS simulations (
                                           id SERIAL PRIMARY KEY,
                                           simulation_name VARCHAR(255) NOT NULL,
    sim_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dimension INTEGER NOT NULL
    );

CREATE TABLE IF NOT EXISTS submarines (
                                          id SERIAL PRIMARY KEY,
                                          simulation_id INTEGER NOT NULL,
                                          submarine_id INTEGER NOT NULL,
                                          step_number INTEGER NOT NULL,
                                          x FLOAT NOT NULL,
                                          y FLOAT NOT NULL,
                                          z FLOAT NOT NULL,
                                          prob FLOAT NOT NULL DEFAULT 0.0,
                                          FOREIGN KEY (simulation_id) REFERENCES simulations(id)
    );

CREATE TABLE IF NOT EXISTS sea_floors (
                                          simulation_id INTEGER NOT NULL,
                                          x INTEGER NOT NULL,
                                          y INTEGER NOT NULL,
                                          height FLOAT NOT NULL,
                                          PRIMARY KEY (simulation_id, x, y),
    FOREIGN KEY (simulation_id) REFERENCES simulations(id)
    );

CREATE TABLE IF NOT EXISTS wrecks (
                                      id SERIAL PRIMARY KEY,
                                      simulation_id INTEGER NOT NULL,
                                      x INTEGER NOT NULL,
                                      y INTEGER NOT NULL,
                                      height FLOAT NOT NULL,
                                      FOREIGN KEY (simulation_id) REFERENCES simulations(id)
    );