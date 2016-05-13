--An example to get data for the last 30 days
declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)


SELECT     Sum(printerusa0_.total_sheets)           AS col_0_0_, 
           Sum(printerusa0_.total_pages)            AS col_1_0_, 
           Sum(printerusa0_.usage_cost)             AS col_2_0_, 
           Count(printerusa0_.printer_usage_log_id) AS col_3_0_, 
           Sum(printerusa0_.total_color_pages)      AS col_4_0_ 
FROM       tbl_printer_usage_log printerusa0_ 
INNER JOIN tbl_printer printer1_ 
ON         printerusa0_.printer_id=printer1_.printer_id 
INNER JOIN tbl_user user2_ 
ON         printerusa0_.used_by_user_id=user2_.user_id 
INNER JOIN tbl_account account3_ 
ON         printerusa0_.charged_to_account_id=account3_.account_id 
INNER JOIN tbl_account account4_ 
ON         printerusa0_.assoc_with_account_id=account4_.account_id 
WHERE      printerusa0_.usage_date>=@start_date
AND        printerusa0_.printed='N'
AND        ( 
                      printerusa0_.denied_reason='RELEASE_STATION_TIMEOUT' 
           OR         printerusa0_.denied_reason='RELEASE_STATION_CANCELLED')