class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('port_facility',pkey='facility_code',name_long='Port facility',name_plural='Port facilities',caption_field='facility_code')
        self.sysFields(tbl,id=False)
        tbl.column('facility_code',size='10',name_long='!![en]Facility code',name_short='!![en]Facility code') 
        tbl.column('country', name_short='!![en]Country')
        tbl.column('nome_porto', name_short='!![en]Port name')
        tbl.column('nome_facility',name_short='!![en]Facility name')
        tbl.column('descrizione', name_short='!![en]Description')
        tbl.column('longitudine', name_short='!![en]Longitude')
        tbl.column('latitudine', name_short='!![en]Latitude')
        tbl.column('piano_approvato', dtype='B', name_short='!![en]Plan approved')
        tbl.column('ultimo_agg', name_short='!![en]Last updated')
