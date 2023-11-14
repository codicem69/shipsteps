# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_arr', pkey='id', name_long='email_arr', name_plural='email_arr',
                        caption_field='description')
        self.sysFields(tbl, counter='arrival_id')

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='arrival_email', mode='foreignkey', onDelete='cascade')
        tbl.column('dest', name_short='!![en]Destination',values='to:to,cc:cc')           
        tbl.column('description', name_short='!![en]Email description')
        tbl.column('email', name_short='Email arrival')
        tbl.column('email_type', size=':3', name_short='!![en]Email type', values='to:to,cc:cc,ccn:ccn')
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.formulaColumn('email_int',"$dest || ' ' || $description",order_by='$dest DESC',group_by='$dest', dtype='T')
        
    

    
