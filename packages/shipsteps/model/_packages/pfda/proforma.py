# encoding: utf-8
from gnr.core.gnrdecorator import metadata
from gnr.core.gnrnumber import floatToDecimal,decimalRound
from gnr.core.gnrdecorator import public_method


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('proforma',partition_agency_id='agency_id')
        tbl.column('agency_id',size='22', name_long='!![en]agency',plugToForm=True,batch_assign=True
                    ).relation('shipsteps.agency.id', relation_name='agency_proforma', mode='foreignkey', onDelete='setNull')
        tbl.formulaColumn('note_ag',select=dict(table='pfda.fileforemail',
                                                columns='$notestandard',
                                                where='$agency_id=#THIS.agency_id'),
                                                dtype='T')
        tbl.formulaColumn('stamp_ag',select=dict(table='shipsteps.agency',
                                                columns='$agency_stamp',
                                                where='$id=#THIS.agency_id and #THIS.timbro=true'),
                                                dtype='P')
        tbl.formulaColumn('bankdetails',select=dict(table='shipsteps.agency',
                                                columns='$bank_details',
                                                where='$id=#THIS.agency_id'),
                                                dtype='T')
        tbl.formulaColumn('bank_dt',":bd || @agency_id.bank_details",
                                                where='@agency_id.id=#THIS.agency_id',dtype='T', var_bd="Our bank details: <br>")

    def defaultValues(self):
        #prendiamo i valori fissi da inserire di default nel proforma
        tbl_valorifissi = self.db.table('pfda.valorifissi')
        garbage,retaingarbage,isps,misc,notemisc,bulkauth=tbl_valorifissi.readColumns(columns='$garbageval,$retaingarbval,$ispsval,$miscval,$notemiscval,$bulkval',
                                                                                      where='$agency_id=:a_id', a_id=self.db.currentEnv.get('current_agency_id'))

        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),data = self.db.workdate,
                    garbage=garbage,retaingarbage=retaingarbage,isps=isps,misc=misc,notemisc=notemisc,bulkauth=bulkauth)

    def counter_protocollo(self,record=None):
        tbl_agency = self.db.table('shipsteps.agency')
        codice = tbl_agency.readColumns(columns='$code', where = '$id =:ag_id', ag_id=record['agency_id'])
        #F14/000001
        if len(codice) == 1:
            code = 'PFDA__'+str(codice)
        elif len(codice) == 2:
            code = 'PFDA_'+str(codice)    
        
        return dict(format='$K$YY/$NNNN',code=code,period='YY',
                   date_field='data',showOnLoad=True,recycle=True)
