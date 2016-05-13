--An example to get data for the last 30 days


declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)


SELECT     group3_.group_name                       AS col_0_0_, 
           printerusa0_.paper_size                  AS col_1_0_, 
           printerusa0_.duplex                      AS col_2_0_, 
           Sum(printerusa0_.total_pages)            AS col_3_0_, 
           Sum(printerusa0_.usage_cost)             AS col_4_0_, 
           Count(printerusa0_.printer_usage_log_id) AS col_5_0_, 
           Sum(printerusa0_.total_color_pages)      AS col_6_0_ 
FROM       tbl_printer_usage_log printerusa0_ 
INNER JOIN tbl_user user1_ 
ON         printerusa0_.used_by_user_id=user1_.user_id 
INNER JOIN tbl_user_group grouplinks2_ 
ON         user1_.user_id=grouplinks2_.user_id 
INNER JOIN tbl_group group3_ 
ON         grouplinks2_.group_id=group3_.group_id 
WHERE      printerusa0_.usage_date>=@start_date
AND        printerusa0_.usage_allowed='Y' 
AND        printerusa0_.refunded='N'
AND        printerusa0_.printed='Ý'
GROUP BY   group3_.group_name , 
           printerusa0_.paper_size , 
           printerusa0_.duplex 
ORDER BY   Lower(group3_.group_name), 
           printerusa0_.paper_size, 
           printerusa0_.duplex