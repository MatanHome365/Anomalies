from anomalies.base_anomaly import Anomaly
from configuration import config


class TenantsMissingRecurringAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 7
        anomaly_type_name = 'Active Tenants Without Recurring'
        handling_by = 'Support'
        id_name = 'Property ID'
        key_reference_id = 'Account ID'
        subject = 'Anomaly Detection Alert - Active Tenants Without Recurring'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of active tenants without recurring.' \
                     '\nPlease find table below of detailed tenants list:\n'

        file_name = "Active Tenants Without Recurring.xlsx"

        query = """select p.property_id "Property ID", presented_address "Address", t.full_name "Tenant Name", t.tenant_id "Account ID",
               rl.start_date::text "Lease Start Date", rl.end_date::text "Lease End Date"
        from "Properties" p
                 inner join "Rental_Listing" rl on rl.property_id = p.property_id
                 inner join "Tenants" T on rl.tenant_id = T.tenant_id
        where p.property_status not in ('Inactive', 'readyForDeactivation', 'phasingOut')
          and p.property_id not in (select property_id from "Recurring" where "Recurring".active ='true')
          and is_rentable = 1 and rl.new_active = 1 and move_out_date is null and "tenantStatus" in ('Active')"""


        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)




