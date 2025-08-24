SELECT
r.name,
(MAX(DATE_PART('year', age(CURRENT_DATE, birthday))) - MIN(DATE_PART('year', age(CURRENT_DATE, birthday))))::INTEGER AS age_diff
FROM rooms r
JOIN students s ON r.id = s.room
WHERE s.is_instant = TRUE
GROUP BY r.name
HAVING MAX(DATE_PART('year', age(CURRENT_DATE, birthday))) - MIN(DATE_PART('year', age(CURRENT_DATE, birthday))) IS NOT NULL
ORDER BY age_diff DESC
LIMIT 5;