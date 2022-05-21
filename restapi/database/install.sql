DELETE FROM api_event_handler WHERE solution_id=10002;
DELETE FROM api_table_view WHERE solution_id=10002;
DELETE FROM api_ui_app_nav_item WHERE solution_id=10002;
DELETE FROM api_ui_app WHERE solution_id=10002;


INSERT IGNORE INTO api_solution(id,name) VALUES (10002, 'aprs');
INSERT IGNORE INTO api_user (id,username,password,is_admin,disabled,solution_id) VALUES (910002,'aprs','password',0,0,10002);
INSERT IGNORE INTO api_group(id,groupname,solution_id) VALUES (910002,'aprs',10002);
INSERT IGNORE INTO api_user_group(user_id,group_id,solution_id) VALUES (910002,910002,10002);

INSERT IGNORE INTO api_table(id,name,alias,table_name,id_field_name,id_field_type,desc_field_name,enable_audit_log,solution_id)
    VALUES
    (910002,'APRS Object','aprs_object','aprs_object','id','int','object_name',-1,10002);

INSERT IGNORE INTO api_table(id,name,alias,table_name,id_field_name,id_field_type,desc_field_name,enable_audit_log,solution_id)
    VALUES
    (910003,'APRS Login','aprs_login','aprs_login','id','int','callsign',-1,10002);


INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (910002,910002,-1,-1,-1,-1,10002);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (910002,910003,-1,-1,-1,-1,10002);


INSERT IGNORE INTO api_event_handler (id,plugin_module_name,publisher,event,type,sorting,solution_id) 
    VALUES (910001,'aprs_send_objects','$timer_every_ten_minutes','execute','after',100,10002);

CREATE TABLE IF NOT EXISTS aprs_login(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    callsign varchar(50) NOT NULL,
    passcode int NOT NULL default '-1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS aprs_object(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    login_id int NOT NULL,
    source_address varchar(10) NOT NULL,
    object_name varchar(9) NOT NULL,
    type varchar(1) NOT NULL default '*' COMMENT '*: create, _:delete object',
    overlay varchar(1) NOT NULL default '/',
    lat_deg int NOT NULL DEFAULT '0',
    lat_min int NOT NULL DEFAULT '0',
    lat_sec decimal(10,4) NOT NULL DEFAULT '.0',
    long_deg int NOT NULL DEFAULT '0',
    long_min int NOT NULL DEFAULT '0',
    long_sec decimal(10,4) NOT NULL DEFAULT '.0',
    symbol_code varchar(1) NOT NULL DEFAULT 'r',
    comment varchar(36) NULL,
    FOREIGN KEY (login_id) REFERENCES aprs_login(id)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE aprs_object MODIFY COLUMN comment varchar(250);

INSERT IGNORE INTO aprs_login(id,callsign,passcode) VALUES (1,'DK9MBS',-1);

INSERT IGNORE INTO aprs_object (id,login_id,source_address,object_name,type,symbol_code,lat_deg,lat_min,lat_sec,long_deg,long_min,long_sec,comment) 
    VALUES (1,1,'DK9MBS','DK0AY','*','r',52,5,14.2008,10,22,8.2236,'144.650MHz');

INSERT IGNORE INTO aprs_object (id,login_id,source_address,object_name,type,symbol_code,lat_deg,lat_min,lat_sec,long_deg,long_min,long_sec,comment) 
    VALUES (2,1,'DK9MBS','OV-H21','*','-',52,5,13.7724,10,22,6.8808,'144.650MHz H21 - https://darc.de/h21');

INSERT IGNORE INTO aprs_object (id,login_id,source_address,object_name,type,symbol_code,lat_deg,lat_min,lat_sec,long_deg,long_min,long_sec,comment) 
    VALUES (3,1,'DK9MBS','DK9MBS','*','r',52,2,55.8492,10,22,21.972,'144.650MHz - https://dk9mbs.de');


INSERT IGNORE INTO api_ui_app (id, name,description,home_url,solution_id)
VALUES (
910000,'APRS','APRS (HAM)','/ui/v1.0/data/view/aprs_object/default?app_id=910000',10002);

INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id)
VALUES (910000,910000,'Objects','/ui/v1.0/data/view/aprs_object/default',1,10002);

INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id)
VALUES (910001,910000,'Logins','/ui/v1.0/data/view/aprs_login/default',1,10002);



INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml) VALUES (
910000,'LISTVIEW','default',910002,'id',10002,'<restapi type="select">
    <table name="aprs_object" alias="o"/>
    <filter type="or">
        <condition field="object_name" table_alias="o" value="$$query$$" operator=" like "/>
    </filter>
    <orderby>
        <field name="object_name" alias="o" sort="ASC"/>
    </orderby>
    <joins>
        <join type="inner" table="aprs_login" alias="l" condition="o.login_id=l.id"/>
    </joins>
    <select>
        <field name="id" table_alias="o" alias="id"/>
        <field name="callsign" table_alias="l" header="Login"/>
        <field name="source_address" table_alias="o" header="Sourceaddress"/>
        <field name="object_name" table_alias="o" header="Objectname"/>
        <field name="type" table_alias="o" header="Type"/>
        <field name="overlay" table_alias="o" header="Overlay"/>
        <field name="symbol_code" table_alias="o" header="Symbolcode"/>
        <field name="comment" table_alias="o" header="Comment"/>
    </select>
</restapi>');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml) VALUES (
910001,'LISTVIEW','default',910003,'id',10002,'<restapi type="select">
    <table name="aprs_login" alias="l"/>
    <filter type="or">
        <condition field="callsign" table_alias="l" value="$$query$$" operator=" like "/>
    </filter>
    <orderby>
        <field name="callsign" alias="l" sort="ASC"/>
    </orderby>
    <select>
        <field name="id" table_alias="l" alias="id" header="ID"/>
        <field name="callsign" table_alias="l" header="Callsign"/>
        <field name="passcode" table_alias="l" header="Passcode"/>
    </select>
</restapi>');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml) VALUES (
910002,'SELECTVIEW','default',910003,'id',10002,'<restapi type="select">
    <table name="aprs_login" alias="l"/>
    <orderby>
        <field name="callsign" alias="l" sort="ASC"/>
    </orderby>
    <select>
        <field name="id" table_alias="l" alias="id"/>
        <field name="callsign" table_alias="l" alias="name"/>
    </select>
</restapi>');
