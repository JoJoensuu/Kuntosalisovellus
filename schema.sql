CREATE TABLE gyms (
	id SERIAL PRIMARY KEY,
	name TEXT,
	address TEXT,
	fee INTEGER,
	description TEXT,
	visible BOOLEAN
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
	user_id INTEGER REFERENCES users,
	gym_id INTEGER REFERENCES gyms,
	stars INTEGER,
	comment TEXT
);
INSERT INTO gyms (
	name,
	address,
	fee,
	description)
	VALUES (
	'Superstar Gym',
	'Superstar Street',
	80,
	'We will make you into a superstar!'
);

INSERT INTO gyms (
	name,
	address,
	fee,
	description)
	VALUES (
	'Average Gym',
	'Average Street',
	20,
	'For the Average Joe'
);
