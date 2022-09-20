from anomalies.base_anomaly import Anomaly
from configuration import config


class DuplicatePaymentReferenceAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 13
        anomaly_type_name = 'Duplicate Payment Reference'
        handling_by = 'Support'
        id_name = 'Payment Reference'
        key_reference_id = 'Payment Reference'
        file_name = None
        subject = 'Anomaly Detection Alert - Duplicate Payment Reference!!'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of duplicate payments with the same payment reference.' \
                     '\nPlease find table below:\n'

        query = """select payment_reference "Payment Reference", payment_method "Payment Method",
               amount::numeric/100 Amount, transfer_reference "Transfer Reference", date::text "Payment Date" from "Payments" where payment_reference in (
            select payment_reference
            from "Payments" p where status = 'success' and payment_reference in (
                select payment_reference
                from "Payments"
                where (payment_reference ilike '%pi%' or payment_reference ilike '%py%') and date >= '2022-06-01 00:00:00'
                group by payment_reference
                having count(*) > 1)
            group by payment_reference
            having count(*) > 1)
        order by payment_reference """

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_NONE_CHANNEL_CODE)



