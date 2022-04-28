# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof_tanks', pkey='id', name_long='Sof tanks', name_plural='Sof tanks',caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_tanks', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('start_insp', dtype='DH', name_short='!![en]Inspection commenced')
        tbl.column('stop_insp', dtype='DH', name_short='!![en]Inspection completed')
        tbl.column('cargo_calc', dtype='DH', name_short='!![en]Cargo calculation')
        tbl.column('start_ullage', dtype='DH', name_short='!![en]Ullage commenced')
        tbl.column('stop_ullage', dtype='DH', name_short='!![en]Ullage completed')
        tbl.column('hose_conn', dtype='DH', name_short='!![en]Hoses connected')
        tbl.column('hose_disconn', dtype='DH', name_short='!![en]Hoses disconnected')
        tbl.column('average', size=':15', dtype='T', name_short='!![en]Average rate')
        tbl.aliasColumn('agency_id','@sof_id.@arrival_id.agency_id')

        tbl.formulaColumn('start_insp_txt', """CASE WHEN $start_insp is not null THEN 'Inspection commenced' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('stop_insp_txt', """CASE WHEN $stop_insp is not null THEN 'Inspection completed' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('cargo_calc_txt', """CASE WHEN $cargo_calc is not null THEN 'Cargo calculation' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('start_ullage_txt', """CASE WHEN $start_ullage is not null THEN 'Ullage commenced' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('stop_ullage_txt', """CASE WHEN $stop_ullage is not null THEN 'Ullage completed' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('hose_conn_txt', """CASE WHEN $hose_conn is not null THEN 'Hoses connected' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('hose_disconn_txt', """CASE WHEN $hose_disconn is not null THEN 'Hoses disconnected' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('average_txt', """CASE WHEN $average is not null THEN 'Average rate' ELSE '' END""", dtype='T')
        tbl.formulaColumn('startinsp_time', """CASE WHEN $start_insp is not null THEN to_char($start_insp, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('stopinsp_time', """CASE WHEN $stop_insp is not null THEN to_char($stop_insp, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('cargocalc_time', """CASE WHEN $cargo_calc is not null THEN to_char($cargo_calc, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('startullage_time', """CASE WHEN $start_ullage is not null THEN to_char($start_ullage, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('stopullage_time', """CASE WHEN $stop_ullage is not null THEN to_char($stop_ullage, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('hoseconn_time', """CASE WHEN $hose_conn is not null THEN to_char($hose_conn, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('hosedisconn_time', """CASE WHEN $hose_disconn is not null THEN to_char($hose_disconn, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('average_sof', """CASE WHEN $average is not null THEN $average || '<br>'  ELSE '' END""", dtype='T')