from gnr.web.gnrwebstruct import struct_method

class GnrCustomWebPage(object):

    @struct_method
    def fi_slotbar_settings(self, slot, **kwargs):

        if self.isGuest:
            return
        if self.user in ('admin','superadmin','_DEV_'):
            slot.userSettings()
        else:
            menu = slot.menudiv(iconClass='iconbox gear')
            menu.menuline('User preferences',
                      action='genro.framedIndexManager.openUserPreferences()')
            menu.menuline('-')
            menu.menuline('User settings',
                      action='genro.framedIndexManager.openUserSettings()')
