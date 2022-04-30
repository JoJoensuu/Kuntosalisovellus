CREATE TABLE gyms (
	id SERIAL PRIMARY KEY,
	name TEXT,
	address TEXT,
	fee INTEGER,
	description TEXT,
	visible BOOLEAN,
	type_id INTEGER REFERENCES gym_types
);
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	admin BOOLEAN
);
CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
	posted_at TIMESTAMP,
	user_id INTEGER REFERENCES users ON DELETE CASCADE,
	gym_id INTEGER REFERENCES gyms,
	stars INTEGER,
	comment TEXT
);
CREATE TABLE gym_types (
	id SERIAL PRIMARY KEY,
	name TEXT,
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
INSERT INTO gyms (
	name,
	address,
	fee,
	description,
	visible
	type_id)
	VALUES (
	'Superstar Gym',
	'Superstar Street',
	80,
	'We will make you into a superstar!',
	True,
	1
);

INSERT INTO gyms (
	name,
	address,
	fee,
	description,
	visible
	type_id)
	VALUES (
	'Average Gym',
	'Average Street',
	20,
	'For the Average Joe',
	True,
	1
);
