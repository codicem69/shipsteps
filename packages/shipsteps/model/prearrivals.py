# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('prearrivals', pkey='id', name_long='!![en]Pre-Arrival', name_plural='!![en]Pre-Arrivals',
                      caption_field='vessel_name', partition_port='port')
        self.sysFields(tbl)

        tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='port_prearr', mode='foreignkey', onDelete='raise')
        tbl.column('imbarcazione_id', size='22', name_short='!![en]Vessel name').relation('pfda.imbarcazione.id',relation_name='imb_prearr', 
                                                                                          mode='foreignkey', onDelete='raise')
        #tbl.column('vessel_details_id',size='22',name_long='!![en]Vessel',validate_notnull=True).relation(
        #                            'vessel_details.id',relation_name='vessel_name', mode='foreignkey', onDelete='raise')
        tbl.column('email_to', name_short='!![en]Email to')
        tbl.column('email_cc', name_short='!![en]Email cc')
        tbl.column('prearr_descr',size='22',name_long='!![en]PreArrivals description',validate_notnull=True).relation(
                                    'prearrivals_default.id',relation_name='prearr_df_descr', mode='foreignkey', onDelete='raise')
        tbl.column('data_invio', dtype='DH', name_short='!![en]Send date')
        tbl.pyColumn('privacy',name_long='!![en]Privacy email', static=True, dtype='T')
        tbl.formulaColumn('fullname',select=dict(table='agz.staff',
                                                columns="""$name ||' '||$surname || '<br>' || coalesce($department ||' department <br>','') 
                            || coalesce('mob.: ' || $telephone || '<br>', '') || coalesce('email: ' || $email || '<br>' , '') 
                            || coalesce($note,'') """,
                                                where='$user_id =:env_user_id',
                                                dtype='T',name_long='!![en]fullname'))
        tbl.aliasColumn('agency_fullstyle','@port.@portag_unlocode.fullstyle')
        tbl.aliasColumn('vessel_name','@imbarcazione_id.nome')

    def defaultValues(self):
        return dict(port=self.db.currentEnv.get('current_port'))
        
    def pyColumn_privacy(self,record,field):
        privacy_email = self.db.application.getPreference('privacy_email',pkg='shipsteps')
        return privacy_email        
    
   