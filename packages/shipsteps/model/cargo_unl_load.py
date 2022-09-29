# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cargo_unl_load', pkey='id', name_long='!![en]Cargo unloding/loading', 
                        name_plural='!![en]Cargoes unloding/loading',caption_field='cargo_arr', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='cargo_lu_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('bln', size=':5', name_short='BL no.')
        tbl.column('shipper_id',size='22', name_long='!![en]Shippers'
                    ).relation('ship_rec.id', relation_name='cargo_lu_ship', mode='foreignkey', onDelete='raise')
        tbl.column('receiver_id',size='22', name_long='!![en]Receivers'
                    ).relation('ship_rec.id', relation_name='cargo_lu_rec', mode='foreignkey', onDelete='raise')
        tbl.column('charterers_id',size='22', name_long='!![en]Charterers'
                    ).relation('charterers.id', relation_name='chart_cargo', mode='foreignkey', onDelete='raise')
        tbl.column('quantity', dtype='N', size='10,3', name_short='!![en]Quantity', format='#,###.000')
        tbl.column('measure_id',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='cargo_lu_measure', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('description_it', name_short='!![en]Description IT')
        tbl.column('extra_description_cp', name_short='!![en]Extra Description CP')
        tbl.column('operation', name_short='operation', values='U:Unloading,L:Loading')
        tbl.column('foreign_cargo', dtype='T', name_short='!![en]Foreign cargo')
        tbl.column('place_origin_goods',size='22',name_short='!![en]Place origin goods').relation('unlocode.place.id',
                                            relation_name='origingoods', mode='foreignkey', onDelete='raise')
        tbl.column('place_dest_goods',size='22',name_short='!![en]Place destination goods').relation('unlocode.place.id',
                                            relation_name='destgoods', mode='foreignkey', onDelete='raise') 
        tbl.aliasColumn('lastport','@arrival_id.@last_port.citta_nazione', name_long='!![en]Last port')
        tbl.aliasColumn('nextport','@arrival_id.@next_port.citta_nazione', name_long='!![en]Next port')
        
        tbl.formulaColumn('cargo_arr',"'-' || COALESCE(@measure_id.description,'') || ' ' || COALESCE($quantity,0) || ' ' || COALESCE($description || '<br>','') ")
        tbl.formulaColumn('cargo_lu_en', """CASE WHEN $operation = 'L' THEN '-Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' 
                                            WHEN $operation = 'U' THEN '-Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' ELSE 'NIL' END """,
                            dtype='T', name_long='Carico L/U')
        tbl.formulaColumn('cargo_descr', """CASE WHEN $operation = 'L' THEN '-Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || ' - Shippers: ' || @shipper_id.name || ' - ' 
                                            WHEN $operation = 'U' THEN '-Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description || ' - Receivers: ' || @receiver_id.name || ' - ' ELSE 'NIL' END """,
                            dtype='T', name_long='Carico L/U shiprec')
        tbl.formulaColumn('cargo_sof', """CASE WHEN $operation = 'L' THEN '-Loading cargo: ' || coalesce('BL no.' || $bln, '') || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' 
                                            WHEN $operation = 'U' THEN '-Unloading cargo: ' || coalesce('BL no.' || $bln, '') || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' ELSE 'NIL' END """,
                            dtype='T', name_long='Carico Sof')
        tbl.formulaColumn('cargo_lu_en_ita', """CASE WHEN $operation = 'L' THEN '-Carico da imbarcare / Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description_it || '<br>' 
                                            WHEN $operation = 'U' THEN '-Carico da sbarcare / Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description_it || '<br>' ELSE 'Nessun carico da movimentare' END """,
                            dtype='T', name_long='Carico L/U ITA')
        tbl.formulaColumn('ship_rec', "coalesce('s: '|| @shipper_id.name,'') || coalesce(' - r: ' || @receiver_id.name,'')")
        tbl.formulaColumn('ship_or_rec', """CASE WHEN $operation = 'L' THEN 'Shipper/Caricatore: ' || @shipper_id.name WHEN $operation = 'U' THEN 'Receiver/Ricevitore: ' || @receiver_id.name ELSE '' END """,
                                        dtype='T', name_long='Ship or Rec')
        tbl.formulaColumn('tot_cargo',select=dict(table='shipsteps.cargo_unl_load',
                                                columns='SUM($quantity)',
                                                where='$id=#THIS.id'),
                                    dtype='N',name_long='!![en]Cargo total', format='#,###.000')
        tbl.formulaColumn('cargo_ship_rec', """CASE WHEN $operation = 'L' THEN '-Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br> Shippers: ' || @shipper_id.name || '<br>' 
                                            WHEN $operation = 'U' THEN '-Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br> Receivers: ' || @receiver_id.name || '<br>' ELSE 'NIL' END """,
                            dtype='T', name_long='Carico L/U shiprec')
        tbl.formulaColumn('tip_cargo_dogana',"""CASE WHEN $foreign_cargo = 'True' THEN 'Merce estera da importare'
                                                WHEN $foreign_cargo = 'False' THEN 'Merce scortata da T2L' ELSE '' END""")
        
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')