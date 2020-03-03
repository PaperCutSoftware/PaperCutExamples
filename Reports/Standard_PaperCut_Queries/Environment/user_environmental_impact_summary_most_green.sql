--An example to get data for the last 30 days

declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     user2_.user_name                         AS col_0_0_, 
           user2_.full_name                         AS col_1_0_, 
           Sum(printerusa0_.total_pages)            AS col_2_0_, 
           Avg(printerusa0_.total_pages)   			AS col_3_0_, 
           Sum(printerusa0_.usage_cost)             AS col_4_0_, 
           Avg(printerusa0_.usage_cost)             AS col_5_0_, 
           Count(printerusa0_.printer_usage_log_id) AS col_6_0_, 
           Sum(printerusa0_.total_sheets)           AS col_7_0_, 
           Sum(printerusa0_.total_color_pages)      AS col_8_0_, 
           user2_.department                        AS col_9_0_, 
           user2_.office                            AS col_10_0_, 
           user2_.card_number                       AS col_11_0_, 
           Sum(printerusa0_.duplex_pages)           AS col_12_0_ 
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
AND        printerusa0_.refunded='N' 
AND        printerusa0_.printed='Y' 
GROUP BY   user2_.user_name , 
           user2_.full_name , 
           user2_.department , 
           user2_.office , 
           user2_.card_number 
ORDER BY   Sum(printerusa0_.total_sheets) ASC