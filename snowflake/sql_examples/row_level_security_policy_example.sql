-- Example Snowflake row access policy for regional finance users.
create or replace row access policy analytics.region_access_policy
as (region varchar) returns boolean ->
    current_role() in ('ACCOUNTADMIN', 'CRUISE_EXECUTIVE')
    or exists (
        select 1
        from security.user_region_access
        where user_name = current_user()
          and allowed_region = region
    );

alter table analytics.mart_executive_scorecard
add row access policy analytics.region_access_policy on (region);
