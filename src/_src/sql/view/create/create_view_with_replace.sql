 CREATE OR REPLACE VIEW experienced_employee
    (id, Name)
    AS SELECT id, name
         FROM all_employee
        WHERE working_years > 5;