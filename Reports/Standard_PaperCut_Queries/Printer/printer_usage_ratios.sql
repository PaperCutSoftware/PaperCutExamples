declare @days_to_report int
set @days_to_report = 365

declare @total_pages decimal
set @total_pages = (select sum(total_pages) from tbl_printer_usage_log where usage_date >= DATEADD(DAY,-@days_to_report,getdate()) and usage_allowed= 'Y'	and refunded= 'N' 	and printed = 'Y' )
print @total_pages

select 
	printer1_.display_name ,
	sum(printerusa0_.total_pages) as total_pages,
	(sum(printerusa0_.total_pages) / @total_pages)*100 as ratio,
	sum(printerusa0_.total_color_pages) as total_color_pages ,
	sum(printerusa0_.total_pages) -	sum(printerusa0_.total_color_pages) as total_greyscale_pages,
	sum(printerusa0_.total_color_pages) / cast(sum(printerusa0_.total_pages) as decimal) * 100 as ratio_color,
	printer1_.server_name ,
	printer1_.printer_name 
from 
	tbl_printer_usage_log printerusa0_ 
	inner join tbl_printer printer1_ on printerusa0_.printer_id=printer1_.printer_id 
	inner join tbl_user user2_ on printerusa0_.used_by_user_id=user2_.user_id 
	inner join tbl_account account3_ on printerusa0_.charged_to_account_id=account3_.account_id 
	inner join tbl_account account4_ on printerusa0_.assoc_with_account_id=account4_.account_id 
where 
	printerusa0_.usage_date  >= DATEADD(DAY,-@days_to_report,getdate()) 
	and printerusa0_.usage_allowed= 'Y'
	and printerusa0_.refunded= 'N' 
	and printerusa0_.printed = 'Y' 
group by 
	printer1_.display_name ,
	printer1_.server_name ,
	printer1_.printer_name 
order by 
	lower(printer1_.display_name)