from gnr.web.gnrwebstruct import struct_method

class GnrCustomWebPage(object):

    @struct_method
    def fi_slotbar_settings(self, slot, **kwargs):

        if self.isGuest:
            return
        tags = self.userTags
        #se in tags troviamo i valori di admin o superadmin o _DEV_ allora non facciamo visualizzare le user preferences
        #nella rotellina in basso sx di settings
        if set(['admin', 'superadmin', '_DEV_']) & set(tags.split(',')):
        #if self.user in ('admin','superadmin','_DEV_'):
            slot.userSettings()
        else:
            menu = slot.menudiv(iconClass='iconbox gear')
            menu.menuline('User preferences',
                      action='genro.framedIndexManager.openUserPreferences()')
            menu.menuline('-')
            menu.menuline('User settings',
                      action='genro.framedIndexManager.openUserSettings()')
