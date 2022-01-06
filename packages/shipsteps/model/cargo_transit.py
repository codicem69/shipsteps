# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cargo_transit', pkey='id', name_long='!![en]Transit cargo', name_plural='!![en]Transit cargoes',caption_field='description')
        self.sysFields(tbl)
        
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='cargo_transit_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('quantity', dtype='N', size='10,3', name_short='Quantity', format=',format=#,###.000')
        tbl.column('measure_id',size='22', name_long='measure'
                    ).relation('measure.id', relation_name='cargo_transit_measure', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        tbl.formulaColumn('transit_cargo',"""coalesce(@measure_id.description, '') || ' ' || coalesce(CAST($quantity AS TEXT),'') || ' ' || coalesce($description,'')""", name_long='!![en]Transit cargo')