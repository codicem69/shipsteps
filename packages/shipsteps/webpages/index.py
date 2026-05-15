# -*- coding: utf-8 -*-
            
class GnrCustomWebPage(object):
    py_requires = 'plainindex'
    
    @property
    def index_url(self):
        return None

    def index_dashboard(self, root):
        port_id = self.db.currentEnv.get('current_port')
        agency_id = self.db.currentEnv.get('current_agency_id')
        agency_name = ''
        if agency_id:
            agency_name = self.db.table('agz.agency').readColumns(
                where='$id=:agency_id',
                agency_id=agency_id,
                columns='$agency_name'
            ) or ''
        print(agency_name)
        port_name = ''
        if port_id:
            port_name = self.db.table('unlocode.place').readColumns(
                where='$id=:port_id',
                port_id=port_id,
                columns='$descrizione'
            ) or ''

        wrapper = root.div(width='100%', height='100%',
                           text_align='center', background='white',
                           padding_top='30px')
        wrapper.img(src='/_pkg/shipsteps/resources/html_pages/images/shipsteps_logo.png',
                    style='width:30%;margin-top:30px;')
        wrapper.div('Shipsteps',
                    font_size='100px', color='#384D63',
                    margin_top='20px', margin_bottom='30px')
        wrapper.div(agency_name + ' - ' + port_name,
                    font_size='50px', color='#384D63',
                    margin_top='20px', margin_bottom='30px')
        wrapper.img(src='/_rsrc/common/html_pages/images/splash_logo.png',
                    style='width:20%;margin-top:30px;')
