class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('port_facility',pkey='facility_code',name_long='Port facility',name_plural='Port facilities',caption_field='facility_code')
        self.sysFields(tbl,id=False)
        tbl.column('facility_code',size='10',name_long='!![en]Facility code',name_short='!![en]Facility code') 
        tbl.column('country', name_short='!![en]Country')
        tbl.column('port_name', name_short='!![en]Port name')
        tbl.column('facility_name',name_short='!![en]Facility name')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('longitude', name_short='!![en]Longitude')
        tbl.column('latitude', name_short='!![en]Latitude')
        tbl.column('plan_approved', dtype='B', name_short='!![en]Plan approved')
        tbl.column('last_updated', dtype='DH', name_short='!![en]Last updated')
