# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof', pkey='id', name_long='sof', name_plural='sof',caption_field='sof_det', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='sof_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('nor_tend', dtype='DH', name_short='!![en]NOR tendered')
        tbl.column('nor_rec', dtype='DH', name_short='!![en]NOR received')
        tbl.column('nor_acc', dtype='T', name_short='!![en]NOR accepted')
        tbl.column('ops_commenced', dtype='DH', name_short='!![en]Load/Unload commenced')
        tbl.column('ops_completed', dtype='DH', name_short='!![en]Load/Unload completed')
        tbl.column('doc_onboard', dtype='DH', name_short='!![en]Documents onboard')
        tbl.column('remarks_rs', name_short='!![en]Receivers / Shippers Remarks')
        tbl.column('remarks_cte', name_short='!![en]Master Remarks')
        tbl.column('note', name_short='!![en]Note SOF')
        tbl.column('onbehalf', name_short='!![en]On behalf')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('ship_rec','@sof_cargo_sof.ship_rec')
        tbl.aliasColumn('cargo_sof', '@sof_cargo_sof.@cargo_unl_load_id.cargo_sof',name_long='!![en]Cargo sof')
       # tbl.aliasColumn('carico_del_sof', '@sof_cargo_sof.carico_del_sof',name_long='!![en]Cargo on sof')
        tbl.aliasColumn('cargo_op', '@sof_cargo_sof.@cargo_unl_load_id.operation',name_long='!![en]Cago operation')
        tbl.aliasColumn('shiprec_sofcargo','@sof_cargo_sof.ship_rec')
        tbl.pyColumn('shiprec',name_long='!![en]Shipper or Receiver')
        tbl.pyColumn('shiprec_bl',name_long='!![en]Shipper or Receiver BL')
        tbl.pyColumn('carico_del_sof',name_long='!![en]Cargo on sof')
        tbl.pyColumn('email_sof_to',name_long='!![en]Email sof to', static=True)
        tbl.pyColumn('email_sof_cc',name_long='!![en]Email sof cc', static=True)
        tbl.pyColumn('email_arr_to',name_long='!![en]Email arrival to', static=True)
        tbl.pyColumn('email_arr_cc',name_long='!![en]Email arrival cc', static=True)
        #tbl.pyColumn('totcarico',name_long='!![en]Totcarico', static=True)
        tbl.formulaColumn('sof_det',"@arrival_id.reference_num || ' - ' || @arrival_id.date || ' - ' || @arrival_id.@vessel_details_id.@imbarcazione_id.nome")
        tbl.formulaColumn('nor_tend_txt', """CASE WHEN $nor_tend is not null THEN 'NOR tendered' ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_rec_txt', """CASE WHEN $nor_rec is not null THEN 'NOR received' ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_acc_txt', """CASE WHEN $nor_acc is not null THEN 'NOR acceppted' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_commenced_txt', """CASE WHEN $ops_commenced is not null AND $cargo_op = 'U' THEN 'Unloading commenced ' 
                                                  WHEN $ops_commenced is not null AND $cargo_op = 'L' THEN 'Loading commenced ' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_completed_txt', """CASE WHEN $ops_completed is not null AND $cargo_op = 'U' THEN 'Unloading completed ' 
                                                  WHEN $ops_completed is not null AND $cargo_op = 'L' THEN 'Loading completed ' ELSE '' END""", dtype='T')
        tbl.formulaColumn('doc_onboard_txt', """CASE WHEN $doc_onboard is not null THEN  :onboard END""",  dtype='T', var_onboard="cargo's documents on board")
        tbl.formulaColumn('note_txt', """CASE WHEN $note is not null THEN 'Notes' || '<br>'  ELSE '' END""", dtype='T')
        
        
        tbl.formulaColumn('time_sof', """coalesce('NOR tendered ' || to_char($nor_tend, :df), '') || '<br>' || coalesce('NOR received ' || to_char($nor_rec, :df),'') || '<br>' ||
                                         coalesce('NOR accepted ' || $nor_acc, '') || '<br>' || $ops_commenced_txt || to_char($ops_commenced, :df) || '<br>' || 
                                         $ops_completed_txt || to_char(ops_completed, :df) || '<br>' || coalesce(:onboard || to_char($doc_onboard,:df),'')""",var_onboard="Cargo's documents on board ",var_df='DD-MM-YYYY HH:MI')

    def pyColumn_carico_del_sof(self,record,field):
        p_key=record['id']
        #prepariamo i dati per la descrizione del carico con le relative BL e operazioni unloding/loading
        carico = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation,coalesce('BL no.' || @cargo_unl_load_id.bln,''), @cargo_unl_load_id.@measure_id.description, @cargo_unl_load_id.quantity,@cargo_unl_load_id.description",
                                                                where='sof_id=:sofid',sofid=p_key).fetch()
        cargo=''
        for c in range(len(carico)):
            if carico[c][0]== 'U':
                cargo += '- Unloading cargo: ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + ' ' + str(carico[c][4]) + '<br>'
            else:
                cargo += '- Loading cargo: ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + ' ' + str(carico[c][4]) + '<br>'
        
        #prepariamo i dati per il totale carico
        tot_carico = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation, @cargo_unl_load_id.@measure_id.description, SUM(@cargo_unl_load_id.quantity)",
                                                                where='sof_id=:sofid',sofid=p_key, group_by='@cargo_unl_load_id.@measure_id.description,@cargo_unl_load_id.operation').fetch()
        totale_carico=''
        for c in range(len(tot_carico)):
            if tot_carico[c][0]== 'U':
                totale_carico += '- Tot. unloading cargo: ' + str(tot_carico[c][1]) + ' ' + str(tot_carico[c][2]) + '<br>'
            else:
                totale_carico += '- Tot. loading cargo: ' + str(tot_carico[c][1]) + ' ' + str(tot_carico[c][2]) + '<br>' 
        
        #inseriamo in un unica variabile tutti i dati relativi al carico sopra calcolati
        descr_carico = cargo + '<br>' + totale_carico
        return descr_carico
    
    def pyColumn_shiprec_bl(self,record,field):
       
        p_key=record['id']
        #prepariamo i dati per associare Shipper e Receiver alle BL
        shiprec = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation,coalesce('BL no.' || @cargo_unl_load_id.bln,''),@cargo_unl_load_id.@shipper_id.name,@cargo_unl_load_id.@receiver_id.name",
                                                                where='sof_id=:sofid',sofid=p_key).fetch()
        ship_rec=''
        for c in range(len(shiprec)):
            if shiprec[c][0] == 'U':
                ship_rec += '- ' + shiprec[c][1] + ' Receiver: ' + shiprec[c][3] + '<br>'
            else:
                ship_rec += '- ' + shiprec[c][1] + ' Shipper: ' + shiprec[c][3] + '<br>'  
        return ship_rec

    def pyColumn_shiprec(self,record,field):
       
        p_key=record['id']
        #prepariamo i dati per associare Shipper e Receiver alle BL
        receiver = self.db.table('shipsteps.sof_cargo').query(columns="""CASE WHEN @cargo_unl_load_id.operation ='U' THEN 'Receiver: ' || 
                                                                        @cargo_unl_load_id.@receiver_id.name ELSE '' END""",
                                                                where='sof_id=:sofid', group_by='@cargo_unl_load_id.operation,@cargo_unl_load_id.@receiver_id.name',sofid=p_key).fetch()  
        shipper = self.db.table('shipsteps.sof_cargo').query(columns="""CASE WHEN @cargo_unl_load_id.operation ='L' THEN 'Shipper: ' || 
                                                                        @cargo_unl_load_id.@shipper_id.name ELSE '' END""",
                                                                where='sof_id=:sofid', group_by='@cargo_unl_load_id.operation,@cargo_unl_load_id.@shipper_id.name',sofid=p_key).fetch()                                                                  
        rec=''
        for c in range(len(receiver)):
            if receiver[c][0] is not '':
                rec += receiver[c][0] + '<br>'             
        ship=''
        for c in range(len(shipper)):
            if shipper[c][0] is not '':
                rec += shipper[c][0] + '<br>'
        ship_rec = rec + ship
        return ship_rec
        print(x) 
   #def pyColumn_carico_del_sof(self,record,field):
   #    
   #    #if not record['pkey']:
   #    p_key=record['id']
   #   # if not record['id']:
   #    #p_key=record['id']

   #    car_s=self.db.table('shipsteps.sof_cargo').query(where='$cargo_unl_load_id IS NOT NULL').fetchGrouped(key='sof_id')#fetch() 
   #    car_sof=car_s[p_key]
   #    cargo=''
   #    a=-1
   #    tot_l_cargo_mt=0
   #    tot_u_cargo_mt=0
   #    tot_l_cargo_kgs=0
   #    tot_u_cargo_kgs=0
   #    tot_l_cargo_ltrs=0
   #    tot_u_cargo_ltrs=0

   #    for c in car_sof:
   #        car=c['cargo_unl_load_id']
   #        
   #        carico = (self.db.table('shipsteps.cargo_unl_load').query(columns="""CASE WHEN $operation = 'L' THEN 'Loading cargo: ' || coalesce('BL no.' || $bln,'') || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description  
   #                                        WHEN $operation = 'U' THEN 'Unloading cargo: ' || coalesce('BL no.'|| $bln,'') || ' ' || @measure_id.description || ' ' || $quantity || ' ' || $description ELSE 'NIL' END """,
   #                                        where='$id=:cargo_id',cargo_id=car).fetch()) 
   #        operation,measure,quantity = self.db.table('shipsteps.cargo_unl_load').readColumns(columns='$operation,@measure_id.description,$quantity',
   #                                where='$id=:cargo_id',cargo_id=car)
   #        cargo_d=self.db.table('shipsteps.cargo_unl_load').query(columns='$operation,@measure_id.description,$quantity',
   #                                        where='$id=:cargo_id',cargo_id=car).fetch()
   #        
   #        if (operation == 'U' and measure =='MT.'):
   #            tot_u_cargo_mt += quantity
   #        elif (operation =='L' and measure =='MT.'):
   #            tot_l_cargo_mt += quantity
   #        if (operation == 'U' and measure =='Kgs'):
   #            tot_u_cargo_kgs += quantity
   #        elif (operation =='L' and measure =='Kgs'):
   #            tot_l_cargo_kgs += quantity
   #        if (operation == 'U' and measure =='Ltrs'):
   #            tot_u_cargo_ltrs += quantity
   #        elif (operation =='L' and measure =='Ltrs'):
   #            tot_l_cargo_ltrs += quantity
   #        cargo += ' - ' + carico[0][0] + '<br>'
   #        #a+= 1
   #    if (tot_u_cargo_mt > 0 and tot_l_cargo_mt == 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: MT. ' + str(tot_u_cargo_mt)
   #    elif (tot_u_cargo_mt == 0 and tot_l_cargo_mt > 0) :
   #        cargo = cargo +  '<br>- Tot. Loading cargo: MT. ' + str(tot_l_cargo_mt)
   #    elif (tot_u_cargo_mt > 0 and tot_l_cargo_mt > 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: MT. ' + str(tot_u_cargo_mt) + '<br>' + '- Tot. Loading cargo: MT. ' + str(tot_l_cargo_mt)
   #    if (tot_u_cargo_kgs > 0 and tot_l_cargo_kgs == 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: Kgs ' + str(tot_u_cargo_kgs)
   #    elif (tot_u_cargo_kgs == 0 and tot_l_cargo_kgs > 0) :
   #        cargo = cargo +  '<br>- Tot. Loading cargo: Kgs ' + str(tot_l_cargo_kgs)
   #    elif (tot_u_cargo_kgs > 0 and tot_l_cargo_kgs > 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: Kgs ' + str(tot_u_cargo_kgs) + '<br>' + '- Tot. Loading cargo: Kgs ' + str(tot_l_cargo_kgs)
   #    if (tot_u_cargo_ltrs > 0 and tot_l_cargo_ltrs == 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: Ltrs ' + str(tot_u_cargo_ltrs)
   #    elif (tot_u_cargo_ltrs == 0 and tot_l_cargo_ltrs > 0) :
   #        cargo = cargo +  '<br>- Tot. Loading cargo: Ltrs ' + str(tot_l_cargo_ltrs)
   #    elif (tot_u_cargo_ltrs > 0 and tot_l_cargo_ltrs > 0) :
   #        cargo = cargo +  '<br>- Tot. Unloading cargo: Ltrs ' + str(tot_u_cargo_ltrs) + '<br>' + '- Tot. Loading cargo: Ltrs ' + str(tot_l_cargo_ltrs)
   #   # print(x)
   #    return cargo

    def pyColumn_email_sof_to(self,record,field):

        pkey=record['id']
        email_dest = self.db.table('shipsteps.email_sof').query(columns="""$dest || ' ' || $description""",
                                                                    where='$sof_id=:a_id and $dest=:to' ,
                                                                    a_id=pkey, to='to').fetch()                                    
        n_email = len(email_dest) 
        email_int=''                                                               
        for r in range (n_email):
            email_int += email_dest[r][0] + '<br>'
        return email_int

    def pyColumn_email_sof_cc(self,record,field):

        pkey=record['id']
        email_dest = self.db.table('shipsteps.email_sof').query(columns="""$dest || ' ' || $description""",
                                                                    where='$sof_id=:a_id and $dest=:to' ,
                                                                    a_id=pkey, to='cc').fetch()                                    
        n_email = len(email_dest) 
        email_int=''                                                               
        for r in range (n_email):
            email_int += email_dest[r][0] + '<br>'
        return email_int
    
    def pyColumn_email_arr_to(self,record,field):
        
        pkey=record['arrival_id']
        email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
                                                                    where='$arrival_id=:a_id and $dest=:to' ,
                                                                    a_id=pkey, to='to').fetch()                                    
        n_email = len(email_dest) 
        email_int=''                                                               
        for r in range (n_email):
            email_int += email_dest[r][0] + '<br>'
        return email_int
    
    def pyColumn_email_arr_cc(self,record,field):
        
        pkey=record['arrival_id']
        email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
                                                                    where='$arrival_id=:a_id and $dest=:to' ,
                                                                    a_id=pkey, to='cc').fetch()                                    
        n_email = len(email_dest) 
        email_int=''                                                               
        for r in range (n_email):
            email_int += email_dest[r][0] + '<br>'
        return email_int

   #def pyColumn_shiprec(self,record,field):
   #   
   #    pkey=record['id']

   #    car_s=self.db.table('shipsteps.sof_cargo').query(where='$cargo_unl_load_id IS NOT NULL').fetchGrouped(key='sof_id')#fetch() 
   #    car_sof=car_s[pkey]
   #    ship_rec=''
   #    
   #    for c in car_sof:
   #        car=c['cargo_unl_load_id']
   #        shiprec = self.db.table('shipsteps.cargo_unl_load').query(columns="""CASE WHEN $operation = 'L' THEN coalesce('BL no.' || $bln,'') || ' Shipper/Caricatore: ' || @shipper_id.name 
   #                                                                        WHEN $operation = 'U' THEN coalesce('BL no.' || $bln, '') || ' Receiver/Ricevitore: ' || @receiver_id.name 
   #                                                                        ELSE '' END AS shiprec""",
   #                                                                  where='$id=:cargo_id',cargo_id=car).fetch()
   #        if ship_rec != shiprec[0][0]:                                                                             
   #            ship_rec += ' - ' + shiprec[0][0] + '<br>'
   #        
   #    return ship_rec
        
        