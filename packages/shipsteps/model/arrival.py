# encoding: utf-8
from datetime import datetime


class Table(object):
    def config_db(self,pkg):
        
        tbl=pkg.table('arrival', pkey='id', name_long='!![en]Arrival', name_plural='!![en]Arrivals',
                                 caption_field='arrival_data')
        self.sysFields(tbl,counter=True)
        #tolto la colonna agency_id perchè inserita nel package agz con la customizzazione di shipsteps
        #tbl.column('agency_id',size='22',name_long='!![en]Agency').relation(
        #                            'agz.agency.id',relation_name='agency_id_name', mode='foreignkey', onDelete='raise')
        tbl.column('reference_num',name_long='!![en]Reference number')
        tbl.column('date',dtype='D',name_long='!![en]Date')
        tbl.column('pfda_id',size='22',name_short='!![en]Pfda no.').relation('pfda.proforma.id',relation_name='pfda_arr', mode='foreignkey', onDelete='raise')
        tbl.column('vessel_details_id',size='22',name_long='!![en]Vessel',validate_notnull=True).relation(
                                    'vessel_details.id',relation_name='vessel_details_name', mode='foreignkey', onDelete='raise')
        tbl.column('visit_id',dtype='T',name_short='Visit ID')
        tbl.column('eta', dtype='DH', name_short='!![en]ETA')
        tbl.column('etb', dtype='DH', name_short='!![en]ETB')
        tbl.column('et_start', dtype='DH', name_short='!![en]ET start')
        tbl.column('etc', dtype='DH', name_short='!![en]ETC')
        tbl.column('ets', dtype='DH', name_short='!![en]ETS')
        tbl.column('draft_aft_arr', dtype='N',size='10,2', name_short='!![en]AFT draft arr.', format='#,###.00')
        tbl.column('draft_fw_arr', dtype='N',size='10,2', name_short='!![en]FW draft arr.', format='#,###.00')
        tbl.column('draft_aft_dep', dtype='N',size='10,2', name_short='!![en]AFT draft dep.', format='#,###.00')
        tbl.column('draft_fw_dep', dtype='N',size='10,2', name_short='!![en]FW draft dep', format='#,###.00')
        tbl.column('mandatory', name_short='!![en]Mandatory')
        tbl.column('dock_id',size='22', name_long='!![en]Dock'
                    ).relation('dock.id', relation_name='dock_id_arr', mode='foreignkey', onDelete='raise')
        tbl.column('info_moor', name_short='!![en]Moor info')
        tbl.column('master_name', name_short='!![en]Master name')
        tbl.column('n_crew', dtype='N',name_short='!![en]Crew no.')
        tbl.column('n_passengers', dtype='N',name_short='!![en]Passengers no.')
        tbl.column('last_port',size='22',name_short='!![en]Last port').relation('unlocode.place.id',relation_name='lastport_arr', mode='foreignkey', onDelete='raise')
        tbl.column('departure_lp', dtype='DH', name_short='!![en]Departure last port')
        tbl.column('next_port',size='22',name_short='!![en]Next port').relation('unlocode.place.id',relation_name='nextport_arr', mode='foreignkey', onDelete='raise')
        tbl.column('eta_np', dtype='DH', name_short='!![en]ETA next port')
        tbl.column('voy_n', name_short='!![en]Voy no.')
        tbl.column('cargo_dest', name_short='!![en]Cargo destination')
        tbl.column('invoice_det_id',size='22', name_long='!![en]Invoicing'
                    ).relation('invoice_det.id', relation_name='invoicing_arr', mode='foreignkey', onDelete='raise')
        tbl.column('cargo_onboard', name_short='!![en]Cargo on board')
        tbl.column('extra_cargo_onboard', name_short='!![en]Extra descr. Cargo on board')
        tbl.column('cargo_onboard_dep', name_short='!![en]Cargo on board')
        tbl.column('extra_cargo_onboard_dep', name_short='!![en]Extra descr. Cargo on board')
        tbl.column('transit_cargo', name_short='!![en]Transit Cargo')
        tbl.column('extra_transit_cargo', name_short='!![en]Extra descr. Transit Cargo')
        tbl.column('nsis_prot', name_short='Nsis prot.')
        tbl.column('firma_div', name_short='!![en]Different signature agency')
        tbl.column('note', name_short='!![en]note')
        tbl.column('tip_mov',name_short='!![en]Tip.Mov.', batch_assign=True
                    ).relation('tip_mov.code', relation_name='ship_mov', mode='foreignkey', onDelete='raise')
        tbl.column('movtype_id',size='22',name_short='!![en]Mov. Type', batch_assign=dict(hasDownArrow=True)
                    ).relation('mov_type.id', relation_name='movtype', mode='foreignkey', onDelete='raise')
        tbl.column('vessel_stamp', dtype='P', name_long='!![en]Vessel Stamp')
        tbl.column('ctm', dtype='N', name_short='ctm')
        tbl.column('date_ctm', dtype='D', name_short='date ctm')
        tbl.column('p_sanimare', dtype='B', name_short='!![en]Sanimare pratique')       
        #tbl.formulaColumn('cargoboard',select=dict(table='shipsteps.cargo_transit', columns='SUM($description)', where='$arrival_id=#THIS.id'), dtype='T',name_long='cargo on board')
        tbl.pyColumn('cargo',name_long='!![en]Cargo', static=True)
        #tbl.pyColumn('email_arr_to',name_long='!![en]Email arrival to', static=True)
        #tbl.pyColumn('email_arr_cc',name_long='!![en]Email arrival cc', static=True)
        
        tbl.pyColumn('saluto',name_long='!![en]Greeting', static=True)
        tbl.pyColumn('datacorrente',name_long='!![en]Current date', static=True)
        tbl.pyColumn('sostanave',name_long='!![en]Sosta nave', static=True)
        #tbl.pyColumn('logocc',name_long='!![en]Logo CC', static=True, dtype='P')
        #tbl.pyColumn('logocp',name_long='!![en]Logo CP', static=True, dtype='P')
        tbl.pyColumn('privacy',name_long='!![en]Privacy email', static=True, dtype='T')
        tbl.pyColumn('docbefore_cp', dtype='B')
        tbl.pyColumn('conv_ctm')
        tbl.pyColumn('uesan_pref',name_long='!![en]UE_San_pref',dtype='B')
       #tbl.aliasColumn('carico_a_bordo','@cargo_onboard_arr.carico_a_bordo')
        tbl.aliasColumn('n_tug_arr','@extradatacp.n_tug_arr')
        tbl.aliasColumn('n_tug_dep','@extradatacp.n_tug_dep')
        tbl.aliasColumn('caricoarrivo','@cargo_lu_arr.cargo_lu_en_ita',name_long='caricoarrivo')
        tbl.aliasColumn('chrtrs','@cargo_lu_arr.@charterers_id.name',name_long='Noleggiatore')
        tbl.aliasColumn('carico_arr','@cargo_lu_arr.cargo_arr',name_long='Carico in arrivo')
        tbl.aliasColumn('cargo_descr','@cargo_lu_arr.cargo_descr',name_long='Descrizione Carico')
        tbl.aliasColumn('cargo_lu_en','@cargo_lu_arr.cargo_ship_rec',name_long='!![en]Cargo L/U')
        tbl.aliasColumn('cargo_op','@cargo_lu_arr.operation')
        tbl.aliasColumn('ship_rec','@cargo_lu_arr.ship_rec',name_long='!![en]Shipper/Receivers')
        tbl.aliasColumn('tot_cargo','@cargo_lu_arr.tot_cargo')#,name_long='!![en]Cargo total')
        tbl.aliasColumn('lastport','@last_port.citta_nazione', name_long='!![en]Last port')
        tbl.aliasColumn('nextport','@next_port.citta_nazione', name_long='!![en]Next port')
        tbl.aliasColumn('owners','@vessel_details_id.@owner_id.own_fullname', name_long='!![en]Owners full name')
        tbl.aliasColumn('ship_or_rec','@cargo_lu_arr.ship_or_rec', name_long='!![en]Ship or Rec')
        tbl.aliasColumn('shiprec','@cargo_lu_arr.shiprec', name_long='!![en]ShipRec')
        tbl.aliasColumn('workport','@agency_id.@port.citta_nazione')
        tbl.aliasColumn('email_account_id','@agency_id.@user.email_account_id')
        #tbl.aliasColumn('email_int_arr','@arrival_email.email_int')
        tbl.aliasColumn('email_int_sof','@sof_arr.@sof_email.email_int')
        tbl.aliasColumn('sailed','@time_arr.sailed')
        tbl.aliasColumn('vesselname','@vessel_details_id.vessel_name')
        tbl.aliasColumn('flag','@vessel_details_id.@imbarcazione_id.@flag.codename')
        tbl.aliasColumn('tsl','@vessel_details_id.tsl')
        tbl.aliasColumn('imo','@vessel_details_id.imo')
        tbl.aliasColumn('time_gate','@agency_id.@agency_sh_gate.details',dtype='T')
        tbl.aliasColumn('map_gate','@agency_id.@agency_sh_gate.map',dtype='P')
        tbl.aliasColumn('timearr_log','@time_arr.time_arr')
        tbl.aliasColumn('timearr2_log','@time_arr.time_arr_2')
        tbl.aliasColumn('movement_type','@movtype_id.@movtype_check.description')
        tbl.formulaColumn('portlog_timearr',"""CASE WHEN $timearr_log !='' THEN 'PORTLOG<br>------------------------------<br>' || coalesce($timearr_log,'') || coalesce($timearr2_log ,'') END""")
        tbl.formulaColumn('rifiuti_conf', """' - ' || @garbage_arr.@garbage.@tip_garbage_id.description || ' - ' || @garbage_arr.@garbage.measure || ' ' || @garbage_arr.@garbage.quantity""",dtype='T',name_long='Rifiuti da conferire')
        tbl.formulaColumn('etb_date','$etb',dtype='D')
        tbl.formulaColumn('fullstyle_forrec',"""CASE WHEN $firma_div IS NULL OR $firma_div = '' THEN @agency_id.fullstyle 
                                                 ELSE $firma_div END""", dtype='T')
        tbl.formulaColumn('protfald', """@prot_arr.prot_n || coalesce(' Fald.' || @prot_arr.@fald_n.numero,'')""",dtype='T',name_long='Prot.Fald.')
        tbl.formulaColumn('logo_cp',select=dict(table='shipsteps.loghi', columns="$logo_cp",
                                                    where='$agency_id=#THIS.agency_id'), dtype='P')
        tbl.formulaColumn('ets_emaildep',"""CASE WHEN $sailed IS NULL THEN :etsed || to_char($ets, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',
                            var_etsed='<br>EXPECTED TIMES<br>------------------------------<br>ETS:...........',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('eta_email',"""CASE WHEN @time_arr.aor IS NULL AND $eta IS NOT NULL THEN :etadescr || to_char($eta, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etadescr='ETA:...........',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('etb_email',"""CASE WHEN @time_arr.moored IS NULL AND $etb IS NOT NULL THEN :etbdescr || to_char($etb, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etbdescr='ETB:...........',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('etstart_email',"""CASE WHEN @sof_arr.ops_commenced IS NULL AND $et_start IS NOT NULL THEN :etstdescr || to_char($et_start, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etstdescr='ET Start ops:..',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('etc_email',"""CASE WHEN $etc IS NOT NULL THEN :etcdescr || to_char($etc, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etcdescr='ETC:...........',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('ets_email',"""CASE WHEN $ets IS NOT NULL THEN :etsdescr || to_char($ets, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etsdescr='ETS:...........',var_df='DD/MM/YYYY HH24:MI')

       #tbl.formulaColumn('eta_email',"""CASE WHEN $eta IS NOT NULL THEN :etadescr || to_char($eta, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etadescr='ETA:...........',var_df='DD/MM/YYYY HH24:MI')
       #tbl.formulaColumn('etb_email',"""CASE WHEN $etb IS NOT NULL THEN :etbdescr || to_char($etb, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etbdescr='ETB:...........',var_df='DD/MM/YYYY HH24:MI')
       #tbl.formulaColumn('etstart_email',"""CASE WHEN $et_start IS NOT NULL THEN :etstdescr || to_char($et_start, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etstdescr='ET Start ops:..',var_df='DD/MM/YYYY HH24:MI')
       #tbl.formulaColumn('etc_email',"""CASE WHEN $etc IS NOT NULL THEN :etcdescr || to_char($etc, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etcdescr='ETC:...........',var_df='DD/MM/YYYY HH24:MI')
       #tbl.formulaColumn('ets_email',"""CASE WHEN $ets IS NOT NULL THEN :etsdescr || to_char($ets, :df) || ' WP/AGW<br>' ELSE '' END""", dtype='T',var_etsdescr='ETS:...........',var_df='DD/MM/YYYY HH24:MI')

        tbl.formulaColumn('arrival_data',"$reference_num || ' - ' || @vessel_details_id.@imbarcazione_id.nome || coalesce(' - ' || $visit_id,'') || coalesce(' - ' || to_char($etb,:df),'')", dtype='T',var_df='DD/MM/YYYY', static=True)    
        tbl.formulaColumn('prox_port', """CASE WHEN $nextport = 'ORDER - ORDINI' THEN '' ELSE $nextport END""" )
        tbl.formulaColumn('totcargo', select=dict(table='shipsteps.cargo_unl_load',
                                                columns="""@measure_id.description || ' ' || SUM($quantity) """,
                                                where='$arrival_id=#THIS.id', group_by='@measure_id.description'),
                                    dtype='N',name_long='Tot_Carico')
        tbl.formulaColumn('port_log_time',"""CASE WHEN $timearr_log !='' THEN 'PORTLOG<br>------------------------------<br>' || coalesce($timearr_log,'') || coalesce($timearr2_log ,'') END""")
        
        #formule column per email servizi
        tbl.formulaColumn('cp_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='capitaneria'),
                                                limit=1,dtype='T')
        tbl.formulaColumn('cp_intnsw',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='capitaneria_nsw'),
                                                dtype='T')
        tbl.formulaColumn('dog_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='dogana'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('dog_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='dogana'),
                                                dtype='T')
        tbl.formulaColumn('dog_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='dogana'),
                                                dtype='T')                                               
        tbl.formulaColumn('gdfroan_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='gdf roan'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('gdfroan_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gdf roan'),
                                                dtype='T')
        tbl.formulaColumn('gdfroan_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gdf roan'),
                                                dtype='T')
        tbl.formulaColumn('gdf_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='gdf'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('gdf_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gdf'),
                                                dtype='T')
        tbl.formulaColumn('gdf_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gdf'),
                                                dtype='T')
        tbl.formulaColumn('immigration_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='immigration'),
                                                limit=1,dtype='T')
        tbl.formulaColumn('immigration_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='immigration'),
                                                dtype='T')
        tbl.formulaColumn('immigration_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='immigration'),
                                                dtype='T')
        tbl.formulaColumn('usma_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='sanimare'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('usma_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='sanimare'),
                                                dtype='T')
        tbl.formulaColumn('usma_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='sanimare'),
                                                dtype='T')
        tbl.formulaColumn('pilot_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='pilot'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('pilot_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='pilot'),
                                                dtype='T')
        tbl.formulaColumn('pilot_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='pilot'),
                                                dtype='T')
        tbl.formulaColumn('moor_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='mooringmen'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('moor_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='mooringmen'),
                                                dtype='T')
        tbl.formulaColumn('moor_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='mooringmen'),
                                                dtype='T')
        tbl.formulaColumn('tug_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='tug'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('tug_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='tug'),
                                                dtype='T')
        tbl.formulaColumn('tug_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='tug'),
                                                dtype='T')
        tbl.formulaColumn('garbage_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, 
                                                serv='garbage',limit=1),
                                                dtype='T', static=True)
        tbl.formulaColumn('garbage_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='garbage'),
                                                limit=1,dtype='T')
        tbl.formulaColumn('garbage_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='garbage'),
                                                limit=1,dtype='T')
        tbl.formulaColumn('chemist_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='chemist'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('chemist_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='chemist'),
                                                dtype='T')
        tbl.formulaColumn('chemist_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='chemist'),
                                                dtype='T')
        tbl.formulaColumn('water_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='water supply'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('water_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='water supply'),
                                                dtype='T')
        tbl.formulaColumn('water_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='water supply'),
                                                dtype='T')
        tbl.formulaColumn('antifire_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='antifire'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('antifire_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='antifire'),
                                                dtype='T')
        tbl.formulaColumn('antifire_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='antifire'),
                                                dtype='T')
        tbl.formulaColumn('ens_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='ens'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('ens_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='ens'),
                                                dtype='T')
        tbl.formulaColumn('ens_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='ens'),
                                                dtype='T')
        tbl.formulaColumn('gpg_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='gpg'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('gpg_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gpg'),
                                                dtype='T')
        tbl.formulaColumn('gpg_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='gpg'),
                                                dtype='T')
        tbl.formulaColumn('pfso_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='pfso'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('pfso_email',select=dict(table='shipsteps.email_services',
                                                columns='$email',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='pfso'),
                                                dtype='T')
        tbl.formulaColumn('pfso_email_cc',select=dict(table='shipsteps.email_services',
                                                columns='$email_cc',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id', serv='pfso'),
                                                dtype='T')
        tbl.formulaColumn('adsp_int',select=dict(table='shipsteps.email_services',
                                                columns='$consignee',
                                                where='$service_for_email=:serv AND $agency_id=#THIS.agency_id AND $default=:df', df=True, serv='adsp'),
                                                limit=1, dtype='T')
        tbl.formulaColumn('email_arr_to',select=dict(table='shipsteps.email_arr', columns="""string_agg($dest || ' ' || $description || '<br>','')""",
                                                    where='$arrival_id=#THIS.id and $dest=:to',to='to', limit=1,ignoreMissing=True))
        tbl.formulaColumn('email_arr_cc',select=dict(table='shipsteps.email_arr', columns="""string_agg($dest || ' ' || $description ||'<br>','')""",
                                                    where='$arrival_id=#THIS.id and $dest=:to',to='cc', limit=1,ignoreMissing=True))                                                    
        #formulaColumn per verificare se la data di partenza sia minore della data attuale e il form partenza nave per la finanza nopn è ancora stato stampato
        #riceviamo un msg di testo che andremo a lanciare con un data controller quando apriamo gli arrivi
        tbl.formulaColumn('gdfdep_timeexp',"""CASE WHEN @time_arr.sailed < NOW() AND @arr_tasklist.form_gdfdep IS NULL OR @arr_tasklist.form_gdfdep = false 
                                            THEN true END""", dtype='B')               
        tbl.formulaColumn('refcode',"'%%' || $reference_num || '%%'",dtype='T')

    #pycolumn creata per verificare tramite le preferenze del pkg shipsteps se abilitare o no le pratiche sanimare alle provenienze navi da tutti gli stati
    # o solo quelli extra ue o se viene flaggato nell'arrivo pratica sanimare. Nella th_arrival di shipsteps ho inserito nei widget sanimare della task list la 
    # variabile hidden che verifica il valore uesan_pref in caso di valore true nasconde il widget 
    def pyColumn_uesan_pref(self, record, field):
        pref=self.db.application.getPreference('ue',pkg='shipsteps')
        movtype=record['@movtype_id.hierarchical_descrizione']
        p_sanimare=record['p_sanimare']
        lastport=record['last_port']
        code = self.db.table('unlocode.place').readColumns(columns="""nazione_code""",
                                                                where="$id=:lp", lp=lastport) 
        
        if pref is False:
            uesan=self.db.table('unlocode.nazione').readColumns(columns="""CASE WHEN $ue is True THEN true ELSE false END""",
                                                                where="$code=:code", code=code)
            #if movtype == 'Passengers/ONG' and uesan is True:
            if p_sanimare is True and uesan is True:    
                uesan = False  
                  
        else:
            uesan = self.db.table('unlocode.nazione').readColumns(columns="""CASE WHEN $ue is True THEN false ELSE false END""",
                                                                where="$code=:code", code=code)  
        
        return uesan
    
    def pyColumn_cargo(self,record,field):
       
        pkey=record['id']
        carico = self.db.table('shipsteps.cargo_unl_load').query(columns="""CASE WHEN $operation = 'L' THEN 'Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description  
                                            WHEN $operation = 'U' THEN 'Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description ELSE 'NIL' END """,
                                                                    where='$arrival_id=:a_id',
                                                                    a_id=pkey).fetch()                                    
        
        n_car = len(carico) 
        cargo=''                                                               
        for r in range (n_car):
            cargo += ' - ' + str(carico[r][0]) + '<br>'

        return cargo
    
    #con la pyColumn ci facciamo restituire il valore True se il tipo di movimentazione è diverso da quello alimentare e nelle preference è attivo 
    #la disabilitazione del pmou - nella form arrival al fine di avere il valore della virtual column disponibile abbiamo inserito form.store.handler('load',virtual_columns='$workport,$docbefore_cp')
    #così abbiamo attribuito il valore hiden alla div che visualizza nella tasklist DOC BEFORE VESSEL ARRIVAL
    def pyColumn_docbefore_cp(self,record,field):
        pkey=record['id']
        tbl_arrival=self.db.table('shipsteps.arrival')
        code=tbl_arrival.readColumns(columns="@movtype_id.hierarchical_descrizione", where="$id=:id_arr",id_arr=pkey)
        pmou = self.db.application.getPreference('pmou',pkg='shipsteps') 
        
        if code != 'Alimentary/UE' and code != 'Alimentary' and pmou==True:
            result = True
        else:
            result = False    
        return result
       
    #def pyColumn_email_arr_to(self,record,field):
    #    
    #    pkey=record['pkey']
    #    email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$arrival_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='to').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += email_dest[r][0] + '<br>'
    #    return email_int
    #
    #def pyColumn_email_arr_cc(self,record,field):
    #    
    #    pkey=record['pkey']
    #    email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$arrival_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='cc').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += email_dest[r][0] + '<br>'
    #    return email_int

    def pyColumn_saluto(self,record,field):
        
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno'  
        elif cur_time < '17:00:00':
            sal='Buon pomeriggio'
        elif cur_time < '24:00:00':
            sal = 'Buonasera'    
        elif cur_time < '04:00:00':
            sal = 'Buona notte'      
        return sal
    
    def pyColumn_datacorrente(self,record,field):
        data_lavoro=self.db.workdate   
        return data_lavoro
    
    def pyColumn_sostanave(self,record,field):
        pkey=record['id']
        moored = self.db.table('shipsteps.arrival_time').readColumns(columns='$moored', where='$arrival_id=:a_id', a_id=pkey)
        if moored is None:
            return 'no moored time'

        ets = record['ets']
        if ets is not None:
            tempo_trascorso = ets - moored
            days=divmod(tempo_trascorso.total_seconds(), 86400)[0]
            hours=divmod(tempo_trascorso.total_seconds(), 3600)[0]
            minutes=divmod(tempo_trascorso.total_seconds(), 60)[0]
            tot_hours = hours-(days*24)
            remain_minutes=((minutes*60)-((days*86400)+(tot_hours*3600)))/60
            sosta=str(days) + ' giorni, ' + str(tot_hours) + ' ore, ' + str(remain_minutes) + ' minuti'
            return sosta    

    def pyColumn_conv_ctm(self,record,field):
        self.ones = ["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine ", "ten ", "eleven ",
                "twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]

        self.twenties = ["", "", "twenty ", "thirty ", "forty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]

        self.thousands = ["", "thousand ", "million ", "billion ", "trillion ", "quadrillion ", "quintillion ", "sextillion ",
             "septillion ", "octillion ", "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ",
             "quattuordecillion ", "quindecillion", "sexdecillion ", "septendecillion ", "octodecillion ",
             "novemdecillion ", "vigintillion "]
        pkey=record['id']
        tbl_arrival=self.db.table('shipsteps.arrival')
        n=tbl_arrival.readColumns(columns="$ctm", where="$id=:id_arr",id_arr=pkey)
        
        cash_word = self.num2word(n)
        return cash_word

    def num999(self,n):
        c = n % 10  # singles digit
        b = ((n % 100) - c) / 10  # tens digit
        a = ((n % 1000) - (b * 10) - c) / 100  # hundreds digit
        t = ""
        h = ""
        if a != 0 and b == 0 and c == 0:
            t = self.ones[int(a)] + "hundred "
        elif a != 0:
            t = self.ones[int(a)] + "hundred and "
        if b <= 1:
            h = self.ones[n % 100]
        elif b > 1:
            h = self.twenties[int(b)] + self.ones[int(c)]
        st = t + h
        return st


    def num2word(self,num):
        if num == 0: return 'zero'

        i = 3
        n = str(num)
        word = ""
        k = 0
        while (i == 3):
            nw = n[-i:]
            n = n[:-i]
            if int(nw) == 0:
                word = self.num999(int(nw)) + self.thousands[int(nw)] + word
            else:
                word = self.num999(int(nw)) + self.thousands[k] + word
            if n == '':
                i = i + 1
            k += 1
        return word[:-1]
    
    #def pyColumn_logocc(self,record,field):
    #    logocc = self.db.application.getPreference('logo_cc',pkg='shipsteps')
    #    return logocc

    #def pyColumn_logocp(self,record,field):
    #    logocp = self.db.application.getPreference('logo_cp',pkg='shipsteps')
    #    return logocp

    def pyColumn_privacy(self,record,field):
        privacy_email = self.db.application.getPreference('privacy_email',pkg='shipsteps')
        return privacy_email    

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),date = self.db.workdate)


   #def defaultValues(self):
   #     return dict(date = self.db.workdate)

    def counter_reference_num(self,record=None):
        #2021/000001
        tbl_agency = self.db.table('agz.agency')
        codice = tbl_agency.readColumns(columns='$code', where = '$id =:ag_id', ag_id=record['agency_id'])
        return dict(format='$K$YYYY/$NNNNNN', code=codice, period='YYYY', date_field='date', showOnLoad=True, date_tolerant=True, recycle=True)

    def randomValues(self):
        return dict(date = dict(sorted=True))

   #def menu_dynamicMenuContent_prova(self,**kwargs):
   #    return self.query(where="""EXTRACT(month from  $date) =:this_month""",this_month=self.db.workdate.month).fetch()
    
    # alla duplicazione del record andiamo a passare i valori nulli che non devono essere duplicati
    def onDuplicating(self,record):
        record['reference_num'] = None
        record['date'] = self.db.workdate
        record['pfda_id'] = None
        record['visit_id'] = None
        record['eta'] = None
        record['etb'] = None
        record['et_start'] = None
        record['etc'] = None
        record['ets'] = None
        record['master_name'] = None
        record['departure_lp'] = None
        record['eta_np'] = None
        record['cargo_onboard'] = None
        record['extra_cargo_onboard'] = None
        record['cargo_onboard_dep'] = None
        record['extra_cargo_onboard_dep'] = None
        record['transit_cargo'] = None
        record['extra_transit_cargo'] = None
        record['info_moor'] = None
        record['voy_n'] = None
        record['nsis_prot'] = None
        record['note'] = None
        record['vessel_stamp'] = None
        