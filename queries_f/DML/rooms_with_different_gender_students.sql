WITH dense_rank_sex AS 
(SELECT room, sex,
DENSE_RANK() OVER(PARTITION BY room ORDER BY sex) AS cnt
FROM students
WHERE is_instant = TRUE)
SELECT DISTINCT room 
FROM dense_rank_sex WHERE cnt = 2