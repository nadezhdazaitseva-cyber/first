SELECT
r.name,
ROUND(AVG(DATE_PART('year', age(CURRENT_DATE, birthday)))) AS avg_age
FROM rooms r
JOIN students s ON r.id = s.room
WHERE s.is_instant = TRUE
GROUP BY r.name
ORDER BY avg_age
LIMIT 5;