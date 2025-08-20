# queries.py

create_rooms_table = """
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,  
    name VARCHAR(100) NOT NULL
);
"""

create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    version_id SERIAL,
    id INT NOT NULL,
    birthday DATE,
    name VARCHAR(100) NOT NULL,
    room INT, 
    sex CHAR(1),
    is_instant boolean NOT NULL DEFAULT TRUE,
    CONSTRAINT students_pkey PRIMARY KEY (version_id),
    CONSTRAINT students_fkey FOREIGN KEY (room)
        REFERENCES public.rooms (id)
        ON DELETE SET NULL  -- Sets room to NULL if room is deleted
        ON UPDATE CASCADE,
    CONSTRAINT valid_sex CHECK (sex IN ('M', 'F', NULL))
);
"""

create_func_and_trigger = """
-- PostgreSQL's IF NOT EXISTS is only available for tables, not functions or triggers,
-- so we create or replace them.
CREATE OR REPLACE FUNCTION public.handle_student_versioning()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $BODY$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.is_instant := TRUE;
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' AND (
        OLD.room IS DISTINCT FROM NEW.room OR 
        OLD.name <> NEW.name
    ) THEN
        UPDATE students 
        SET is_instant = FALSE 
        WHERE id = OLD.id AND is_instant = TRUE;

        INSERT INTO students (id, birthday, name, room, sex, is_instant)
        VALUES (NEW.id, NEW.birthday, NEW.name, NEW.room, NEW.sex, TRUE);

        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$BODY$;

CREATE OR REPLACE TRIGGER students_insert_trigger
BEFORE INSERT ON students
FOR EACH ROW
EXECUTE FUNCTION handle_student_versioning();

CREATE OR REPLACE TRIGGER students_update_trigger
BEFORE UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION handle_student_versioning();
"""

insert_rooms = """
INSERT INTO rooms (id, name)
VALUES (%s, %s)
ON CONFLICT (id) DO NOTHING;
"""

insert_students = """
INSERT INTO students (id, birthday, name, room, sex)
VALUES (%s, %s, %s, %s, %s);
"""


list_of_rooms_students = """
SELECT r.name, count(s.id)
FROM rooms r
FULL JOIN students s ON r.id = s.room
GROUP BY r.name, r.id
ORDER BY r.id;
"""

rooms_with_smallest_avg_age = """
SELECT
r.name,
ROUND(AVG(DATE_PART('year', age(CURRENT_DATE, birthday)))) AS avg_age
FROM rooms r
JOIN students s ON r.id = s.room
WHERE s.is_instant = TRUE
GROUP BY r.name
ORDER BY avg_age
LIMIT 5;
"""

rooms_with_biggest_age_difference = """
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
"""

rooms_with_different_gender_students = """
WITH dense_rank_sex AS 
(SELECT room, sex,
DENSE_RANK() OVER(PARTITION BY room ORDER BY sex) AS cnt
FROM students
WHERE is_instant = TRUE)
SELECT DISTINCT room 
FROM dense_rank_sex WHERE cnt = 2"""

create_indexes = """
CREATE INDEX IF NOT EXISTS indx_students_for_join ON students(room);
CREATE INDEX IF NOT EXISTS indx_rooms_for_join ON rooms(id)"""