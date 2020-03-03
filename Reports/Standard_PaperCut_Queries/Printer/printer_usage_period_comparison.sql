--An example of the last two months

declare @start_date datetime
declare @end_date datetime

set @end_date = getdate()
set @start_date = DATEADD(MONTH,-2,@end_date)

select
	printer1_.display_name ,
	sum(printerusa0_.total_pages) as total_pages,
	avg(printerusa0_.total_pages) as average_pages ,
	sum(printerusa0_.usage_cost) as total_cost,
	avg(printerusa0_.usage_cost) as average_cost ,
	count(printerusa0_.printer_usage_log_id)  as total_jobs,
	printer1_.server_name ,
	printer1_.printer_name ,
	printer1_.physical_printer_id ,
	printer1_.printer_type ,
	printer1_.location ,
	sum(printerusa0_.total_sheets) as total_sheets,
	sum(printerusa0_.total_color_pages) as total_color_pages ,
	sum(printerusa0_.duplex_pages) as total_duplex_pages
from 
	tbl_printer_usage_log printerusa0_ 
	inner join tbl_printer printer1_ on printerusa0_.printer_id=printer1_.printer_id 
	inner join tbl_user user2_ on printerusa0_.used_by_user_id=user2_.user_id 
	inner join tbl_account account3_ on printerusa0_.charged_to_account_id=account3_.account_id 
	inner join tbl_account account4_ on printerusa0_.assoc_with_account_id=account4_.account_id
where 
	printerusa0_.usage_date>= @start_date
	and printerusa0_.usage_date<= @end_date 
	and printerusa0_.usage_allowed='Y' 
	and printerusa0_.refunded='N'
	and printerusa0_.printed='Y'
group by 
	printer1_.display_name ,
	printer1_.server_name ,
	printer1_.printer_name ,
	printer1_.physical_printer_id ,
	printer1_.printer_type ,
	printer1_.location 
order by 
	lower(printer1_.display_name) 