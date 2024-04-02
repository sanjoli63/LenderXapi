class EncompassSettings:
    def __init__(self):
        self.Key = None
        self.Description = None
        self.Default = False

    def __str__(self):
        return self.Description

    @staticmethod
    def get_system_defaults():
        return [
            EncompassSettings(Key="356", Description="Subj. Property Appraised Value (356)", Default=True),
            EncompassSettings(Key="641", Description="Appraisal Fee (641)", Default=False),
            EncompassSettings(Key="617", Description="Appraisal Company (617)", Default=True),
            EncompassSettings(Key="619", Description="Appraisal Company Address (619)", Default=True),
            EncompassSettings(Key="620", Description="Appraisal Company City (620)", Default=True),
            EncompassSettings(Key="1244", Description="Appraisal Company State (1244)", Default=True),
            EncompassSettings(Key="621", Description="Appraisal Company Zip (621)", Default=True),
            EncompassSettings(Key="622", Description="Appraisal Company Phone (622)", Default=True),
            EncompassSettings(Key="618", Description="Appraiser Name (618)", Default=True),
            EncompassSettings(Key="1401", Description="Loan Program (1401)", Default=False),
            EncompassSettings(Key="1821", Description="Estimated Value", Default=False),
            EncompassSettings(Key="ULDD.X30", Description="Property Valuation Effective Date", Default=False),
            EncompassSettings(Key="ULDD.X31", Description="UCDP Doc File ID", Default=False),
            EncompassSettings(Key="CreateEFolder", Description="Auto Create eFolder", Default=True),
        ]

    @staticmethod
    def is_setting_enabled(key, default_value, service_context):
        setting = service_context.Company.GetServiceCustomValue("SL" + key.strip())
        if setting == "Y":
            return True
        elif setting == "N":
            return False
        else:
            return default_value

    @staticmethod
    def is_setting_enabled_default(key, service_context):
        setting = service_context.Company.GetServiceCustomValue("SL" + key.strip())
        if setting == "":
            default_value = next(item.Default for item in EncompassSettings.get_system_defaults() if item.Key == key)
            setting = "Y" if default_value else "N"
        return setting == "Y"

    @staticmethod
    def get_encompass_value(key, service_context):
        value = service_context.CurrentLoan.Fields.GetValue(key)
        return str(value) if value is not None else ""
