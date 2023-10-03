# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof', pkey='id', name_long='sof', name_plural='sof',caption_field='sof_det')
        self.sysFields(tbl,counter=True)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='sof_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('sof_n',dtype='T', name_short='!![en]SOF n.')
        tbl.column('nor_tend', dtype='DH', name_short='!![en]NOR tendered')
        tbl.column('nor_rec', dtype='DH', name_short='!![en]NOR received')
        tbl.column('nor_acc', dtype='T', name_short='!![en]NOR accepted')
        tbl.column('customs_commenced', dtype='DH', name_short='!![en]Customs formalities commenced')
        tbl.column('customs_completed', dtype='DH', name_short='!![en]Customs formalities completed')
        tbl.column('ops_commenced', dtype='DH', name_short='!![en]Load/Unload commenced')
        tbl.column('ops_completed', dtype='DH', name_short='!![en]Load/Unload completed')
        tbl.column('doc_onboard', dtype='DH', name_short='!![en]Documents onboard')
        tbl.column('remarks_rs', name_short='!![en]Receivers / Shippers Remarks')
        tbl.column('remarks_cte', name_short='!![en]Master Remarks')
        tbl.column('note', name_short='!![en]Note SOF')
        tbl.column('onbehalf', name_short='!![en]On behalf')
        tbl.column('int_sof', name_short='!![en]Sof header')
        tbl.column('htmlbag', dtype='X', name_long='HTML Doc Bag')
        tbl.column('htmlbag_lop', dtype='X', name_long='HTML Doc LOP Bag')
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('ship_rec','@sof_cargo_sof.ship_rec')
        tbl.aliasColumn('cargo_sof', '@sof_cargo_sof.@cargo_unl_load_id.cargo_sof',name_long='!![en]Cargo sof')
       # tbl.aliasColumn('carico_del_sof', '@sof_cargo_sof.carico_del_sof',name_long='!![en]Cargo on sof')
        tbl.aliasColumn('cargo_op', '@sof_cargo_sof.@cargo_unl_load_id.operation',name_long='!![en]Cago operation')
        tbl.aliasColumn('receivers_name', '@sof_cargo_sof.@cargo_unl_load_id.@receiver_id.name',name_long='!![en]Receivers name')
        tbl.aliasColumn('shiprec_sofcargo','@sof_cargo_sof.ship_rec')
        tbl.aliasColumn('agencyname','@arrival_id.@agency_id.agency_name')
        tbl.aliasColumn('timearr','@arrival_id.@time_arr.time_arr')
        tbl.aliasColumn('timearr2','@arrival_id.@time_arr.time_arr_2')
        tbl.aliasColumn('sofop_int','@sof_operations.operation_int')
        tbl.aliasColumn('sof_shiprec','@sof_cargo_sof.@cargo_unl_load_id.sof_shiprec')
        tbl.pyColumn('shiprec',name_long='!![en]Shipper or Receiver')
        tbl.pyColumn('shiprec_bl',name_long='!![en]Shipper or Receiver BL')
        tbl.pyColumn('carico_del_sof',name_long='!![en]Cargo on sof')
        tbl.pyColumn('carico_sofbl',name_long='!![en]Cargo on sof BL')
        #tbl.pyColumn('email_sof_to',name_long='!![en]Email sof to', static=True)
        #tbl.pyColumn('email_sof_cc',name_long='!![en]Email sof cc', static=True)
        #tbl.pyColumn('email_arr_to',name_long='!![en]Email arrival to', static=True)
        #tbl.pyColumn('email_arr_cc',name_long='!![en]Email arrival cc', static=True)
        #tbl.pyColumn('totcarico',name_long='!![en]Totcarico', static=True)
        tbl.formulaColumn('tot_cargo_sof',select=dict(table='shipsteps.cargo_unl_load',
                                                columns='SUM($quantity)',
                                                where='$id=#THIS.@sof_cargo_sof.cargo_unl_load_id'),
                                    dtype='N',name_long='!![en]Cargo total', format='#,###.000')
        tbl.formulaColumn('int_carico',"""CASE WHEN $cargo_sof <>'NIL' THEN 'CARGO DETAILS<br>' || :carsof ELSE '' END""",dtype='T',var_carsof='------------------------------<br>')
        tbl.formulaColumn('sof_det',"$sof_n || '-' || @arrival_id.reference_num || ' - ' || @arrival_id.date || ' - ' || @arrival_id.@vessel_details_id.@imbarcazione_id.nome")
        tbl.formulaColumn('nor_tend_txt', """CASE WHEN $nor_tend is not null THEN 'NOR tendered' || '<br>'  ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_rec_txt', """CASE WHEN $nor_rec is not null THEN 'NOR received' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_acc_txt', """CASE WHEN $nor_acc is not null THEN 'NOR acceppted' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('customs_commenced_txt', """CASE WHEN $customs_commenced is not null THEN 'Customs formalities commenced '  || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('customs_completed_txt', """CASE WHEN $customs_completed is not null THEN 'Customs formalities completed '  || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_commenced_txt', """CASE WHEN $ops_commenced is not null AND $cargo_op = 'U' THEN 'Unloading commenced '  || '<br>' 
                                                  WHEN $ops_commenced is not null AND $cargo_op = 'L' THEN 'Loading commenced ' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_completed_txt', """CASE WHEN $ops_completed is not null AND $cargo_op = 'U' THEN 'Unloading completed '  || '<br>'
                                                  WHEN $ops_completed is not null AND $cargo_op = 'L' THEN 'Loading completed ' || '<br>' ELSE '' END""", dtype='T')
        tbl.formulaColumn('customs_commenced_email', """CASE WHEN $customs_commenced is not null THEN 'Customs formalities commenced-' ELSE '' END""", dtype='T')
        tbl.formulaColumn('customs_completed_email', """CASE WHEN $customs_completed is not null THEN 'Customs formalities completed-' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_commenced_email', """CASE WHEN $ops_commenced is not null AND $cargo_op = 'U' THEN 'Unloading commenced-----------'
                                                  WHEN $ops_commenced is not null AND $cargo_op = 'L' THEN 'Loading commenced-------------' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_completed_email', """CASE WHEN $ops_completed is not null AND $cargo_op = 'U' THEN 'Unloading completed-----------'
                                                  WHEN $ops_completed is not null AND $cargo_op = 'L' THEN 'Loading completed-------------' ELSE '' END""", dtype='T')
        tbl.formulaColumn('doc_onboard_txt', """CASE WHEN $doc_onboard is not null THEN  :onboard  || '<br>' END""",  dtype='T', var_onboard="cargo's documents on board ")
        tbl.formulaColumn('nor_tend_time', """CASE WHEN $nor_tend is not null THEN to_char($nor_tend, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('nor_rec_time', """CASE WHEN $nor_rec is not null THEN to_char($nor_rec, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('nor_acc_time', """CASE WHEN $nor_acc is not null THEN $nor_acc || '<br>'  ELSE '' END""", dtype='T')
        tbl.formulaColumn('customs_commenced_time', """CASE WHEN $customs_commenced is not null THEN to_char($customs_commenced, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('customs_completed_time', """CASE WHEN $customs_completed is not null THEN to_char($customs_completed, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('ops_commenced_time', """CASE WHEN $ops_commenced is not null THEN to_char($ops_commenced, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('ops_completed_time', """CASE WHEN $ops_completed is not null THEN to_char($ops_completed, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')
        tbl.formulaColumn('doc_onboard_time', """CASE WHEN $doc_onboard is not null THEN to_char($doc_onboard, :df) || '<br>'  ELSE '' END""", dtype='T',var_df='DD/MM/YYYY HH24:MI')

        tbl.formulaColumn('note_txt', """CASE WHEN $note is not null THEN 'Notes/Rain Times/General Reamarks' || '<br>'  ELSE '' END""", dtype='T')
        
        
        tbl.formulaColumn('time_sof', """coalesce('NOR tendered------------------' || to_char($nor_tend, :df) || '<br>', '') || coalesce('NOR received------------------' || to_char($nor_rec, :df) || '<br>','') ||
                                         coalesce('NOR accepted------------------' || $nor_acc || '<br>', '') || coalesce($customs_commenced_email || to_char($customs_commenced, :df) || '<br>','') ||
                                         coalesce($customs_completed_email || to_char($customs_completed, :df) || '<br>','') || coalesce($ops_commenced_email || to_char($ops_commenced, :df) || '<br>','') || 
                                         coalesce($ops_completed_email || to_char(ops_completed, :df) || '<br>','') || coalesce(:onboard || to_char($doc_onboard,:df) || '<br>','')""",var_onboard="Documents on board------------",var_df='DD/MM/YYYY HH24:MI')
        #tbl.formulaColumn('portlog_time',"""CASE WHEN $timearr is not null OR $time_sof is not null OR $timearr2 is not null THEN 
        #                                    'PORTLOG<br>------------------------------<br>' || $timearr || '<br>' || $time_sof || '<br>' || $timearr2 || '<br>' END""")
        tbl.formulaColumn('portlog_time',"""CASE WHEN $timearr !='' THEN 'PORTLOG<br>------------------------------<br>' || coalesce($timearr,'') || coalesce($time_sof ,'') || coalesce($timearr2 ,'') END""")
        tbl.formulaColumn('intestazione_sof',"""CASE WHEN $int_sof is null THEN $agencyname 
                                                WHEN $int_sof = '' THEN $agencyname ELSE $int_sof END""" )
        tbl.formulaColumn('email_sof_to',select=dict(table='shipsteps.email_sof', columns="""string_agg($dest || ' ' || $description || '<br>', '')""",
                                                    where='$sof_id=#THIS.id and $dest=:to',to='to', limit=1,ignoreMissing=True))
        tbl.formulaColumn('email_sof_cc',select=dict(table='shipsteps.email_sof', columns="""string_agg($dest || ' ' || $description ||'<br>', '')""",
                                                    where='$sof_id=#THIS.id and $dest=:to',to='cc', limit=1,ignoreMissing=True))
        tbl.formulaColumn('fullstyle_for_rec',"""CASE WHEN $firma_diversa IS NULL OR $firma_diversa = '' THEN @arrival_id.@agency_id.fullstyle 
                                                 ELSE $firma_diversa END""", dtype='T')
        tbl.aliasColumn('firma_diversa','@arrival_id.firma_div')
        tbl.aliasColumn('email_arr_to','@arrival_id.email_arr_to')
        tbl.aliasColumn('email_arr_cc','@arrival_id.email_arr_cc')
        tbl.formulaColumn('this_port','UPPER(@arrival_id.@agency_id.@port.descrizione)')
        tbl.formulaColumn('tot_mov',select=dict(table='shipsteps.daily_sofdetails',
                                                columns="$tot_progressivo",
                                                where='$sof_id=#THIS.id',order_by='$date_op DESC',
                                                limit=1,dtype='N'))
        tbl.formulaColumn('shortage',select=dict(table='shipsteps.daily_sofdetails',
                                                columns="$shortage_surplus",
                                                where='$sof_id=#THIS.id',order_by='$date_op DESC',
                                                limit=1,dtype='N'))                                                
        #formulaColumn measure_sof verifica il tipo di misura del carico inserito e sarà passato nello store tramite la form di sof con form.store.handler('load',virtual_columns='$measure_sof')
        #che ci servirà in th_daily_sofdetails a filtrare il solo tipo di misura da scegliere tramite la condition nel campo measure_id
        tbl.formulaColumn('measure_sof',select=dict(table='shipsteps.cargo_unl_load', columns="$measure_id",
                                                    where='$id=#THIS.@sof_cargo_sof.cargo_unl_load_id'),name_long='measure_sof')
        
     
        tbl.aliasColumn('measure','@sof_daily.@measure_id.description')
        tbl.aliasColumn('place_origin_goods','@sof_cargo_sof.@cargo_unl_load_id.@place_origin_goods.citta_nazione')

    def pyColumn_carico_del_sof(self,record,field):
        p_key=record['id']
        #prepariamo i dati per la descrizione del carico con le relative BL e operazioni unloding/loading
        carico = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation,coalesce('BL no.' || @cargo_unl_load_id.bln,''), @cargo_unl_load_id.@measure_id.description, @cargo_unl_load_id.quantity,@cargo_unl_load_id.description",
                                                                where='sof_id=:sofid',sofid=p_key).fetch()
        cargo=''
        for c in range(len(carico)):
            if carico[c][0]== 'U':
                cargo += '- Unloading cargo: ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + ' ' + str(carico[c][4]) + '<br>'
            elif carico[c][0]== 'L':
                cargo += '- Loading cargo: ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + ' ' + str(carico[c][4]) + '<br>'
            else:
                cargo = ''
        #prepariamo i dati per il totale carico
        tot_carico = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation, @cargo_unl_load_id.@measure_id.description, SUM(@cargo_unl_load_id.quantity)",
                                                                where='sof_id=:sofid',sofid=p_key, group_by='@cargo_unl_load_id.@measure_id.description,@cargo_unl_load_id.operation').fetch()
        totale_carico=''
        for c in range(len(tot_carico)):
            if tot_carico[c][0]== 'U':
                totale_carico += '- Tot. unloading cargo: ' + str(tot_carico[c][1]) + ' ' + str(tot_carico[c][2]) + '<br>'
            elif tot_carico[c][0]== 'L':
                totale_carico += '- Tot. loading cargo: ' + str(tot_carico[c][1]) + ' ' + str(tot_carico[c][2]) + '<br>' 
            else:
                totale_carico =''
        #inseriamo in un unica variabile tutti i dati relativi al carico sopra calcolati
        if cargo != '' or totale_carico != '':
            descr_carico = cargo + '<br>' + totale_carico
        else:
            descr_carico = ''
        return descr_carico

    def pyColumn_carico_sofbl(self,record,field):
        p_key=record['id']
        #prepariamo i dati per la descrizione del carico con le relative BL e operazioni unloding/loading
        carico = self.db.table('shipsteps.sof_cargo').query(columns="""@cargo_unl_load_id.@measure_id.description, @cargo_unl_load_id.quantity,@cargo_unl_load_id.description,
                                                                     coalesce('BL no.' || @cargo_unl_load_id.bln,''),coalesce(' Dated ' || to_char(@cargo_unl_load_id.bl_date, :df),'') || coalesce(' ' || @cargo_unl_load_id.@place_origin_goods.citta_nazione,'')""",
                                                                where='sof_id=:sofid',sofid=p_key,df='DD/MM/YYYY').fetch()
        #print(x)                                                                
        cargo=''
        for c in range(len(carico)):
            if c in range(0,len(carico)-1):
                cargo += '- ' + str(carico[c][0]) + ' ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + str(carico[c][4]) + '<br>'
            else:
                cargo += '- ' + str(carico[c][0]) + ' ' + str(carico[c][1]) + ' ' + str(carico[c][2]) + ' ' + str(carico[c][3]) + str(carico[c][4])
        #prepariamo i dati per il totale carico
        tot_carico = self.db.table('shipsteps.sof_cargo').query(columns="@cargo_unl_load_id.operation, @cargo_unl_load_id.@measure_id.description, SUM(@cargo_unl_load_id.quantity)",
                                                                where='sof_id=:sofid',sofid=p_key, group_by='@cargo_unl_load_id.@measure_id.description,@cargo_unl_load_id.operation').fetch()
        totale_carico=''
        for c in range(len(tot_carico)):
            totale_carico += '-Total Bill of lading quantity: ' + str(tot_carico[c][1]) + ' ' + str(tot_carico[c][2]) + '<br>'
            
        #inseriamo in un unica variabile tutti i dati relativi al carico sopra calcolati
        if cargo != '' or totale_carico != '':
            descr_carico = cargo + '<br>' + totale_carico
        else:
            descr_carico = ''
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
            if receiver[c][0] != '':
                rec += '<br>' + receiver[c][0] + '<br>'             
        ship=''
        for c in range(len(shipper)):
            if shipper[c][0] != '':
                rec += '<br>' + shipper[c][0] + '<br>'
        if rec != '' or rec != '':
            ship_rec = rec + ship + '<br>'
        else:
            ship_rec=''    
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

    #def pyColumn_email_sof_to(self,record,field):

    #    pkey=record['id']
    #    email_dest = self.db.table('shipsteps.email_sof').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$sof_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='to').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += str(email_dest[r][0]) + '<br>'
    #    return email_int

    #def pyColumn_email_sof_cc(self,record,field):

    #    pkey=record['id']
    #    email_dest = self.db.table('shipsteps.email_sof').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$sof_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='cc').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += str(email_dest[r][0]) + '<br>'
    #    return email_int
    
    #def pyColumn_email_arr_to(self,record,field):
    #    
    #    pkey=record['arrival_id']
    #    email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$arrival_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='to').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += str(email_dest[r][0]) + '<br>'
    #    return email_int
    #
    #def pyColumn_email_arr_cc(self,record,field):
    #    
    #    pkey=record['arrival_id']
    #    email_dest = self.db.table('shipsteps.email_arr').query(columns="""$dest || ' ' || $description""",
    #                                                                where='$arrival_id=:a_id and $dest=:to' ,
    #                                                                a_id=pkey, to='cc').fetch()                                    
    #    n_email = len(email_dest) 
    #    email_int=''                                                               
    #    for r in range (n_email):
    #        email_int += email_dest[r][0] + '<br>'
    #    return email_int

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
    
    @public_method
    def getHTMLDoc(self,sof_id=None,record_template=None,**kwargs):
        testo=TableTemplateToHtml(table=self,record_template=record_template).contentFromTemplate(record=sof_id)
        return testo


    def counter_sof_n(self,record=None):
        #2021/000001
        #return dict(format='$K$YYYY/$NNNNNN', code='A', period='YYYY', date_field='date', showOnLoad=True, date_tolerant=True)
        return dict(format='$K/$NNN',code='S', showOnLoad=True)    
