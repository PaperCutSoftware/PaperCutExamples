print DATEADD(DAY,-30,getdate())
select 
	user2_.user_name as col_0_0_, 
	user2_.full_name as col_1_0_, 
	sum(printerusa0_.total_pages) as col_2_0_, 
	avg(printerusa0_.total_pages) as col_3_0_, 
	sum(printerusa0_.usage_cost) as col_4_0_, 
	avg(printerusa0_.usage_cost) as col_5_0_, 
	count(printerusa0_.printer_usage_log_id) as col_6_0_, 
	sum(printerusa0_.total_sheets) as col_7_0_, 
	sum(printerusa0_.total_color_pages) as col_8_0_, 
	user2_.department as col_9_0_,
	user2_.office as col_10_0_, 
	user2_.card_number as col_11_0_, 
	sum(printerusa0_.duplex_pages) as col_12_0_ 
from 
	tbl_printer_usage_log printerusa0_ 
	inner join tbl_printer printer1_ on printerusa0_.printer_id=printer1_.printer_id 
	inner join tbl_user user2_ on printerusa0_.used_by_user_id=user2_.user_id 
	inner join tbl_account account3_ on printerusa0_.charged_to_account_id=account3_.account_id 
	inner join tbl_account account4_ on printerusa0_.assoc_with_account_id=account4_.account_id 
where 
	printerusa0_.usage_date>=DATEADD(DAY,-30,getdate())
	and printerusa0_.usage_allowed='Y' 
	and printerusa0_.refunded='N' 
	and printerusa0_.printed='Y' 
group by 
	user2_.user_name , 
	user2_.full_name , 
	user2_.department , 
	user2_.office , 
	user2_.card_number 
order by 
	sum(printerusa0_.total_pages) desc