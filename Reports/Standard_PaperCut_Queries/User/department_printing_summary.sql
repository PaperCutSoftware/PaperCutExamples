--Set the number of days to include in the report

declare @days_to_report int
set @days_to_report = 365

select 
	userfieldh0_.field_value as col_0_0_, 
	sum(printerusa1_.total_pages) as col_1_0_, 
	avg(printerusa1_.total_pages) as col_2_0_, 
	sum(printerusa1_.usage_cost) as col_3_0_, 
	avg(printerusa1_.usage_cost) as col_4_0_, 
	count(printerusa1_.printer_usage_log_id) as col_5_0_, 
	sum(printerusa1_.total_sheets) as col_6_0_, 
	sum(printerusa1_.total_color_pages) as col_7_0_, 
	sum(printerusa1_.duplex_pages) as col_8_0_ 
from 
	tbl_user_field_history userfieldh0_, tbl_printer_usage_log printerusa1_ 
	inner join tbl_printer printer2_ on printerusa1_.printer_id=printer2_.printer_id 
	inner join tbl_user user3_ on printerusa1_.used_by_user_id=user3_.user_id 
	inner join tbl_account account4_ on printerusa1_.charged_to_account_id=account4_.account_id 
	inner join tbl_account account5_ on printerusa1_.assoc_with_account_id=account5_.account_id 
where 
	printerusa1_.usage_date>=DATEADD(DAY,-@days_to_report,getdate())   
	and printerusa1_.usage_allowed='Y' 
	and printerusa1_.refunded='N' 
	and printerusa1_.printed='Y'
	and userfieldh0_.field_type='DEPARTMENT' 
	and userfieldh0_.user_id=printerusa1_.used_by_user_id 
	and userfieldh0_.start_date<=printerusa1_.usage_date 
	and userfieldh0_.end_date>printerusa1_.usage_date 
group by 
	userfieldh0_.field_value 
order by 
	userfieldh0_.field_value 