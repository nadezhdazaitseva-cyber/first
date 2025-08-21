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