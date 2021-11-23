create user if not exists root@'%' identified by 'ogn';
grant all privileges on *.* to root@'%' with GRANT option;
create user if not exists ogn@'%' identified by 'ogn';
grant all privileges on *.* to ogn@'%' with GRANT option;
create user if not exists nextcloud@'%' identified by 'ogn';
grant all privileges on *.* to nextcloud@'%' with GRANT option;

