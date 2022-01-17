# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof_cargo', pkey='id', name_long='sof_cargo', name_plural='sof_cargo',caption_field='id')
        self.sysFields(tbl)

        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_cargo_sof', mode='foreignkey', onDelete='cascade')   
        tbl.column('cargo_unl_load_id',size='22', name_long='cargo_unl_load_id'
                    ).relation('cargo_unl_load.id', relation_name='cargo_sof', mode='foreignkey', onDelete='cascade')     
    
    