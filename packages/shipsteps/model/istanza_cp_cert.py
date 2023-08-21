class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('istanza_cp_cert', pkey='id', name_long='istanza_cp certificato', name_plural='istanza cp certificati',caption_field='id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='istanza_cert_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('data_visita', dtype='D', name_short='!![en]Visit date')
        tbl.column('contatto', name_short='!![en]Contact')
        tbl.column('perconto',name_short='!![en]On behalf')
        tbl.column('registro_classe', name_short='!![en]Class registry')
        tbl.column('certificato', name_short='!![en]Certificate')
        tbl.column('navigazione', name_short='!![en]Navigation type')
        tbl.column('servizio', name_short='!![en]Service')
        tbl.column('motivo_istanza', name_short='!![en]Reason for application')
        tbl.column('note', name_short='!![en]Notes')
        tbl.column('allegati', name_short='!![en]Attachments')

