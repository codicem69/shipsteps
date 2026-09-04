# encoding: utf-8
from gnr.core.gnrbag import Bag
from gnr.core.gnrnumber import floatToDecimal,decimalRound

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('daily_sofdetails', pkey='id', name_long='!![en]Daily sof detail', name_plural='!![en]Daily sof details',caption_field='sof_id',
                        order_by='_row_count',group_carico_dep='Totale qt Magazzino')
        self.sysFields(tbl, counter='sof_id')
        
        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_daily', mode='foreignkey', onDelete='cascade')
        tbl.column('date_op', dtype='D', name_short='!![en]Date')
        tbl.column('measure_id',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='sofdaily_measure', mode='foreignkey', onDelete='raise')
        tbl.column('qt_mov', dtype='N', name_short='!![en]Quantity handled', format='#,###.000')
        tbl.column('tot_progressivo', dtype='N', name_short='!![en]Progressive Total quantity handled', format='#,###.000')
        tbl.column('shortage_surplus', dtype='N', name_short='!![en]Q.ty Shortage / Surplus', format='#,###.000')
        tbl.column('perc_short_surpl', dtype='N', name_short='!![en]Percentage Shortage / Surplus', format='#,###.000')
        #tbl.aliasColumn('totcargo','@sof_id.tot_cargo_sof', dtype='N', format='#,###.000')
        tbl.aliasColumn('nome_ricevitore','@sof_id.@sof_cargo_sof.@cargo_unl_load_id.@receiver_id.name')
        tbl.aliasColumn('totcargo','@sof_id.tot_cargo_sof')
        tbl.formulaColumn('daily_mov',"""'daily cargo discharged  -' || @measure_id.description || ' ' || $qt_mov || '<br>' ||
                                         'total cargo discharged   ' || @measure_id.description || ' ' || $tot_progressivo || '<br>' ||
                                         'remain to be discharged ' || @measure_id.description || ' ' || $shortage_surplus """)
        
        #tbl.formulaColumn('totcargo',select=dict(table='shipsteps.cargo_unl_load',
        #                                        columns='SUM($quantity) as quantity',
        #                                        where='$id=#THIS.@sof_id.@sof_cargo_sof.cargo_unl_load_id'),
        #                            dtype='N',name_long='!![en]Cargo total', format='#,###.000')
       
        #tbl.formulaColumn('measure_sof',select=dict(table='shipsteps.cargo_unl_load', columns="$measure_id",
        #                                            where='$id=#THIS.@sof_id.@sof_cargo_sof.cargo_unl_load_id'),name_long='measure_sof')

        
        tbl.formulaColumn('tot_scarico_mag',select=dict(table='shipsteps.qt_destino',
                                                  columns='SUM($tot_xdate)',
                                                  where="$dailysof_id=#THIS.id"),
                                               dtype='N',name_long='Tot.Carico Mag.', group_by='$wharehouse_id')
        tbl.subQueryColumn('day_details', query=dict(table='shipsteps.qt_destino',
                                                                columns="@wharehouse_id.descrizione as descrizione,$tot_xdate as quantità",
                                                                where='$dailysof_id=#THIS.id'), 
                                                 mode='json', name_long='Dettaglio giornaliero')
        tbl.pyColumn('events_rows',dtype='X',required_columns='$id',name_long='Q.tà magazzini')
        tbl.pyColumn('qt_progres',dtype='N',name_long='Qta progressiva')
        tbl.pyColumn('qt_handled',dtype='X',required_columns='$date_op',name_long='mov')

   
    def formulaColumn_carico(self):
        depositi = self.db.table('shipsteps.magazzini').query().fetch()
        result = []
        for r in depositi:
            result.append(
                dict(name=f'qta_{r["id"]}', select=dict(table='shipsteps.qt_destino',
                 columns='coalesce(SUM($tot_xdate),0)', where='$dailysof_id=#THIS.id AND $wharehouse_id=:dep',
                 dep=r['id']), dtype='N', name_long=f'Carico {r["descrizione"]}',
                 group='carico_dep'))
        #print(x)
        return result    
    
    #definiamo questa pyColumn per utilizzarla come dati template nell'invio email
    def pyColumn_qt_handled(self,record=None,field=None):
        if not record.get('date_op'):
            return Bag(dict(error='Missing data'))
        sof_id = record.get('sof_id')
        tbl_dailyMov = self.db.table('shipsteps.daily_sofdetails')
        records_dailymov = tbl_dailyMov.query(columns='*,$totcargo', where='$sof_id=:sof_id',sof_id=sof_id).fetch()
        rows = Bag()
        tot_progres = 0
        #for r in records_dailymov:
        for n,r in enumerate(records_dailymov,1):
            qt_mov = r['qt_mov']
            tot_progres += qt_mov
            r['tot_progressivo']=tot_progres
            r['shortage_surplus']=r['totcargo']-tot_progres
            r['perc_short_surpl']=decimalRound(r['shortage_surplus']/r['totcargo']*100)
            rows['r_%s'%(n)]=Bag(r)
            #rows.setAttr('r_%s'%(n)+'.qta',format='#,###.000')
        #print(x)   
        return rows
           

    def pyColumn_qt_progres(self,record=None,field=None):
        sof_id = record.get('sof_id')
        tbl_dailyMov = self.db.table('shipsteps.daily_sofdetails')
        records_dailymov = tbl_dailyMov.query(columns='*', where='$sof_id=:sof_id',sof_id=sof_id).fetch()
        tot_progres = 0
        for r in records_dailymov:
            qt_mov = r['qt_mov']
            tot_progres += qt_mov
            
        if r['id'] == record.get('id'):
                exit()    
        return tot_progres
    #definiamo questa pyColumn per utilizzarla come dati template nell'invio email
    def pyColumn_events_rows(self,record=None,field=None):
        if not record.get('sof_id'):
            return Bag(dict(error='Missing sof'))
        #prendiamo id del primo carico abbinato al sof
        cargo_id = record['@sof_id.@sof_cargo_sof'].keys()[0]
        #possiamo ora prendere il valore operation avendo la chiave del carico abbinato
        if cargo_id:
            operation=record['@sof_id.@sof_cargo_sof.'+cargo_id+'.@cargo_unl_load_id.operation']
        movim=''
        if operation =='U':
            movim= 'scaricato'
        else:
            movim= 'caricato'
        tot_cargo = record['@sof_id.tot_cargo_sof']
        tbl_qtdest = self.db.table('shipsteps.qt_destino')
        pkey=record.get('sof_id') #se lanciata in una view vuole record['id] se in un template vuole record['pkey] - con il get nel caso non esiste la key non torna l'errore
        date_op = record.get('date_op')
        recordsRate = tbl_qtdest.query(columns='@dailysof_id.date_op as date_op,@wharehouse_id.descrizione as magazzino, SUM($tot_xdate) as qta',
                                                    where='@dailysof_id.sof_id = :sof_id',group_by='@wharehouse_id.descrizione,@dailysof_id.date_op',
                                                    sof_id=pkey, order_by='@dailysof_id.date_op,@wharehouse_id.descrizione').fetch()
        
        recordsRateTot = tbl_qtdest.query(columns='@dailysof_id.date_op as date_op, SUM($tot_xdate) as qta',
                                                    where='@dailysof_id.sof_id = :sof_id',group_by='@dailysof_id.date_op',
                                                    sof_id=pkey, order_by='@dailysof_id.date_op').fetch()
        for r in recordsRateTot:
            r.update(dict(magazzino='Totale per data '+ str(r['qta'])))

        
        
        #aggiungiamo a recordsRate i vari dati 'Totale / Totale B/L / rimanenza e percentuale 
        #tot_movimentato=0
        #for r in recordsRate:          
        #    tot_movimentato+= r['qta']
        #
        #recordsRate.append(dict(magazzino='Totale '+movim,qta=tot_movimentato))
        #recordsRate.append(dict(magazzino='Totale B/Ls',qta=tot_cargo))
        #rimanenza = tot_cargo - tot_movimentato
        #perc_rimanenza = round((rimanenza/tot_cargo)*100,2)
        #
        #descr_rim = ''
        #if rimanenza >= 0:
        #    if record['@sof_id.ops_completed']:
        #        descr_rim = 'Ammanco'
        #    else:
        #        descr_rim='Rimanenza'
        #else:
        #    descr_rim = 'Maggior prodotto'
        #recordsRate.append(dict(magazzino=descr_rim,qta=rimanenza))
        #recordsRate.append(dict(magazzino='Percentuale '+descr_rim +' '+str(perc_rimanenza)))
        #creiamo la bag e aggiungiamo l'attributo format per visualizzare correttamente le cifre con la virgola
        rows = Bag()
        for n,r in enumerate(recordsRate,1):
            #print(X)
            rows['r_%s'%(n)]=Bag(r)
            rows.setAttr('r_%s'%(n)+'.qta',format='#,###.000')
        #print(x)   
        return rows

    def trigger_onInserted(self, record=None):
        if self.currentTrigger.parent:
            return
        sof_id = record.get('sof_id')
        if sof_id:
            self.aggiorna_Totali(sof_id)

    def trigger_onUpdated(self, record=None, old_record=None):
        if self.currentTrigger.parent:
            return
        sof_id = record.get('sof_id')
        if sof_id:
            self.aggiorna_Totali(sof_id)

    def trigger_onDeleted(self, record=None):
        if self.currentTrigger.parent:
            return
        
        sof_id = record.get('sof_id')
        if sof_id:
            self.aggiorna_Totali(sof_id)

    def aggiorna_Totali(self,sof_id=None):
        self.db.deferToCommit(self.ricalcolaTotali,
                                   sof_id=sof_id,
                                   _deferredId=sof_id)    
