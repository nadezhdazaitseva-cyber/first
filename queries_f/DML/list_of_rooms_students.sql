SELECT r.name, count(s.id)
FROM rooms r
FULL JOIN students s ON r.id = s.room
GROUP BY r.name, r.id
ORDER BY r.id;