export function getRandomInt(min, max) {
	min = Math.ceil(min); // Ensure min is an integer
	max = Math.floor(max); // Ensure max is an integer
	return Math.floor(Math.random() * (max - min + 1)) + min;
}
