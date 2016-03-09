--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     accounttra0_.account_transaction_id AS account1_3_, 
           accounttra0_.transaction_date       AS transact2_3_, 
           accounttra0_.transacted_by          AS transacted3_3_, 
           accounttra0_.account_id             AS account4_3_, 
           accounttra0_.usage_log_type         AS usage5_3_, 
           accounttra0_.usage_log_id           AS usage6_3_, 
           accounttra0_.amount                 AS amount3_, 
           accounttra0_.balance                AS balance3_, 
           accounttra0_.txn_comment            AS txn9_3_, 
           accounttra0_.is_credit              AS is10_3_, 
           accounttra0_.transaction_type       AS transac11_3_, 
           accounttra0_.ext_device_id          AS ext12_3_ 
FROM       tbl_account_transaction accounttra0_ 
INNER JOIN tbl_account account1_ 
ON         accounttra0_.account_id=account1_.account_id 
WHERE      1=1 
AND        accounttra0_.transaction_date>=@start_date 
ORDER BY   accounttra0_.transaction_date DESC, 
           accounttra0_.account_transaction_id DESC