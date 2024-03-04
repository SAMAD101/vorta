from PyQt6 import QtCore, uic

from vorta.utils import get_asset

uifile = get_asset("UI/scriptedit.ui")
ScriptEditUI, ScriptEditBase = uic.loadUiType(uifile)


class ScriptEditWindow(ScriptEditUI, ScriptEditBase):
    def __init__(self, context: str, profile, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        self.context = context
        if context == "pre":
            self.setWindowTitle(self.tr("Edit Pre-Backup Script"))
        elif context == "post":
            self.setWindowTitle(self.tr("Edit Post-Backup Script"))

        self.profile = profile
        self.saveScriptButton.clicked.connect(self.save_script)

        # Populate data from profile
        self.populate_from_profile()

    def populate_from_profile(self):
        """Populate the script editor with the current profile's script."""
        profile = self.profile
        if self.context == "pre":
            self.scriptEdit.setPlainText(profile.pre_backup_cmd)
        elif self.context == "post":
            self.scriptEdit.setPlainText(profile.post_backup_cmd)

    def save_profile_attr(self, attr, new_value):
        profile = self.profile
        setattr(profile, attr, new_value)
        profile.save()

    def save_script(self):
        script = self.scriptEdit.toPlainText()
        profile = self.profile
        if self.context == "pre":
            self.save_profile_attr("pre_backup_cmd", script)
        elif self.context == "post":
            self.save_profile_attr("post_backup_cmd", script)
        profile.save()
        self.close()