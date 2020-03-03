--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     accounttra0_.transaction_type              AS col_0_0_, 
           Sum(accounttra0_.amount)                   AS col_1_0_, 
           accounttra0_.is_credit                     AS col_2_0_, 
           Count(accounttra0_.account_transaction_id) AS col_3_0_ 
FROM       tbl_account_transaction accounttra0_ 
INNER JOIN tbl_account account1_ 
ON         accounttra0_.account_id=account1_.account_id 
WHERE      1=1 
AND        accounttra0_.transaction_date>=@start_date
GROUP BY   accounttra0_.transaction_type , 
           accounttra0_.is_credit 
ORDER BY   accounttra0_.transaction_type, 
           accounttra0_.is_credit