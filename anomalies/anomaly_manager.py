from configuration import config
from anomaly_factory import AnomalyFactory


class AnomalyManager:
    def __init__(self):
        self.anomalies = [config.SECURITY_DEPOSIT_ANOMALY, config.DUPLICATE_TRANSACTIONS_ANOMALY,
                          config.TENANT_MOVE_OUT_DATE_ANOMALY, config.PLANS_END_DATE_ANOMALY,
                          config.PROJECT_MULTIPLE_PAYMENTS_ANOMALY, config.DUPLICATE_RECURRING_ANOMALY,
                          config.EXPIRED_LEASES_ANOMALY, config.DUPLICATE_PAYMENT_REFERENCE_ANOMALY]
        self.anomaly_factory = AnomalyFactory()

    def run_anomalies(self):
        for anomaly_name in self.anomalies:
            anomaly = self.anomaly_factory.get_anomaly(anomaly_name)
            anomaly.applying_anomaly()


if __name__ == '__main__':
    AnomalyManager().run_anomalies()