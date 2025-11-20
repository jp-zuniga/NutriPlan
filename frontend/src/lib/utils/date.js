export function toReadableDate(
	iso,
	{
		locale = 'es-NI',
		timeZone = 'America/Managua',
		// tweak these as you like: 'short' | 'medium' | 'long' | 'full'
		dateStyle = 'medium',
		timeStyle = 'short',
		...rest
	} = {}
) {
	if (!iso) return '';

	// Normalize: keep only 3 fractional digits before timezone (e.g. .396099-06:00 -> .396-06:00)
	const normalized = iso.replace(/\.(\d{3})\d*(?=(?:Z|[+-]\d{2}:\d{2})$)/, '.$1');

	const d = new Date(normalized);
	if (Number.isNaN(d.getTime())) return iso; // fallback if something unexpected

	return new Intl.DateTimeFormat(locale, {
		dateStyle,
		timeStyle,
		timeZone,
		...rest
	}).format(d);
}
