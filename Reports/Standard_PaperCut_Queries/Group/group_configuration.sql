

SELECT   group0_.group_id                 AS group1_6_, 
         group0_.group_name               AS group2_6_, 
         group0_.initial_credit           AS initial3_6_, 
         group0_.initially_restricted     AS initially4_6_, 
         group0_.schedule_period          AS schedule5_6_, 
         group0_.schedule_amount          AS schedule6_6_, 
         group0_.allow_accum              AS allow7_6_, 
         group0_.max_accum_balance        AS max8_6_, 
         group0_.reset_statistics         AS reset9_6_, 
         group0_.created_date             AS created10_6_, 
         group0_.created_by               AS created11_6_, 
         group0_.modified_date            AS modified12_6_, 
         group0_.modified_by              AS modified13_6_, 
         group0_.initial_settings_enabled AS initial14_6_, 
         group0_.modified_ticks           AS modified15_6_ 
FROM     tbl_group group0_ 
ORDER BY Lower(group0_.group_name) ASC