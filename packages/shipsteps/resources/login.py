# -*- coding: UTF-8 -*-

from gnr.web.gnrwebpage import BaseComponent
        
class LoginComponent(BaseComponent):
    
    def onAuthenticating_shipsteps(self,avatar,rootenv=None):
        agency_id = self.db.table('shipsteps.staff').readColumns(where='$user_id=:u_id', 
                            u_id=avatar.user_id, columns='$agency_id')
        rootenv['current_agency_id'] = agency_id 
        