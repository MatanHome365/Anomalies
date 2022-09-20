from anomalies.base_anomaly import Anomaly
from configuration import config


class DuplicateRecurringAnomaly(Anomaly):
    def __init__(self):
        anomaly_type_id = 5
        anomaly_type_name = 'More Than One Recurring Per Property'
        handling_by = 'Support'
        id_name = 'Property ID'
        key_reference_id = 'Property ID'
        file_name = 'dup_recurring.xlsx'
        subject = 'Anomaly Detection Alert - More Than One Recurring Per Property'
        intro_mail = 'Pay Attention!\n\nFound out anomaly of properties with more than one recurring record with the same category.' \
                     '\nPlease find table below and attached file showing detailed recurring list:\n'

        query = """select p.property_id "Property ID", c.name "Category Name", count(*) "Duplicate Recurring Count"
        from "Recurring" r
                 inner join  "Categories" c on c.category_id = r.category_id
                 inner join "Properties" p on p.property_id = r.property_id
        where r.active='true' and p.property_id <> 'EA840872-C170-4807-B4C5-F930EB89269C'
        group by p.property_id, c.name
        having count(*) > 1"""

        super().__init__(anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                config.INTERNAL_RND_MAIL, subject, intro_mail, config.SLACK_RND_CHANNEL_CODE)



