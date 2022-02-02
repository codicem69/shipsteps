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
        tbl.column('quantity', dtype='N', size='10,3', name_short='!![en]Quantity', format='#,###.000')
        tbl.column('measure_id',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='cargo_lu_measure', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('description_it', name_short='!![en]Description IT')
        tbl.column('operation', name_short='operation', values='U:Unloading,L:Loading')
        tbl.column('foreign_cargo', dtype='B', name_short='!![en]Foreign cargo')
        tbl.formulaColumn('cargo_arr',"'-' || COALESCE(@measure_id.description,'') || ' ' || COALESCE($quantity,0) || ' ' || COALESCE($description,'') || '<br>'")
        tbl.formulaColumn('cargo_lu_en', """CASE WHEN $operation = 'L' THEN '-Loading cargo: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' 
                                            WHEN $operation = 'U' THEN '-Unloading cargo: ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' ELSE 'NIL' END """,
                            dtype='T', name_long='Carico L/U')
        tbl.formulaColumn('ship_rec', "'s: '|| @shipper_id.name || ' - r: ' || @receiver_id.name")
        tbl.formulaColumn('tot_cargo',select=dict(table='shipsteps.cargo_unl_load',
                                                columns='SUM($quantity)',
                                                where='$id=#THIS.id'),
                                    dtype='N',name_long='!![en]Cargo total', format='#,###.000')

        tbl.aliasColumn('agency_id','@arrival_id.agency_id')