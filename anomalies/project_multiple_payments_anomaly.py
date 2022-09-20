from anomalies.base_anomaly import Anomaly
from configuration import config


class ProjectMultiplePaymentsAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 10
        anomaly_type_name = 'multiple pays for vendors on single projects'
        handling_by = 'Support'
        id_name = 'property_id'
        key_reference_id = 'property_id'
        file_name = 'multiple_pays_for_vendors_on_single_projects.xlsx'
        subject = 'Anomaly Detection Alert - multiple payments for vendors on single projects'
        intro_mail = 'find below table that contain the vendors that get multiple payments on single projects'

        query = """
            select *
            from "Anomalies_Type";
            select case when acc.nametype = 'Holding_Company' then 'Owner'
                when acc.nametype = 'Vendor' then 'Home365'
                    else acc.nametype
                        end as pay_by,
                   temp1.*
            from
            (select distinct account_paid_by,property_id, project_vendor_id,amount, status, count(*),min(date_created) min_date, max(date_created) max_date
            from "Transactions" t1
            where bill_type = 'projectComplete'
            and status in ('paid', 'readyForPayment')
            and date_created > '2022-09-01 00:00:00'
            and amount > 0
            group by account_paid_by,property_id, project_vendor_id,amount, status
            having count(*) > 1
            order by min_date desc) as temp1
            inner join "Accounts" acc on temp1.account_paid_by = acc.account_id;
            """

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                         config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)
