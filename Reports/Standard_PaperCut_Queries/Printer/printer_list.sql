
SELECT   printer0_.printer_id           AS printer1_, 
         printer0_.server_name          AS server2_10_, 
         printer0_.printer_name         AS printer3_10_, 
         printer0_.display_name         AS display4_10_, 
         printer0_.location             AS location10_, 
         printer0_.notes                AS notes10_, 
         printer0_.charge_type          AS charge7_10_, 
         printer0_.default_cost         AS default8_10_, 
         printer0_.deleted              AS deleted10_, 
         printer0_.deleted_date         AS deleted10_10_, 
         printer0_.disabled             AS disabled10_, 
         printer0_.disabled_until       AS disabled12_10_, 
         printer0_.total_jobs           AS total13_10_, 
         printer0_.total_pages          AS total14_10_, 
         printer0_.total_sheets         AS total15_10_, 
         printer0_.reset_by             AS reset16_10_, 
         printer0_.reset_date           AS reset17_10_, 
         printer0_.created_date         AS created18_10_, 
         printer0_.created_by           AS created19_10_, 
         printer0_.modified_date        AS modified20_10_, 
         printer0_.modified_by          AS modified21_10_, 
         printer0_.color_detection_mode AS color22_10_, 
         printer0_.device_type          AS device23_10_, 
         printer0_.ext_device_function  AS ext24_10_, 
         printer0_.physical_printer_id  AS physical25_10_, 
         printer0_.printer_type         AS printer26_10_, 
         printer0_.serial_number        AS serial27_10_, 
         printer0_.web_print_enabled    AS web28_10_, 
         printer0_.custom1              AS custom29_10_, 
         printer0_.custom2              AS custom30_10_, 
         printer0_.custom3              AS custom31_10_, 
         printer0_.custom4              AS custom32_10_, 
         printer0_.custom5              AS custom33_10_, 
         printer0_.custom6              AS custom34_10_, 
         printer0_.last_usage_date      AS last35_10_, 
         printer0_.gcp_printer_id       AS gcp36_10_, 
         printer0_.gcp_enabled          AS gcp37_10_, 
         printer0_.modified_ticks       AS modified38_10_, 
         printer0_.server_uuid          AS server39_10_ 
FROM     tbl_printer printer0_ 
WHERE    printer0_.deleted='N' 
AND      printer0_.printer_name<>? 
AND      ( 
                  printer0_.device_type='printer' 
         OR       printer0_.device_type='virtual_queue') 
ORDER BY COALESCE(printer0_.server_name, '!') ASC, 
         printer0_.printer_name ASC

SELECT   p 
FROM     tbl_printer p 
WHERE    p.deleted = 'N' 
AND      p.printername <>'!!template printer!!' 
AND      ( 
                  p.devicetype = 'printer' 
         OR       p.devicetype = 'virtual_queue') 
ORDER BY COALESCE(p.servername, '!') ASC, 
         p.printername ASC
		 
		 
		 
		 