-- Write a safe room-1 reservation; use the quoted marker 'REQUEST_KEY'.
-- Return request_key,room_id or no rows when unavailable.
SELECT id,available FROM inventory;