#    def ricalcolaTotali(self, sof_id=None):
#        if not sof_id:
#            return
#
#        tbl_daily = self.db.table('shipsteps.daily_sofdetails')
#        tbl_sof_cargo = self.db.table('shipsteps.sof_cargo')
#        tbl_cargo = self.db.table('shipsteps.cargo_unl_load')
#
#        # Totale cargo del SOF
#        cargo_rows = tbl_sof_cargo.query(
#            columns='$cargo_unl_load_id',
#            where='$sof_id=:sof_id',
#            sof_id=sof_id
#        ).fetch()
#
#        tot_cargo = 0
#
#        for cargo_row in cargo_rows:
#            quantity = tbl_cargo.readColumns(
#                columns='$quantity',
#                where='$id=:cargo_id',
#                cargo_id=cargo_row['cargo_unl_load_id']
#            ) or 0
#
#            tot_cargo += quantity
#
#        # Movimenti ordinati per data
#        rows = tbl_daily.query(
#            columns='$id,$date_op,$qt_mov',
#            where='$sof_id=:sof_id',
#            sof_id=sof_id,
#            order_by='$date_op,$id'
#        ).fetch()
#
#        tot_progressivo = 0
#
#        for row in rows:
#            qt_mov = row['qt_mov'] or 0
#            tot_progressivo += qt_mov
#
#            shortage_surplus = tot_cargo - tot_progressivo
#
#            if tot_cargo:
#                perc_short_surpl = decimalRound(
#                    shortage_surplus / tot_cargo * 100
#                )
#            else:
#                perc_short_surpl = 0
#
#            with tbl_daily.recordToUpdate(row['id']) as record:
#                record['tot_progressivo'] = tot_progressivo
#                record['shortage_surplus'] = shortage_surplus
#                record['perc_short_surpl'] = perc_short_surpl



    
    def ricalcolaTotali(self, sof_id=None):
        
        if not sof_id:
            return

        tbl_daily = self.db.table('shipsteps.daily_sofdetails')
        tbl_sof_cargo = self.db.table('shipsteps.sof_cargo')
        tbl_cargo = self.db.table('shipsteps.cargo_unl_load')

        # Totale cargo del SOF
        cargo_rows = tbl_sof_cargo.query(
            columns='$cargo_unl_load_id',
            where='$sof_id=:sof_id',
            sof_id=sof_id
        ).fetch()

        totcargo = 0

        for cargo_row in cargo_rows:
            quantity = tbl_cargo.readColumns(
                columns='$quantity',
                where='$id=:cargo_id',
                cargo_id=cargo_row['cargo_unl_load_id']
            ) or 0

            totcargo += quantity

        # Righe del SOF
        rows = tbl_daily.query(
            columns='$id,$date_op,$qt_mov',
            where='$sof_id=:sof_id',
            sof_id=sof_id,
            order_by='$date_op,$id'
        ).fetch()

        tot_progressivo = 0

        for row in rows:

            qt_mov = row['qt_mov'] or 0
            tot_progressivo += qt_mov

            shortage_surplus = totcargo - tot_progressivo

            if totcargo:
                perc_short_surpl = decimalRound(
                    shortage_surplus / totcargo * 100
                )
            else:
                perc_short_surpl = 0

            tbl_daily.update(
                dict(
                    id=row['id'],
                    tot_progressivo=tot_progressivo,
                    shortage_surplus=shortage_surplus,
                    perc_short_surpl=perc_short_surpl
                )
            )


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
           