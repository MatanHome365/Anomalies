from security_deposit_anomaly import SecurityDepositAnomaly
from configuration import config
from duplicate_transactions_anomaly import DuplicateTransactions
from tenant_move_out_date_anomaly import TenantMoveOutDateAnomaly
from tenants_missing_recurring_anomaly import TenantsMissingRecurringAnomaly
from plans_expired_end_date_anomaly import PlansExpiredEndDateAnomaly
from project_multiple_payments_anomaly import ProjectMultiplePaymentsAnomaly
from expired_leases_anomaly import ExpiredLeasesAnomaly
from duplicate_recurring_anomaly import DuplicateRecurringAnomaly
from duplicate_payment_reference_anomaly import DuplicatePaymentReferenceAnomaly


class AnomalyFactory:

    def __init__(self):
        self.anomalies_dic = {config.SECURITY_DEPOSIT_ANOMALY: SecurityDepositAnomaly,
                              config.DUPLICATE_TRANSACTIONS_ANOMALY: DuplicateTransactions,
                              config.TENANT_MOVE_OUT_DATE_ANOMALY: TenantMoveOutDateAnomaly,
                              config.TENANTS_MISSING_RECURRING_ANOMALY: TenantsMissingRecurringAnomaly,
                              config.PLANS_END_DATE_ANOMALY: PlansExpiredEndDateAnomaly,
                              config.PROJECT_MULTIPLE_PAYMENTS_ANOMALY: ProjectMultiplePaymentsAnomaly,
                              config.EXPIRED_LEASES_ANOMALY: ExpiredLeasesAnomaly,
                              config.DUPLICATE_RECURRING_ANOMALY: DuplicateRecurringAnomaly,
                              config.DUPLICATE_PAYMENT_REFERENCE_ANOMALY: DuplicatePaymentReferenceAnomaly}

    def get_anomaly(self, name):
        if name in self.anomalies_dic:
            return self.anomalies_dic[name]()
        else:
            return None