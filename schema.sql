CREATE TABLE gyms (
	id SERIAL PRIMARY KEY,
	name TEXT,
	address TEXT,
	fee INTEGER,
	description TEXT
);
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT
);
CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
	posted_at TIMESTAMP,
	user_id INTEGER REFERENCES users,
	gym_id INTEGER REFERENCES gyms,
	stars INTEGER,
	comment TEXT
);
