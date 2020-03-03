--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     userfieldh0_.field_value                 AS col_0_0_, 
           Sum(printerusa1_.total_pages)            AS col_1_0_, 
           Avg(printerusa1_.total_pages)    		AS col_2_0_, 
           Sum(printerusa1_.usage_cost)             AS col_3_0_, 
           Avg(printerusa1_.usage_cost)             AS col_4_0_, 
           Count(printerusa1_.printer_usage_log_id) AS col_5_0_, 
           Sum(printerusa1_.total_sheets)           AS col_6_0_, 
           Sum(printerusa1_.total_color_pages)      AS col_7_0_, 
           Sum(printerusa1_.duplex_pages)           AS col_8_0_ 
FROM       tbl_user_field_history userfieldh0_, 
           tbl_printer_usage_log printerusa1_ 
INNER JOIN tbl_printer printer2_ 
ON         printerusa1_.printer_id=printer2_.printer_id 
INNER JOIN tbl_user user3_ 
ON         printerusa1_.used_by_user_id=user3_.user_id 
INNER JOIN tbl_account account4_ 
ON         printerusa1_.charged_to_account_id=account4_.account_id 
INNER JOIN tbl_account account5_ 
ON         printerusa1_.assoc_with_account_id=account5_.account_id 
WHERE      printerusa1_.usage_date>=start_date 
AND        printerusa1_.usage_allowed='Y'
AND        printerusa1_.refunded='N'
AND        printerusa1_.printed='Y'
AND        userfieldh0_.field_type='OFFICE' 
AND        userfieldh0_.user_id=printerusa1_.used_by_user_id 
AND        userfieldh0_.start_date<=printerusa1_.usage_date 
AND        userfieldh0_.end_date>printerusa1_.usage_date 
GROUP BY   userfieldh0_.field_value 
ORDER BY   userfieldh0_.field_value 