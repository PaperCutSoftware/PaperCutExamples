SELECT   account0_.account_id           AS account1_0_, 
         account0_.account_type         AS account2_0_, 
         account0_.account_name         AS account3_0_, 
         account0_.balance              AS balance0_, 
         account0_.restricted           AS restricted0_, 
         account0_.overdraft            AS overdraft0_, 
         account0_.pin                  AS pin0_, 
         account0_.use_global_overdraft AS use8_0_, 
         account0_.notes                AS notes0_, 
         account0_.deleted              AS deleted0_, 
         account0_.deleted_date         AS deleted11_0_, 
         account0_.created_date         AS created12_0_, 
         account0_.created_by           AS created13_0_, 
         account0_.modified_date        AS modified14_0_, 
         account0_.modified_by          AS modified15_0_, 
         account0_.parent_id            AS parent16_0_, 
         account0_.account_name_lower   AS account17_0_, 
         account0_.sub_name             AS sub18_0_, 
         account0_.sub_name_lower       AS sub19_0_, 
         account0_.disabled             AS disabled0_, 
         account0_.disabled_until       AS disabled21_0_, 
         account0_.comments             AS comments0_, 
         account0_.invoicing            AS invoicing0_, 
         account0_.sub_pin              AS sub24_0_, 
         account0_.modified_ticks       AS modified25_0_ 
FROM     tbl_account account0_ 
WHERE    account0_.deleted='N' 
AND      account0_.account_type='SHARED'
AND      account0_.account_name_lower<> '!!template account!!' 
ORDER BY account0_.account_name_lower ASC, 
         COALESCE(account0_.sub_name_lower, '!!!')