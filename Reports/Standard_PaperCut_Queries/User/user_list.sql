SELECT		tU.user_id as col0,
			tU.user_name as "Username",
			tU.full_name as "Full Name",
			tU.email as "Email",
			tU.department as "Department",
			tU.office as "Office",
			tU.card_number as "Primary Card Number",
			tU.notes as "Notes",
			tU.total_pages as "Total Printed Pages",
			tU.total_jobs as "Jobs",
			tU.net_total_megabytes as col_10,
			tU.net_total_time_hours as col_11,
			tU.last_user_activity as "Last activity",
			tU.created_date as "Created Date",
			tU.internal as "Internal User",
			tU.card_number2 as "Secondary Card Number",
			tU.secondary_user_name as "Username alias",
			tA.restricted as "Restricted",
			tA.use_global_overdraft as col_18,
			tA.overdraft as col_19,
			sum(tA2.balance) as "Balance"
FROM		tbl_user tU
INNER JOIN	tbl_user_account	tUA		on tU.user_id=tUA.user_id
INNER JOIN	tbl_account			tA		on tUA.account_id=tA.account_id
INNER JOIN	tbl_user_account	tUA2	on tU.user_id=tUA2.user_id
INNER JOIN	tbl_account			tA2		on tUA2.account_id=tA2.account_id
WHERE		tU.deleted='N' and
			tA.account_type='USER' and
			(tA2.account_type in ('USER-001' , 'USER-002', 'USER'))
GROUP BY	tU.user_id ,
			tU.user_name ,
			tU.full_name ,
			tU.email ,
			tU.department ,
			tU.office ,
			tU.card_number ,
			tU.notes ,
			tU.total_pages ,
			tU.total_jobs ,
			tU.net_total_megabytes ,
			tU.net_total_time_hours ,
			tU.last_user_activity ,
			tU.created_date ,
			tU.internal ,
			tU.card_number2 ,
			tU.secondary_user_name ,
			tA.restricted ,
			tA.use_global_overdraft ,
			tA.overdraft