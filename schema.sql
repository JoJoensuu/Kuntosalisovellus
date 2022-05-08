CREATE TABLE gym_types (
	type_id SERIAL PRIMARY KEY,
	name TEXT
);
CREATE TABLE gyms (
	gym_id SERIAL PRIMARY KEY,
	name TEXT,
	address TEXT,
	fee INTEGER,
	description TEXT,
	visible BOOLEAN,
	type_id INTEGER REFERENCES gym_types
);
CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	admin BOOLEAN
);
CREATE TABLE reviews (
	review_id SERIAL PRIMARY KEY,
	posted_at TIMESTAMP,
	user_id INTEGER REFERENCES users ON DELETE CASCADE,
	gym_id INTEGER REFERENCES gyms,
	stars INTEGER,
	comment TEXT
);
CREATE TABLE subscriptions (
	sub_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users ON DELETE CASCADE,
	gym_id INTEGER REFERENCES gyms ON DELETE CASCADE,
	joined_at TIMESTAMP
);
INSERT INTO gym_types (
	name)
	VALUES (
	'bodybuilding gym'
);
INSERT INTO gym_types (
	name)
	VALUES (
	'weightlifting gym'
);
INSERT INTO gym_types (
	name)
	VALUES (
	'powerlifting gym'
);
INSERT INTO gym_types (
	name)
	VALUES (
	'crossfit gym'
);
