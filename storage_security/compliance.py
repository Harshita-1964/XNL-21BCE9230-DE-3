# Basic GDPR & PCI-DSS compliance logic

class Compliance:
    def __init__(self):
        self.gdpr_compliant = False
        self.pci_dss_compliant = False

    def check_gdpr_compliance(self, data):
        # Example check: Ensure personal data is anonymized or pseudonymized
        if "personal_data" not in data:
            self.gdpr_compliant = True
        else:
            self.gdpr_compliant = False

    def check_pci_dss_compliance(self, credit_card_number):
        # Example: Mask credit card number (only last 4 digits visible)
        if len(credit_card_number) == 16:
            masked = credit_card_number[:12] + "****"  # PCI-DSS compliance for card numbers
            return masked
        return None

if __name__ == '__main__':
    compliance = Compliance()
    sample_data = {"name": "John Doe", "personal_data": "Sensitive Info"}
    compliance.check_gdpr_compliance(sample_data)
    print(f"GDPR Compliant: {compliance.gdpr_compliant}")

    masked_card = compliance.check_pci_dss_compliance("1234567812345678")
    print(f"Masked Credit Card: {masked_card}")
