SELECT name, dob
FROM drivers
WHERE nationality = "Indian" AND dob <= "1990-01-01"
ORDER BY dob