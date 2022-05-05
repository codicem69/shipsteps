
class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('staff', pkey='id', caption_field='username', name_long='!![en]Staff', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('user_id',size='22', group='_', name_long='!![en]User'
                    ).relation('adm.user.id', relation_name='staff', mode='foreignkey', onDelete='raise')
        tbl.column('agency_id', size='22', name_long='!![en]Agency').relation('agency.id',
                        relation_name='user', mode='foreignkey', onDelete='raise')    
        tbl.column('name',name_long='!![en]Name')
        tbl.column('surname',name_long='!![en]Surname') 
        tbl.column('telephone',name_long='!![en]Telephone')
        tbl.column('email',name_long='!![en]E-mail')  
        tbl.column('note', name_long='note')
        tbl.column('department', name_long='department')
        tbl.column('profile_photo', dtype='P', name_long='!![en]Profile photo')
        tbl.column('is_active', dtype='B', name_long='!![en]Is active')   
        tbl.column('email_account_id',size='22', name_long='!![en]Email account'
                    ).relation('email.account.id', relation_name='', mode='foreignkey', onDelete='raise')
        #tbl.formulaColumn('fullname', """$name ||' '||$surname || '<br>' || coalesce($department ||' department <br>','') 
        #                    || coalesce('mob.: ' || $telephone || '<br>', '') || coalesce('email: ' || $email || '<br>' , '') 
        #                    || coalesce($note,'') """, name_long='!![en]Fullname')
        tbl.aliasColumn('username', '@user_id.username', name_long='!![en]Username')
       
        tbl.formulaColumn('fullname',select=dict(table='shipsteps.staff',
                                                columns="""$name ||' '||$surname || '<br>' || coalesce($department ||' department <br>','') 
                            || coalesce('mob.: ' || $telephone || '<br>', '') || coalesce('email: ' || $email || '<br>' , '') 
                            || coalesce($note,'') """,
                                                where='$user_id =:env_user_id',
                                                dtype='T',name_long='!![en]fullname'))