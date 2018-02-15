USE [papercut]
GO

/****** Object:  StoredProcedure [dbo].[udp_user_printing_printer_summary]    Script Date: 4/04/2016 2:50:09 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[udp_user_printing_printer_summary] @days_to_report int as

print DATEADD(DAY,-@days_to_report,getdate()) 

select 
	printer1_.display_name as printer_name, 
	user2_.user_name , 
	user2_.full_name , 
	sum(printerusa0_.total_pages) as total_pages, 
	avg(printerusa0_.total_pages) as average_pages, 
	sum(printerusa0_.usage_cost) as total_cost, 
	avg(printerusa0_.usage_cost) as average_cost, 
	count(printerusa0_.printer_usage_log_id) as total_jobs, 
	printer1_.server_name, 
	printer1_.printer_name, 
	user2_.department, 
	sum(printerusa0_.total_color_pages) as total_color_pages, 
	sum(printerusa0_.duplex_pages) as duplex_pages 
from 
	tbl_printer_usage_log printerusa0_ 
	inner join tbl_printer printer1_ on printerusa0_.printer_id=printer1_.printer_id 
	inner join tbl_user user2_ on printerusa0_.used_by_user_id=user2_.user_id 
	inner join tbl_account account3_ on printerusa0_.charged_to_account_id=account3_.account_id 
	inner join tbl_account account4_ on printerusa0_.assoc_with_account_id=account4_.account_id 
where 
	printerusa0_.usage_date>=DATEADD(DAY,-@days_to_report,getdate())   
	and printerusa0_.usage_allowed= 'Y' 
	and printerusa0_.refunded = 'N'
	and printerusa0_.printed= 'Y'
group by 
	user2_.user_name , 
	user2_.full_name , 
	printer1_.display_name , 
	printer1_.server_name , 
	printer1_.printer_name , 
	user2_.department 
order by 
	lower(user2_.user_name), 
	lower(printer1_.display_name)
GO

