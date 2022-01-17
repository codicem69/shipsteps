# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('arrival_det', pkey='id', name_long='!![en]Arrival details', name_plural='!![en]Arrival details',
                                     caption_field='id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='arr_details', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('draft_aft_arr', size=':15', name_short='!![en]Draft AFT arrival')
        tbl.column('draft_fw_arr', size=':15', name_short='!![en]Draft FW arrival')
        tbl.column('draft_aft_dep', size=':15', name_short='!![en]Draft AFT departure')
        tbl.column('draft_fw_dep', size=':15', name_short='!![en]Draft FW departure')
        tbl.column('tug_in', size=':2', name_short='!![en]TUG in')
        tbl.column('tug_out', size=':2', name_short='!![en]TUG out')
        tbl.column('ifo_arr', size=':15', name_short='!![en]IFO arrival')
        tbl.column('do_arr', size=':15', name_short='!![en]Diesel Oil arrival')
        tbl.column('lo_arr', size=':15', name_short='!![en]Lub Oil arrival')
        tbl.column('fw_arr', size=':15', name_short='!![en]Fresh Water arrival')
        tbl.column('ifo_dep', size=':15', name_short='!![en]IFO departure')
        tbl.column('do_dep', size=':15', name_short='!![en]Diesel Oil departure')
        tbl.column('lo_dep', size=':15', name_short='!![en]Lub Oil departure')
        tbl.column('fw_dep', size=':15', name_short='!![en]Fresh Water departure')

    