--An example to get data for the last 30 days
declare @start_date datetime

declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(DAY,-30,@end_date)

SELECT     printerusa0_.printer_usage_log_id  AS col_0_0_, 
           printer1_.printer_id               AS col_1_0_, 
           user2_.user_name                   AS col_2_0_, 
           user2_.full_name                   AS col_3_0_, 
           account4_.account_name             AS col_4_0_, 
           account4_.sub_name                 AS col_5_0_, 
           account4_.pin                      AS col_6_0_, 
           account4_.sub_pin                  AS col_7_0_, 
           printerusa0_.printer_usage_log_id  AS printer1_14_0_, 
           printer1_.printer_id               AS printer1_10_1_, 
           printerusa0_.usage_date            AS usage2_14_0_, 
           printerusa0_.usage_day             AS usage3_14_0_, 
           printerusa0_.used_by_user_id       AS used4_14_0_, 
           printerusa0_.charged_to_account_id AS charged5_14_0_, 
           printerusa0_.usage_cost            AS usage6_14_0_, 
           printerusa0_.usage_allowed         AS usage7_14_0_, 
           printerusa0_.printer_id            AS printer8_14_0_, 
           printerusa0_.original_printer_id   AS original9_14_0_, 
           printerusa0_.job_id                AS job10_14_0_, 
           printerusa0_.document_name         AS document11_14_0_, 
           printerusa0_.client_machine        AS client12_14_0_, 
           printerusa0_.total_pages           AS total13_14_0_, 
           printerusa0_.total_sheets          AS total14_14_0_, 
           printerusa0_.copies                AS copies14_0_, 
           printerusa0_.paper_size            AS paper16_14_0_, 
           printerusa0_.paper_height_mm       AS paper17_14_0_, 
           printerusa0_.paper_width_mm        AS paper18_14_0_, 
           printerusa0_.printer_language      AS printer19_14_0_, 
           printerusa0_.document_size_kb      AS document20_14_0_, 
           printerusa0_.denied_reason         AS denied21_14_0_, 
           printerusa0_.duplex                AS duplex14_0_, 
           printerusa0_.gray_scale            AS gray23_14_0_, 
           printerusa0_.printed               AS printed14_0_, 
           printerusa0_.cancelled             AS cancelled14_0_, 
           printerusa0_.refunded              AS refunded14_0_, 
           printerusa0_.assoc_with_account_id AS assoc27_14_0_, 
           printerusa0_.total_color_pages     AS total28_14_0_, 
           printerusa0_.color_pages_estimated AS color29_14_0_, 
           printerusa0_.job_type              AS job30_14_0_, 
           printerusa0_.invoiced              AS invoiced14_0_, 
           printerusa0_.job_comment           AS job32_14_0_, 
           printerusa0_.protocol              AS protocol14_0_, 
           printerusa0_.original_usage_cost   AS original34_14_0_, 
           printerusa0_.refund_status         AS refund35_14_0_, 
           printerusa0_.refund_request_id     AS refund36_14_0_, 
           printerusa0_.replayed              AS replayed14_0_, 
           printerusa0_.signature             AS signature14_0_, 
           printerusa0_.hardware_check_status AS hardware39_14_0_, 
           printerusa0_.hardware_check_id     AS hardware40_14_0_, 
           printerusa0_.job_uid               AS job41_14_0_, 
           printerusa0_.archive_path          AS archive42_14_0_, 
           printerusa0_.duplex_pages          AS duplex43_14_0_, 
           printerusa0_.offline_usage         AS offline44_14_0_, 
           printerusa0_.print_queue_id        AS print45_14_0_, 
           printer1_.server_name              AS server2_10_1_, 
           printer1_.printer_name             AS printer3_10_1_, 
           printer1_.display_name             AS display4_10_1_, 
           printer1_.location                 AS location10_1_, 
           printer1_.notes                    AS notes10_1_, 
           printer1_.charge_type              AS charge7_10_1_, 
           printer1_.default_cost             AS default8_10_1_, 
           printer1_.deleted                  AS deleted10_1_, 
           printer1_.deleted_date             AS deleted10_10_1_, 
           printer1_.disabled                 AS disabled10_1_, 
           printer1_.disabled_until           AS disabled12_10_1_, 
           printer1_.total_jobs               AS total13_10_1_, 
           printer1_.total_pages              AS total14_10_1_, 
           printer1_.total_sheets             AS total15_10_1_, 
           printer1_.reset_by                 AS reset16_10_1_, 
           printer1_.reset_date               AS reset17_10_1_, 
           printer1_.created_date             AS created18_10_1_, 
           printer1_.created_by               AS created19_10_1_, 
           printer1_.modified_date            AS modified20_10_1_, 
           printer1_.modified_by              AS modified21_10_1_, 
           printer1_.color_detection_mode     AS color22_10_1_, 
           printer1_.device_type              AS device23_10_1_, 
           printer1_.ext_device_function      AS ext24_10_1_, 
           printer1_.physical_printer_id      AS physical25_10_1_, 
           printer1_.printer_type             AS printer26_10_1_, 
           printer1_.serial_number            AS serial27_10_1_, 
           printer1_.web_print_enabled        AS web28_10_1_, 
           printer1_.custom1                  AS custom29_10_1_, 
           printer1_.custom2                  AS custom30_10_1_, 
           printer1_.custom3                  AS custom31_10_1_, 
           printer1_.custom4                  AS custom32_10_1_, 
           printer1_.custom5                  AS custom33_10_1_, 
           printer1_.custom6                  AS custom34_10_1_, 
           printer1_.last_usage_date          AS last35_10_1_, 
           printer1_.gcp_printer_id           AS gcp36_10_1_, 
           printer1_.gcp_enabled              AS gcp37_10_1_, 
           printer1_.modified_ticks           AS modified38_10_1_, 
           printer1_.server_uuid              AS server39_10_1_, 
           printer1_.parent_id                AS parent40_10_1_ 
FROM       tbl_printer_usage_log printerusa0_ 
INNER JOIN tbl_printer printer1_ 
ON         printerusa0_.printer_id=printer1_.printer_id 
INNER JOIN tbl_user user2_ 
ON         printerusa0_.used_by_user_id=user2_.user_id 
INNER JOIN tbl_account account3_ 
ON         printerusa0_.charged_to_account_id=account3_.account_id 
INNER JOIN tbl_account account4_ 
ON         printerusa0_.assoc_with_account_id=account4_.account_id 
WHERE      account4_.account_type='SHARED' 
AND        printerusa0_.usage_date>=@start_date
AND        printerusa0_.usage_allowed='Y'
AND        printerusa0_.refunded='N' 
AND        printerusa0_.printed='Y' 
ORDER BY   account4_.account_name_lower, 
           account4_.sub_name_lower, 
           Lower(printer1_.display_name), 
           printerusa0_.usage_date ASC
