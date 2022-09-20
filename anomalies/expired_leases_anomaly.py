from anomalies.base_anomaly import Anomaly
from configuration import config


class ExpiredLeasesAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 3
        anomaly_type_name = 'Active Leases With Expired End Date'
        handling_by = 'Support'
        id_name = 'property_id'
        key_reference_id = 'tenant_id'
        file_name = 'leases_with_expired_end_date.xlsx'
        subject = 'Anomaly Detection Alert - Active Leases With Expired End Date !!'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of active leases with expired end date.' \
                                                                                '\nPlease find attached file showing detailed anomaly list.\n\n'

        query = """ select distinct p.property_id ,p.presented_address "Address", pu.full_name "Metro Director", t.full_name "Tenant Name", rl.start_date::text "Lease Start Date",
               rl.end_date::text "Lease End Date", rl.lease_type "Lease Type", t.tenant_id
        from "Rental_Listing" rl
                 inner join "Properties" p on p.property_id = rl.property_id
                 inner join "Tenants" t on t.tenant_id = rl.tenant_id
                inner join "PM_users" pu on pu.pm_user_id = p.account_manager_id
        where new_active = 1 and end_date < current_date and lease_type = 'Yearly' and t.full_name not ilike '%test%' """

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)
