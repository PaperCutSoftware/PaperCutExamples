select 
	printer0_.printer_id ,
	printer0_.server_name ,
	printer0_.printer_name ,
	printer0_.display_name ,
	printer0_.location ,
	printer0_.notes ,
	printer0_.charge_type ,
	printer0_.default_cost ,
	printer0_.deleted ,
	printer0_.deleted_date ,
	printer0_.disabled ,
	printer0_.disabled_until ,
	printer0_.total_jobs ,
	printer0_.total_pages ,
	printer0_.total_sheets ,
	printer0_.reset_by ,
	printer0_.reset_date ,
	printer0_.created_date ,
	printer0_.created_by ,
	printer0_.modified_date ,
	printer0_.modified_by ,
	printer0_.color_detection_mode ,
	printer0_.device_type ,
	printer0_.ext_device_function ,
	printer0_.physical_printer_id ,
	printer0_.printer_type ,
	printer0_.serial_number ,
	printer0_.web_print_enabled ,
	printer0_.custom1 ,
	printer0_.custom2 ,
	printer0_.custom3 ,
	printer0_.custom4 ,
	printer0_.custom5 ,
	printer0_.custom6 ,
	printer0_.last_usage_date ,
	printer0_.gcp_printer_id ,
	printer0_.gcp_enabled ,
	printer0_.modified_ticks ,
	printer0_.server_uuid
from 
	tbl_printer printer0_ 
where 
	printer0_.deleted='N' 
	and printer0_.printer_name<>'!!template printer!!'
	and (printer0_.device_type='PRINTER'
	or printer0_.device_type='VIRTUAL_QUEUE') 
order by 
	coalesce(printer0_.server_name, '!') asc,
	printer0_.printer_name asc 