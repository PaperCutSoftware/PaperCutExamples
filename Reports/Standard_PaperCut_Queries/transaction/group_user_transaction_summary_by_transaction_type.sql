--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     group5_.group_name                         AS col_0_0_, 
           user3_.user_name                           AS col_1_0_, 
           user3_.full_name                           AS col_2_0_, 
           accounttra0_.transaction_type              AS col_3_0_, 
           accounttra0_.is_credit                     AS col_4_0_, 
           Sum(accounttra0_.amount)                   AS col_5_0_, 
           Count(accounttra0_.account_transaction_id) AS col_6_0_ 
FROM       tbl_account_transaction accounttra0_ 
INNER JOIN tbl_account account1_ 
ON         accounttra0_.account_id=account1_.account_id 
INNER JOIN tbl_user_account userlinks2_ 
ON         account1_.account_id=userlinks2_.account_id 
INNER JOIN tbl_user user3_ 
ON         userlinks2_.user_id=user3_.user_id 
INNER JOIN tbl_user_group grouplinks4_ 
ON         user3_.user_id=grouplinks4_.user_id 
INNER JOIN tbl_group group5_ 
ON         grouplinks4_.group_id=group5_.group_id 
WHERE      1=1 
AND        accounttra0_.transaction_date>=@start_date
AND        ( 
                      account1_.account_type LIKE 'USER%') 
AND        ( 
                      account1_.account_type LIKE 'USER%') 
GROUP BY   group5_.group_name , 
           user3_.user_name , 
           user3_.full_name , 
           accounttra0_.transaction_type , 
           accounttra0_.is_credit 
ORDER BY   Lower(group5_.group_name), 
           user3_.user_name, 
           accounttra0_.transaction_type, 
           accounttra0_.is_credit