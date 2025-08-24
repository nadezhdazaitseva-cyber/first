CREATE INDEX IF NOT EXISTS indx_students_for_join ON students(room);
CREATE INDEX IF NOT EXISTS indx_rooms_for_join ON rooms(id)