DELETE FROM all_events
   WHERE session_time < (SELECT min(session_time) FROM good_events)