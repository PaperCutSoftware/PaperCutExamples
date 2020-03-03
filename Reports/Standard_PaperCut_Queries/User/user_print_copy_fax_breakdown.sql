declare @days_to_report int
set @days_to_report = 365

declare @user_name varchar(255)
set @user_name  = '[All Users]'

select 
	user2_.user_name as user_name, 
	user2_.full_name as full_name, 
	printerusa0_.job_type as job_type, 
	sum(printerusa0_.total_pages) as total_pages,
	sum(printerusa0_.usage_cost) as usage_cost, 
	sum(printerusa0_.total_color_pages) as total_color_pages, 
	sum(printerusa0_.duplex_pages) as total_duplex_pages 
from 
	tbl_printer_usage_log printerusa0_ 
	inner join tbl_printer printer1_ on printerusa0_.printer_id=printer1_.printer_id 
	inner join tbl_user user2_ on printerusa0_.used_by_user_id=user2_.user_id 
	inner join tbl_account account3_ on printerusa0_.charged_to_account_id=account3_.account_id 
	inner join tbl_account account4_ on printerusa0_.assoc_with_account_id=account4_.account_id 
where 
	printerusa0_.usage_date >= DATEADD(DAY,-@days_to_report,getdate()) 
	and printerusa0_.usage_allowed='Y'
	and printerusa0_.refunded='N' 
	--and (printerusa0_.job_type in ('COPY','PRINT') and printerusa0_.printed=? or printerusa0_.job_type<>?) 
group by 
	user2_.user_name , 
	user2_.full_name , 
	printerusa0_.job_type 
order by 
	user2_.user_name