class Table(object): 
      def config_db(self,pkg): 
           tbl=pkg.table('imbarcazione', pkey='id')
           self.sysFields(tbl)
           tbl.column('imo', plugToForm=True, lbl='IMO',validate_notnull=True)
