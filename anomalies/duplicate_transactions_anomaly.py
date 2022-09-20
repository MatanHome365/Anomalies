from anomalies.base_anomaly import Anomaly
from configuration import config


class DuplicateTransactions(Anomaly):
    def __init__(self):
        anomaly_type_id = 2
        anomaly_type_name = 'duplicate transactions with the same property, category, due date and amount'
        handling_by = 'Support'
        id_name = 'property_id'
        key_reference_id = 'account_paid_by'

        query = """select t.account_paid_by, p.short_address, unit, p.property_id, due_date::text "Due Date", category_name "Category Name",
               amount::numeric/100 "Amount", status "Transaction Status", memo "Memo",
               count(*) "Duplicate Transactions Count"
        from "Transactions" t inner join "Properties" p on p.property_id = t.property_id
        where t.status in ('paid', 'readyForPayment', 'pendingAch') and memo <> 'Auto ML Process' and due_date >= '2022-07-01 00:00:00' and file_url is null and amount > 0 and is_partial_payment is null
          and p.property_status not in ('Inactive', 'readyForDeactivation', 'phasingOut') and memo not ilike '%%test%%'
        group by t.account_paid_by, p.short_address, unit, p.property_id, due_date, category_name, amount, status, presented_address, memo
        having count(*) > 1
        order by "Duplicate Transactions Count" desc """

        file_name = 'multi_trans_category_amount.xlsx'
        subject = 'Anomaly Detection Alert - duplicate transactions with the same property, category, due date and amount !!'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of duplicate transactions with the same property, category, due date and amount.' \
                     '\nPlease find table below and attached file showing detailed list:\n'

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)



