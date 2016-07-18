-- esets    org.name           num_assignees
-- 3287:    Bose Coropoation   9
-- 88762:   Bose Institute     4
-- 270675:  SANWA BOSEI KK     2


SELECT
  O.eset as eset,
  O.name as org_name,
  O.who as org_who,
  O.stamp as org_stamp,
  O.grouped as org_grouped,
  O.size as org_size,
  O.size_active as org_size_active,
  A.assignee_id as assignee_id,
  A.abbreviation as assignee_abbreviation,
  A.size as assignee_size,
  A.size_active as assignee_size_active
FROM OrganisationName O
JOIN Assignee A USING(eset)
WHERE O.eset = 88762
;
