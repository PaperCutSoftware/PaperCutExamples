--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT printer2_.display_name                     AS col_0_0_, 
       printer2_.location                         AS col_1_0_, 
       Sum(accounttra0_.amount)                   AS col_2_0_, 
       Count(accounttra0_.account_transaction_id) AS col_3_0_ 
FROM   tbl_account_transaction accounttra0_ 
       INNER JOIN tbl_printer printer1_ 
               ON accounttra0_.ext_device_id = printer1_.printer_id, 
       tbl_printer printer2_ 
WHERE  accounttra0_.ext_device_id = printer2_.printer_id 
       AND ( accounttra0_.ext_device_id IS NOT NULL ) 
       AND accounttra0_.transaction_date >=@start_date
GROUP  BY printer2_.display_name, 
          printer2_.location