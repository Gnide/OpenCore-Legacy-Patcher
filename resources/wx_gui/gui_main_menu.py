import wx
from resources.wx_gui import (
    gui_build,
    gui_macos_installer_download,
    gui_sys_patch,
    gui_support,
    gui_help,
    gui_settings,
)
from resources import constants
from data import os_data

class MainMenu(wx.Frame):
    def __init__(self, parent: wx.Frame, title: str, global_constants: constants.Constants, screen_location: tuple = None):
        super(MainMenu, self).__init__(parent, title=title, size=(350, 300), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.constants: constants.Constants = global_constants
        self.title: str = title

        self.model_label: wx.StaticText = None
        self.build_button: wx.Button = None

        self._generate_elements()

        self.SetPosition(screen_location) if screen_location else self.Centre()
        self.Show()


    def _generate_elements(self) -> None:
        """
        Generate UI elements for the main menu

        Format:
          - Title label: OpenCore Legacy Patcher v{X.Y.Z}
          - Text:        Model: {Build or Host Model}
          - Buttons:
            - Build and Install OpenCore
            - Post-Install Root Patch
            - Create macOS Installer
            - Settings
            - Help
          - Text:        Copyright
        """

        # Title label: OpenCore Legacy Patcher v{X.Y.Z}
        title_label = wx.StaticText(self, label=f"OpenCore Legacy Patcher v{self.constants.patcher_version}", pos=(-1,1))
        title_label.SetFont(wx.Font(19, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, ".AppleSystemUIFont"))
        title_label.Center(wx.HORIZONTAL)

        # Text: Model: {Build or Host Model}
        model_label = wx.StaticText(self, label=f"Model: {self.constants.custom_model or self.constants.computer.real_model}", pos=(-1,30))
        model_label.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, ".AppleSystemUIFont"))
        model_label.Center(wx.HORIZONTAL)
        self.model_label = model_label

        # Buttons:
        menu_buttons = {
            "Build and Install OpenCore": self.on_build_and_install,
            "Post-Install Root Patch":    self.on_post_install_root_patch,
            "Create macOS Installer":     self.on_create_macos_installer,
            "Settings":                   self.on_settings,
            "Help":                       self.on_help
        }
        button_y = model_label.GetPosition()[1] + 20
        for button_name, button_function in menu_buttons.items():
            button = wx.Button(self, label=button_name, pos=(-1, button_y), size=(200, 30))
            button.Bind(wx.EVT_BUTTON, button_function)
            button.Center(wx.HORIZONTAL)
            button_y += 30

            if button_name == "Build and Install OpenCore":
                self.build_button = button
                if gui_support.CheckProperties(self.constants).host_can_build() is False:
                    button.Disable()
            elif button_name == "Post-Install Root Patch":
                if self.constants.detected_os < os_data.os_data.big_sur:
                    button.Disable()

        # Text: Copyright
        copy_label = wx.StaticText(self, label=self.constants.copyright_date, pos=(-1, button_y + 10))
        copy_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, ".AppleSystemUIFont"))
        copy_label.Center(wx.HORIZONTAL)

        # Set window size
        self.SetSize((350, copy_label.GetPosition()[1] + 50))


    def on_build_and_install(self, event: wx.Event = None):
        self.Hide()
        gui_build.BuildFrame(
            parent=None,
            title=self.title,
            global_constants=self.constants,
            screen_location=self.GetPosition()
        )
        self.Destroy()


    def on_post_install_root_patch(self, event: wx.Event = None):
        self.Hide()
        gui_sys_patch.SysPatchMenu(
            parent=None,
            title=self.title,
            global_constants=self.constants,
            screen_location=self.GetPosition()
        )
        self.Destroy()


    def on_create_macos_installer(self, event: wx.Event = None):
        gui_macos_installer_download.macOSInstallerFrame(
            parent=self,
            title=self.title,
            global_constants=self.constants,
            screen_location=self.GetPosition()
        )


    def on_settings(self, event: wx.Event = None):
        gui_settings.SettingsFrame(
            parent=self,
            title=self.title,
            global_constants=self.constants,
            screen_location=self.GetPosition()
        )

    def on_help(self, event: wx.Event = None):
        gui_help.HelpFrame(
            parent=self,
            title=self.title,
            global_constants=self.constants,
            screen_location=self.GetPosition()
        )
