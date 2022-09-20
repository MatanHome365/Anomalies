from anomalies.base_anomaly import Anomaly
from configuration import config


class PlansExpiredEndDateAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 8
        anomaly_type_name = 'Active Plans With Expired End Date'
        handling_by = 'Support'
        id_name = 'Property ID'
        key_reference_id = 'Property ID'
        file_name = 'plans_with_expired_end_date.xlsx'
        subject = 'Anomaly Detection Alert - Active Plans With Expired End Date !!'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of active plans with expired end date.' \
                                                                                '\nPlease find attached file showing detailed anomaly list.\n\n'

        query = """ select distinct p.presented_address "Presented Address", pu.full_name "Metro Director",
                p.property_status "Property Status", p.property_id "Property ID", effective_date::text "Effective Date", plan_end_date::text "Plan End Date"
                from "Plans" pl
                         inner join "Properties" p on p.property_id = pl.property_id
                         inner join "PM_users" pu on pu.pm_user_id = p.account_manager_id
                where pl.active = 1 and plan_end_date < current_date and p.property_status not in ('Inactive', 'readyForDeactivation', 'phasingOut')
                order by "Plan End Date" """

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)

