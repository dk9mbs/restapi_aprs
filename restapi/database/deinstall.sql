DELETE FROM api_group_permission WHERE solution_id=10002;
DELETE FROM api_user_group WHERE solution_id=10002;
DELETE FROM api_table WHERE solution_id=10002;
DELETE FROM api_session WHERE user_id IN(910002);
DELETE FROM api_user WHERE solution_id=10002;
DELETE FROM api_group WHERE solution_id=10002;
DELETE FROM api_event_handler WHERE solution_id=10002;
DELETE FROM api_solution WHERE id=10002;

DROP TABLE IF EXISTS aprs_object;
DROP TABLE IF EXISTS aprs_login;




