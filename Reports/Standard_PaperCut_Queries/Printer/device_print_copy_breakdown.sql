--An example to get data for the last 30 days


declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     printer1_.display_name              AS col_0_0_, 
           printerusa0_.job_type               AS col_1_0_, 
           Sum(printerusa0_.total_pages)       AS col_2_0_, 
           Sum(printerusa0_.usage_cost)        AS col_3_0_, 
           Sum(printerusa0_.total_color_pages) AS col_4_0_, 
           printer1_.server_name               AS col_5_0_, 
           printer1_.printer_name              AS col_6_0_, 
           printer1_.physical_printer_id       AS col_7_0_, 
           printer1_.printer_type              AS col_8_0_, 
           printer1_.location                  AS col_9_0_, 
           Sum(printerusa0_.duplex_pages)      AS col_10_0_ 
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
AND        printer1_.device_type<>'PRINTER' 
AND        printer1_.device_type<>'VIRTUAL_QUEUE' 
AND        ( 
                      printerusa0_.job_type='PRINT' 
           AND        printerusa0_.printed='ANY' 
           OR         printerusa0_.job_type<>'PRINT') 
GROUP BY   printer1_.display_name , 
           printer1_.server_name , 
           printer1_.printer_name , 
           printer1_.physical_printer_id , 
           printer1_.printer_type , 
           printer1_.location , 
           printerusa0_.job_type 
ORDER BY   Lower(printer1_.display_name)
