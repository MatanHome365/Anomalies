from anomalies.base_anomaly import Anomaly
from configuration import config


class SecurityDepositAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 1
        anomaly_type_name = 'Multiple Releases Of Security Deposit'
        handling_by = 'Shauly'
        id_name = 'Trans Num'
        key_reference_id = 'Property ID'
        file_name = 'multi_sd_per_owner.xlsx'
        subject = 'Anomaly Detection Alert - Multiple Releases Of Security Deposit !!'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of security deposit releases of more than 1 transaction per property.' \
                     '\nPlease find table below and attached file showing detailed transactions list:\n'

        query = """select distinct t.transaction_number "Trans Num", status, p.property_id "Property ID", p.presented_address "Address", t.account_paid_by "Account ID", hc.name "Owner Name", amount::numeric / 100 "Amount"
        from "Transactions" t
                 inner join "Holding_Companies" hc on hc.company_id = t.account_paid_by
                inner join "Properties" p on p.property_id = t.property_id
        where date_created >= '2022-04-01 00:00:00' and category_name = 'Release Security Deposit to tenant' and status = 'paid' and amount > 0 and t.property_id
        in (select distinct t.property_id "Account ID"
            from "Transactions" t
            where date_created >= '2022-04-01 00:00:00' and category_name = 'Release Security Deposit to tenant' and status in ('paid', 'readyForPayment') and amount > 0
            group by t.property_id
            having count(*) > 1)
        order by "Property ID" """

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)






