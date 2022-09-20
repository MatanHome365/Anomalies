from anomalies.base_anomaly import Anomaly
from configuration import config


class TenantMoveOutDateAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 4
        anomaly_type_name = 'Moved Out Tenants Which Marked As Active'
        handling_by = 'Support'
        id_name = 'tenant_id'
        key_reference_id = 'property_id'
        file_name = 'moved_out_active_tenants.xlsx'
        subject = 'Anomaly Detection Alert - Moved Out Tenants Which Marked As Active'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of tenants which marked as active, although should be ' \
                     'inactive due to passing moved out date.\nPlease find table below and attached file showing detailed tenants list:\n'

        query = """select distinct p.property_id, t.tenant_id, p.presented_address "Address", pu.full_name "Metro Director",
                t.full_name "Tenant Name", rl.move_out_date::text "Move Out Date", t.tenant_status "Tenant Status",
                t.secondary_status "Secondary Status", rl.start_date::text
                                                                "Lease Start Date", rl.end_date::text "Lease End Date"
                from "Rental_Listing" rl
                 inner join "Tenants" t on t.tenant_id = rl.tenant_id
                 inner join "Properties" p on p.property_id = rl.property_id
                 inner join "PM_users" pu on pu.pm_user_id = p.account_manager_id
                where new_active = 1 and rl.move_out_date is not null and rl.move_out_date < current_date::text and t.full_name not ilike '%test%'
                order by rl.move_out_date"""

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)


