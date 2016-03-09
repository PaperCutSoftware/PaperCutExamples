--An example to get data for the past 1 month

declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(MONTH,-1,@end_date)

SELECT     printer1_.display_name                   AS col_0_0_, 
           printerusa0_.paper_size                  AS col_1_0_, 
           printerusa0_.duplex                      AS col_2_0_, 
           Sum(printerusa0_.total_pages)            AS col_3_0_, 
           Sum(printerusa0_.usage_cost)             AS col_4_0_, 
           Count(printerusa0_.printer_usage_log_id) AS col_5_0_, 
           Sum(printerusa0_.total_color_pages)      AS col_6_0_, 
           printer1_.physical_printer_id            AS col_7_0_, 
           printer1_.printer_type                   AS col_8_0_ 
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
AND        printerusa0_.usage_allowed='Y' 
AND        printerusa0_.refunded='Y' 
AND        printerusa0_.printed='Y'
GROUP BY   printer1_.display_name , 
           printer1_.physical_printer_id , 
           printer1_.printer_type , 
           printerusa0_.paper_size , 
           printerusa0_.duplex 
ORDER BY   Lower(printer1_.display_name), 
           printerusa0_.paper_size, 
           printerusa0_.duplex 
		   
