select 
	user0_.user_id as col_0_0_, 
	user0_.user_name as col_1_0_, 
	user0_.full_name as col_2_0_, 
	account2_.restricted as col_3_0_, 
	user0_.deleted_date as col_4_0_, 
	user0_.modified_by as col_5_0_, 
	user0_.email as col_6_0_, 
	user0_.department as col_7_0_, 
	user0_.office as col_8_0_, 
	user0_.card_number as col_9_0_, 
	user0_.notes as col_10_0_, 
	user0_.internal as col_11_0_, 
	user0_.created_date as col_12_0_, 
	user0_.card_number2 as col_13_0_, 
	account2_.balance as col_14_0_ 
from 
	tbl_user user0_ 
	inner join tbl_user_account accountlin1_ on user0_.user_id=accountlin1_.user_id 
	inner join tbl_account account2_ on accountlin1_.account_id=account2_.account_id 
where 
	user0_.deleted='Y' 
	and account2_.account_type='USER' 
order by 
	user0_.user_name asc