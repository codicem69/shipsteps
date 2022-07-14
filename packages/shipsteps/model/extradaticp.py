from email.policy import default


class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('extradaticp', pkey='id', name_long='!![en]Extra data CP', name_plural='!![en]Extra data CP',
                                      caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='extradatacp', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('mot_appr',  name_short='Motivo approdo')
        tbl.column('lavori', name_short='Per lavori o altri motivi')
        tbl.column('notizie',  name_short='Altre notizie')
        tbl.column('pilot_arr', dtype='B', name_short='!![en]Pilot on arrival')
        tbl.column('pilot_arr_vhf', dtype='B', name_short='!![en]Pilot VHF on arrival')
        tbl.column('antifire_arr', dtype='B', name_short='!![en]Antifire on arrival')
        tbl.column('antipol_arr', dtype='B', name_short='!![en]Antipollution on arrival')
        tbl.column('moor_arr', dtype='B', name_short='!![en]Moor on arrival')
        tbl.column('n_moor_arr', name_short='!![en]No. moor on arrival')
        tbl.column('tug_arr', dtype='B', name_short='!![en]Tug on arrival')
        tbl.column('n_tug_arr', name_short='!![en]No. Tug on arrival')
        tbl.column('daywork', name_short='!![en]Days of work')
        tbl.column('timework',  name_short='!![en]Time work')
        tbl.column('pilot_dep', dtype='B', name_short='!![en]Pilot on departure')
        tbl.column('pilot_dep_vhf', dtype='B', name_short='!![en]Pilot VHF on departure')
        tbl.column('antifire_dep', dtype='B', name_short='!![en]Antifire on departure')
        tbl.column('antipol_dep', dtype='B', name_short='!![en]Antipollution on departure')
        tbl.column('moor_dep', dtype='B', name_short='!![en]Moor on departure')
        tbl.column('n_moor_dep', name_short='!![en]No. moor on departure')
        tbl.column('tug_dep', dtype='B', name_short='!![en]Tug on departure')
        tbl.column('n_tug_dep', name_short='!![en]No. Tug on departure')
        tbl.column('motivo_viaggio',  name_short='Motivo Viaggio')
        tbl.column('tipo_viaggio',  name_short='Tipo Viaggio')
        tbl.column('naz_cte', name_short='!![en]Master nationality')
        tbl.column('n_ita', dtype='N', name_short='!![en]Number of italian')
        tbl.column('n_com', dtype='N', name_short='!![en]Number of comunitary')
        tbl.column('n_excom', dtype='N', name_short='!![en]Number of extra comunitary')
        tbl.column('n_pax_dep', dtype='N', name_short='!![en]Pax onboard departure')
        tbl.column('n_pax_sba_imb', dtype='N', name_short='!![en]Pax Enbarked/disembarked')
        tbl.column('n_car_mcycle', dtype='N', name_short='!![en]Car/Motorcycle on board')
        tbl.column('n_carmcycle_imbsba', dtype='N', name_short='!![en]Car/Motorcycle load/unl')
        tbl.column('n_comm_veic', dtype='N', name_short='!![en]Commercial Vehicles onboard')
        tbl.column('n_commveic_imbsba', dtype='N', name_short='!![en]Commercial Vehicles load/unl')
        

        tbl.aliasColumn('agency_id','@arrival_id.agency_id')