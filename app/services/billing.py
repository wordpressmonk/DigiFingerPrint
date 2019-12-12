create table customer1.customer (acc_no integer primary key, cust_name varchar(20), avail_balance decimal);

create table customer2.micro_statement (acc_no integer, avail_balance decimal, foreign key(acc_no) references customer1.customer(acc_no) on delete cascade);

delimiter //
create trigger update_after after update on customer1.customer for each row begin if new.acc_no = 1001 THEN insert into customer2.micro_statement values(new.acc_no, new.avail_balance); END IF;
end;
//

delimiter //
create trigger update_after after update on customer1.customer for each row begin if new.acc_no = 1001 THEN insert into customer2.micro_statement values(new.acc_no, new.avail_balance); END IF;
end;
//

https://www.geeksforgeeks.org/different-types-of-mysql-triggers-with-examples/
    https: // stackoverflow.com / questions / 50462279 / creating - trigger - using - connector - python - mysql
    https: // stackoverflow.com / questions / 56965681 / using - mysql - connector - in -python - execute - a - mysql - trigger - that - calculates - and -inse
    https: // www.tutorialspoint.com / mysql - trigger - to - insert - row - into - another - table
"delimiter; "