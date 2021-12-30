#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='shipsteps package',sqlschema='shipsteps',sqlprefix=True,
                    name_short='Shipsteps', name_long='shipsteps', name_full='Shipsteps')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
