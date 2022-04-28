# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('arrival_time', pkey='id', name_long='!![en]arrival times', name_plural='!![en]arrival times',
                                      caption_field='aor', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='time_arr', mode='foreignkey', onDelete='cascade', one_one='*')   
        tbl.column('eosp', dtype='DH', name_short='!![en]End of sea passage')     
        tbl.column('aor', dtype='DH', name_short='!![en]Arrived on road')
        tbl.column('anchored', dtype='DH', name_short='!![en]Anchored')
        tbl.column('anchor_up', dtype='DH', name_short='!![en]Anchor up')
        tbl.column('pob', dtype='DH', name_short='!![en]Pilot on board')
        tbl.column('first_rope', dtype='DH', name_short='!![en]First rope')
        tbl.column('moored', dtype='DH', name_short='!![en]Moored')
        tbl.column('poff', dtype='DH', name_short='!![en]Pilot off')
        tbl.column('gangway', dtype='DH', name_short='!![en]Gangway in pos.')
        tbl.column('free_p', dtype='DH', name_short='!![en]Free pratique')
        tbl.column('pobd', dtype='DH', name_short='!![en]Pilot on board dep')
        tbl.column('last_line', dtype='DH', name_short='!![en]Last line')
        tbl.column('sailed', dtype='DH', name_short='!![en]Vessel sailed')
        tbl.column('cosp', dtype='DH', name_short='!![en]Commenced of sea pass')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
       # tbl.aliasColumn('time_from_sof','@arrival_id.@sof_arr.time_sof')
        tbl.formulaColumn('eosp_txt', """CASE WHEN $eosp is not null THEN 'Eosp' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('aor_txt', """CASE WHEN $aor is not null THEN 'Vessel arrived on road' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('anchored_txt', """CASE WHEN $anchored is not null THEN 'Anchored' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('anchor_up_txt', """CASE WHEN $anchor_up is not null THEN 'Anchor aweigh' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('pob_txt', """CASE WHEN $pob is not null THEN 'Pilot on board' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('first_rope_txt', """CASE WHEN $first_rope is not null THEN 'First rope' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('moored_txt', """CASE WHEN $moored is not null THEN 'All fast/moored' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('poff_txt', """CASE WHEN $poff is not null THEN 'Pilot off' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('gangway_txt', """CASE WHEN $gangway is not null THEN 'Gangway in position' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('free_p_txt', """CASE WHEN $free_p is not null THEN 'Free pratique reported' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('pobd_txt', """CASE WHEN $pobd is not null THEN 'Sailing pilot on board' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('last_line_txt', """CASE WHEN $last_line is not null THEN 'Last line' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('sailed_txt', """CASE WHEN $sailed is not null THEN 'Vessel unmoored/sailed' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('cosp_txt', """CASE WHEN $cosp is not null THEN 'Commenced of sea passage' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('eosp_time', """CASE WHEN $eosp is not null THEN to_char($eosp, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('aor_time', """CASE WHEN $aor is not null THEN to_char($aor, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('anchored_time', """CASE WHEN $anchored is not null THEN to_char($anchored, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('anchorup_time', """CASE WHEN $anchor_up is not null THEN to_char($anchor_up, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('pob_time', """CASE WHEN $pob is not null THEN to_char($pob, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('firstrope_time', """CASE WHEN $first_rope is not null THEN to_char($first_rope, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('moored_time', """CASE WHEN $moored is not null THEN to_char($moored, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('poff_time', """CASE WHEN $poff is not null THEN to_char($poff, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('gangway_time', """CASE WHEN $gangway is not null THEN to_char($gangway, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('freep_time', """CASE WHEN $free_p is not null THEN to_char($free_p, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('pobd_time', """CASE WHEN $pobd is not null THEN to_char($pobd, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('lastline_time', """CASE WHEN $last_line is not null THEN to_char($last_line, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('sailed_time', """CASE WHEN $sailed is not null THEN to_char($sailed, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')
        tbl.formulaColumn('cosp_time', """CASE WHEN $cosp is not null THEN to_char($cosp, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH:MI')

        tbl.formulaColumn('time_arr',"""coalesce('End of sea passage ' || to_char($eosp, :df),'') || '<br>' || coalesce('Arrived on road ' || to_char($aor, :df), '') || '<br>' ||
                                        coalesce('Anchored ' || to_char($anchored, :df),'') || '<br>' || coalesce('Anchor aweigh ' || to_char($anchor_up, :df),'') || '<br>' ||
                                        coalesce('Pilot on board ' || to_char($pob, :df),'') || '<br>' || coalesce('First rope ashore ' || to_char($first_rope, :df),'') || '<br>' ||
                                        coalesce('Moored ' || to_char($moored, :df),'') || '<br>' || coalesce('Pilot off ' || to_char($poff, :df), '') || '<br>' ||
                                        coalesce('Gangway in position ' || to_char($gangway, :df), '') || '<br>' || coalesce('Free pratique reported ' || to_char($free_p, :df), '') """,dtype='T',var_df='DD-MM-YYYY HH.MI')
        tbl.formulaColumn('time_arr_2',"""coalesce('Sailing pilot on board ' || to_char($pobd, :df), '') || '<br>' || coalesce('Last line ashore ' || to_char($last_line, :df),'') || '<br>' ||
                                          coalesce('Vessel sailed ' || to_char($sailed, :df),'') || '<br>' || coalesce('Commenced of sea passage ' || to_char($cosp, :df), '')""", dtype='T',var_df='DD-MM-YYYY HH.MI')
        