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