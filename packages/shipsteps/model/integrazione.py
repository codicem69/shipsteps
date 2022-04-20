class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('integrazione', pkey='id', name_long='!![en]integration', name_plural='!![en]integration',
                        caption_field='cargo_unload_id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_short='arrival_id'
                    ).relation('arrival.id', relation_name='integrazione', mode='foreignkey', onDelete='cascade')
        tbl.column('cargo_unl_load_id',size='22', name_long='cargo_unl_load_id'
                    ).relation('cargo_unl_load.id', relation_name='cargo_integrazione', mode='foreignkey', onDelete='cascade')
        tbl.column('noleggiatore', name_short='!![en]Charterers')
        tbl.column('place_origin_goods',size='22',name_short='!![en]Place origin goods').relation('unlocode.place.id',
                                            relation_name='place_origingoods', mode='foreignkey', onDelete='raise')
        tbl.column('place_dest_goods',size='22',name_short='!![en]Place destination goods').relation('unlocode.place.id',
                                            relation_name='place_destgoods', mode='foreignkey', onDelete='raise')                                            
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        