--An example to get data for the last 30 days

declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     group4_.group_name                       AS col_0_0_, 
           printer1_.display_name                   AS col_1_0_, 
           Sum(printerusa0_.total_pages)            AS col_2_0_, 
           Avg(printerusa0_.total_pagess)    AS col_3_0_, 
           Sum(printerusa0_.usage_cost)             AS col_4_0_, 
           Avg(printerusa0_.usage_cost)             AS col_5_0_, 
           Count(printerusa0_.printer_usage_log_id) AS col_6_0_, 
           Sum(printerusa0_.total_color_pages)      AS col_7_0_, 
           printer1_.serial_number                  AS col_8_0_, 
           Sum(printerusa0_.duplex_pages)           AS col_9_0_ 
FROM       tbl_printer_usage_log printerusa0_ 
INNER JOIN tbl_printer printer1_ 
ON         printerusa0_.printer_id=printer1_.printer_id 
INNER JOIN tbl_user user2_ 
ON         printerusa0_.used_by_user_id=user2_.user_id 
INNER JOIN tbl_user_group grouplinks3_ 
ON         user2_.user_id=grouplinks3_.user_id 
INNER JOIN tbl_group group4_ 
ON         grouplinks3_.group_id=group4_.group_id 
WHERE      printerusa0_.usage_date>=@start_date 
AND        printerusa0_.usage_allowed='Y'
AND        printerusa0_.refunded='N'
AND        printerusa0_.printed='Y' 
GROUP BY   group4_.group_name , 
           printer1_.display_name , 
           printer1_.serial_number 
ORDER BY   Lower(group4_.group_name), 
           Lower(printer1_.display_name) 