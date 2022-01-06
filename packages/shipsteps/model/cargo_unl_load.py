# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cargo_unl_load', pkey='id', name_long='!![en]Cargo unloding/loading', name_plural='!![en]Cargoes unloding/loading',caption_field='description')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='cargo_lu_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('shipper_id',size='22', name_long='!![en]Shippers'
                    ).relation('ship_rec.id', relation_name='cargo_lu_ship', mode='foreignkey', onDelete='raise')
        tbl.column('receiver_id',size='22', name_long='!![en]Receivers'
                    ).relation('ship_rec.id', relation_name='cargo_lu_rec', mode='foreignkey', onDelete='raise')
        tbl.column('quantity', dtype='N', size='10,3', name_short='Quantity', format='#,###.000')
        tbl.column('measure_id',size='22', name_long='measure'
                    ).relation('measure.id', relation_name='cargo_lu_measure', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('operation', name_short='operation', values='U:Unloading,L:Loading')
        tbl.column('foreign_cargo', dtype='B', name_short='!![en]Foreign cargo')
        tbl.formulaColumn('cargo_arr',"'-' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>'")
        tbl.formulaColumn('cargo_onboard', """CASE WHEN $operation = 'L' THEN '-Loading cargo/carico da imbarcare: ' || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' 
                                            ELSE '-Unloading cargo/carico da sbarcare: ' || @measure_id.description || ' ' || $quantity || ' ' || $description || '<br>' END """,
                            dtype='T', name_long='Carico a bordo')
        tbl.formulaColumn('ship_rec', "'s: '|| @shipper_id.name || ' - r: ' || @receiver_id.name")
        tbl.formulaColumn('tot_cargo',select=dict(table='shipsteps.cargo_unl_load',
                                                columns='SUM($quantity)',
                                                where='$id=#THIS.id'),
                                    dtype='N',name_long='!![en]Cargo total', format='#,###.000')

        