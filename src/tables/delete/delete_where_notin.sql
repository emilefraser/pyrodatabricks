DELETE FROM events
   WHERE category NOT IN (SELECT category FROM events2 WHERE date > '2001-01-01')