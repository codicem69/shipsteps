# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('agency',pkey='id',name_long='!![en]Agency',name_plural='!![en]Agencies',caption_field='agency_name',lookup=False)
        self.sysFields(tbl)
        tbl.column('agency_name',name_short='!![en]Agency Name')
        tbl.column('description',name_short='!![en]Description Agency')
        tbl.column('address',name_short='!![en]address')
        tbl.column('tel',name_short='!![en]telephone')
        tbl.column('fax',name_short='!![en]fax')
        tbl.column('email',name_short='!![en]email')
        tbl.column('web',name_short='!![en]web')
        tbl.column('agent_name',name_short='!![en]Agent name')
        tbl.column('mobile_agent',name_short='!![en]Agent mobile')
        tbl.column('birthplace',name_short='!![en]Birth place')
        tbl.column('birthdate',dtype='D',name_short='!![en]Birth date')
        tbl.column('cciaa_n',name_short='N. CCIAA')
        tbl.column('cciaa_place',name_short='!![en]Place CCIAA')
        tbl.column('cf_agent',size='16',name_short='!![en]C.F. agent')
        tbl.column('residence_address',name_short='!![en]Residential address')
        tbl.column('cap_residence',size='5',name_short='!![en]CAP res. city')
        tbl.column('residence_city',name_short='!![en]Residential city')
        tbl.column('virtual_stamp',name_short='!![en]Virtual stamp description')
        tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='portag_unlocode', mode='foreignkey', onDelete='raise')
        tbl.column('emailpec_account_id',size='22', name_long='!![en]Email pec account'
                    ).relation('email.account.id', relation_name='', mode='foreignkey', onDelete='raise')
        tbl.column('agency_stamp', dtype='P', name_long='!![en]Agency Stamp')
        tbl.aliasColumn('fullname','@user.fullname', name_long='!![en]user signature')
        
        tbl.aliasColumn('consignee','@email_services.consignee')
        tbl.formulaColumn('fullstyle',"$agency_name || '<br>' || $address || '<br>' || 'tel. ' || $tel || '<br>' || coalesce('fax ' || $fax,'') || '<br>' || $email || '<br>' || $web ")
        
        #tbl.aliasColumn('nameag','@agency_id_name.firma_div', name_long='!![en]name ag')                                         
        #tbl.formulaColumn('dog_int', """CASE WHEN $service_fe = 'dogana' THEN $consignee ELSE NULL END""")

    def partitioning_pkeys(self):
        if self.db.currentEnv.get('current_agency_id'):
            return [self.db.currentEnv['current_agency_id']]
        else:
            return [r['id'] for r in self.query().fetch()]
        #Prendiamo gli id di tutti i dipartimenti per fare il partizionamento