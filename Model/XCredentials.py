import json
from Comm import LenderXComm

class XCredentials:
    def __init__(self):
        self.APIKey = None
        self.APISecret = None
        self.LXUser = None
        self.LXUserId = None
        self.BaseURL = None
        self.PaymentsEnabled = None
        self._permissions = None
        self._preferences = None

    @property
    def Permissions(self):
        if self._permissions is None:
            self._permissions = json.loads(LenderXComm.GetPermissions(self))
        return self._permissions

    @property
    def Preferences(self):
        if self._preferences is None:
            self._preferences = json.loads(LenderXComm.GetPreferences(self))
        return self._preferences

    def CheckPermission(self, path):
        perm = self.Permissions.get(path)
        return perm is not None and perm == "1"

    def GetPreferenceValue(self, path):
        pref = self.Preferences.get(path)
        return pref if pref is not None else None
